
# coding: utf-8

# In[1]:

"""
Process and export monthly data.



Author: Rutger Hofste
Date: 20190712
Kernel: python35
Docker: rutgerhofste/gisdocker:ubuntu16.04

"""

TESTING = 0

SCRIPT_NAME = "Y2019M07D12_RH_Aqueduct30_Data_Download_Monthly_V01"
OUTPUT_VERSION = 2

S3_INPUT_PATH = {}
S3_INPUT_PATH["hybas"] = "s3://wri-projects/Aqueduct30/processData/Y2017M08D02_RH_Merge_HydroBasins_V02/output_V04"
S3_INPUT_PATH["monthly"] = "s3://wri-projects/Aqueduct30/finalData/Y2019M01D14_RH_Aqueduct_Results_V01/output_V04/monthly"


INPUT_FILENAME = {}
INPUT_FILENAME["hybas"] = "hybas_lev06_v1c_merged_fiona_V04.shp"


ec2_input_path = "/volumes/data/{}/input_V{:02.0f}".format(SCRIPT_NAME,OUTPUT_VERSION)
ec2_output_path = "/volumes/data/{}/output_V{:02.0f}".format(SCRIPT_NAME,OUTPUT_VERSION)

s3_output_path = "s3://wri-projects/Aqueduct30/processData/{}/output_V{:02.0f}/".format(SCRIPT_NAME,OUTPUT_VERSION)

print(s3_output_path)


# In[2]:

import time, datetime, sys
dateString = time.strftime("Y%YM%mD%d")
timeString = time.strftime("UTC %H:%M")
start = datetime.datetime.now()
print(dateString,timeString)
sys.version
get_ipython().magic('matplotlib inline')


# In[3]:

get_ipython().system('rm -r {ec2_input_path} ')
get_ipython().system('rm -r {ec2_output_path} ')
get_ipython().system('mkdir -p {ec2_input_path} ')
get_ipython().system('mkdir -p {ec2_output_path} ')


# In[4]:

get_ipython().system('aws s3 cp {S3_INPUT_PATH["hybas"]} {ec2_input_path} --recursive --quiet')


# In[5]:

get_ipython().system('aws s3 cp {S3_INPUT_PATH["monthly"]} {ec2_input_path} --recursive --quiet')


# In[6]:

import pandas as pd
import geopandas as gpd
from tqdm import tqdm

from shapely.geometry import MultiPolygon, shape


# In[7]:

input_path_geom = "{}/{}".format(ec2_input_path,INPUT_FILENAME["hybas"])


# In[8]:

def convert_row_to_multipolygon(row):
    if row.type == "Polygon":
        new_geom = MultiPolygon([row.geometry])
    elif row.type == "MultiPolygon":
        new_geom = row.geometry
    else:
        new_geom = -9999
    return new_geom
    
def df_force_multipolygon(gdf):
    """
    Force all geometries in a geodataframe to be 
    MultiPolygons. The GeoPackage format does not allow
    mixing of polygons and multipolygons.   
    
    Args:
        gdf(GeoDataFrame) : GeoDataFrame
    Returns:
        gdf_mp(GeoDataFrame): GeodataFrame with multipolygons
    
    """
    gdf_temp = gdf.copy()
    gdf_temp["type"] = gdf_temp["geometry"].geom_type
    gdf["geometry"] = gdf_temp.apply(axis=1,func=convert_row_to_multipolygon)
    return gdf

def process_df(df,indicator,month):
    """
    Process monthly dataframe
    
    Args:
        df(dataframe): input dataframe
        indicator(string): short name for indicator. in bws bwd iav
        month(integere): month 
    
    Return:
        df_out(dataframe) : output dataframe. simplified, clean, beatiful!
    
    
    """
    df_out = df[["pfaf_id","raw","score","cat","label"]]
    df_out = df_out.rename(columns={"raw":"{}_{:02.0f}_raw".format(indicator,month),
                                    "score":"{}_{:02.0f}_score".format(indicator,month),
                                    "cat":"{}_{:02.0f}_cat".format(indicator,month),
                                    "label":"{}_{:02.0f}_label".format(indicator,month)})
    df_out.set_index("pfaf_id",inplace=True)
    
    return df_out

def process_gdf(gdf):
    """
    Process the hydrobasin level6 geodataframe 
    
    Dropping a weird polygon that crosses the -180 meridian and has a 
    non unique ID 353020
    
    Args:
        gdf(geodataframe): hydrobasin level 6 geodataframe
    Returns:
        gdf_out(geodataframe): simple, clean beatiful
    
    """
    gdf_out = gdf.loc[gdf["PFAF_ID"] != 353020]
    
    drop_columns = ["HYBAS_ID",
                    "NEXT_DOWN",
                    "NEXT_SINK",
                    "MAIN_BAS",
                    "DIST_SINK",
                    "DIST_MAIN",
                    "SUB_AREA",
                    "UP_AREA",
                    "ENDO",
                    "COAST",
                    "ORDER",
                    "SORT"]
    
    
    gdf_out = gdf_out.drop(drop_columns,axis=1)
    gdf_out = gdf_out.rename(columns={"PFAF_ID":"pfaf_id"})
    gdf_out = df_force_multipolygon(gdf_out)
    return gdf_out
    
    


# In[9]:

gdf_in = gpd.read_file(filename=input_path_geom)


# In[10]:

gdf_in.shape


# In[11]:

gdf = process_gdf(gdf_in)


# In[12]:

gdf.head()


# # Add monthly tabular data, pivot

# In[13]:

indicators = ["bws",'bwd','iav']


# In[14]:

months = range(1,12+1)


# In[15]:


for indicator in indicators:
    input_filename = "monthly_{}.pkl".format(indicator)
    input_path = "{}/{}".format(ec2_input_path,input_filename)
    df = pd.read_pickle(path=input_path)
        
    for month in months:
        df_month = df.loc[df["month"]==month]
        df_month = process_df(df_month,indicator,month)

        gdf = gdf.merge(right=df_month,
                        how="left",
                        left_on="pfaf_id",
                        right_index=True)


# In[16]:

output_filename= "{}".format(SCRIPT_NAME).lower()


# In[17]:

output_path = "{}/{}".format(ec2_output_path,output_filename)


# In[ ]:

gdf.to_file(driver="GPKG",
            filename=output_path + ".gpkg",
            encoding="UTF-8")


# In[ ]:

get_ipython().system('aws s3 cp {ec2_output_path} {s3_output_path}  --recursive')


# In[ ]:

end = datetime.datetime.now()
elapsed = end - start
print(elapsed)


# Previous runs:  
# 0:02:06.463591
# 

# In[ ]:



