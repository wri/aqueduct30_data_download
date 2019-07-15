
# coding: utf-8

# In[1]:

"""
Process and export all aqueduct 30 data.

When users want to download the entire dataset, this is what they will get. 

Author: Rutger Hofste
Date: 20190711
Kernel: python35
Docker: rutgerhofste/gisdocker:ubuntu16.04

"""

SCRIPT_NAME = "Y2019M07D11_RH_Aqueduct30_Data_Download"
OUTPUT_VERSION = 1

S3_INPUT_PATH = {}
S3_INPUT_PATH["master_geom_simplified"] = "s3://wri-projects/Aqueduct30/processData/Y2019M07D09_RH_Simplified_Geometries_V01/output_V02"
S3_INPUT_PATH["annual"] = "s3://wri-projects/Aqueduct30/finalData/Y2019M01D14_RH_Aqueduct_Results_V01/output_V04/annual"

# We simplified the master_geom using verious keep_percentages. 
KEEP_PERCENT = 30

INPUT_FILENAME = {}
INPUT_FILENAME["master_geom_simplified"] = "mastergeom_mapshaper_visvalingam_keeppercent{:03.0f}_v01.shp".format(KEEP_PERCENT)
INPUT_FILENAME["annual"] = "annual_pivot.pkl"

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

get_ipython().system('aws s3 cp {S3_INPUT_PATH["master_geom_simplified"]} {ec2_input_path} --recursive --quiet')


# In[5]:

get_ipython().system('aws s3 cp {S3_INPUT_PATH["annual"]} {ec2_input_path} --recursive')


# In[ ]:




# In[50]:

import pandas as pd
import geopandas as gpd
from tqdm import tqdm

from shapely.geometry import MultiPolygon, shape


# In[51]:

input_path_master_geom_simplified = "{}/{}".format(ec2_input_path,INPUT_FILENAME["master_geom_simplified"])


# In[78]:

gdf_in = gpd.read_file(filename=input_path_master_geom_simplified)


# In[79]:

gdf_in.head()


# In[85]:

gdf_in.shape


# In[80]:

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
    


# In[91]:

gdf = df_force_multipolygon(gdf_in)


# In[92]:

# Change column order. See https://github.com/wri/aqueduct_analyze_locations/blob/master/data_download/instructions.md#annual-baseline
gdf = gdf[["string_id","aq30_id","pfaf_id","gid_1","aqid","geometry"]]


# ## Annual

# In[82]:

input_path_annual = "{}/{}".format(ec2_input_path,INPUT_FILENAME["annual"])


# In[132]:

df_annual = pd.read_pickle(path=input_path_annual)


# In[133]:

df_annual.head()


# In[134]:

df_annual.shape


# In[135]:

def annual_column_order():
    """
    Create a list of the preferred column order. 
    
    See https://github.com/wri/aqueduct_analyze_locations/blob/master/data_download/instructions.md#annual-baseline
    
    Args:
        none
    Returns:
        columns(list): List of strings with column names
    
    """
    # Indicator Columns
    indicators =   ["bws",
                    "bwd",
                    "iav",
                    "sev",
                    "gtd",
                    "rfr",
                    "cfr",
                    "drr",
                    "ucw",
                    "cep",
                    "udw",
                    "usa",
                    "rri"]
    types = ["raw","score","cat","label"]
    
    indicator_columns =[]
    for indicator in indicators:
        for one_type in types:
            column = "{}_{}".format(indicator,one_type)
            indicator_columns.append(column)
            
    # Grouped Water Risk Columns        
    industries =   ["def",
                    "agr",
                    "che",
                    "con",
                    "elp",
                    "fnb",
                    "min",
                    "ong",
                    "smc",
                    "tex"]
    
    groups = ["qan",
              "qal",
              "rrr",
              "tot"]
        
    types_awr = ["raw","score","cat","label","weight_fraction"]
    grouped_water_risk_columns = []
    for industry in industries:
        for group in groups:
            for one_type_awr in types_awr:
                column = "w_awr_{}_{}_{}".format(industry,group,one_type_awr)
                grouped_water_risk_columns.append(column)
    
    columns = indicator_columns + grouped_water_risk_columns
    
    return columns


# In[136]:

result_column_names = annual_column_order()


# In[137]:

extra_column_names = ["string_id","gid_0","name_0","name_1","area_km2"]


# In[138]:

annual_column_names = extra_column_names + result_column_names


# In[139]:

df_annual = df_annual[annual_column_names]


# In[140]:

gdf_annual = gdf.merge(df_annual,on="string_id",how="left")


# In[141]:

gdf_annual.shape


# In[143]:

gdf_annual.head()


# In[144]:

gdf_annual.sort_values(by="aq30_id",inplace=True)


# # Monthly

# In[ ]:




# In[ ]:




# In[ ]:




# # Export

# In[146]:

output_filename_annual = "y2019m07d11_aqueduct30_annual_v01"


# In[147]:

output_path_annual = "{}/{}".format(ec2_output_path,output_filename_annual)


# In[ ]:

gdf_annual.to_file(driver="GPKG",
                   filename=output_path_annual + ".gpkg",
                   encoding="UTF-8")


# In[ ]:

get_ipython().system('aws s3 cp {ec2_output_path} {s3_output_path}  --recursive')


# In[ ]:



