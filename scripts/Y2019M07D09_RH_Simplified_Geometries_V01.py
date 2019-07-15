
# coding: utf-8

# In[1]:

"""
Simplify master geometry

Changed to just simplify the master geometry using the mapshaper cli.

Author: Rutger Hofste
Date: 20190709
Kernel: python35
Docker: rutgerhofste/gisdocker:ubuntu16.04

"""

SCRIPT_NAME = "Y2019M07D09_RH_Simplified_Geometries_V01"
OUTPUT_VERSION = 2


S3_INPUT_PATH = {}
S3_INPUT_PATH["master_geom"] = "s3://wri-projects/Aqueduct30/finalData/Y2019M01D14_RH_Aqueduct_Results_V01/output_V04/master_geom"

INPUT_FILENAME = {}
INPUT_FILENAME["master_geom"] = "master_geom.shp"


ec2_input_path = "/volumes/data/{}/input_V{:02.0f}".format(SCRIPT_NAME,OUTPUT_VERSION)
ec2_output_path = "/volumes/data/{}/output_V{:02.0f}".format(SCRIPT_NAME,OUTPUT_VERSION)

s3_output_path = "s3://wri-projects/Aqueduct30/processData/{}/output_V{:02.0f}/".format(SCRIPT_NAME,OUTPUT_VERSION)

KEEP_FRACTION = {}
KEEP_FRACTION["master_geom"] = 0.5

print(s3_output_path)


# In[2]:

get_ipython().system('mapshaper -v')


# In[3]:

import time, datetime, sys
dateString = time.strftime("Y%YM%mD%d")
timeString = time.strftime("UTC %H:%M")
start = datetime.datetime.now()
print(dateString,timeString)
sys.version
get_ipython().magic('matplotlib inline')


# In[4]:

import subprocess


# In[5]:

get_ipython().system('rm -r {ec2_input_path} ')
get_ipython().system('rm -r {ec2_output_path} ')
get_ipython().system('mkdir -p {ec2_input_path} ')
get_ipython().system('mkdir -p {ec2_output_path} ')


# In[6]:

get_ipython().system('aws s3 cp {S3_INPUT_PATH["master_geom"]} {ec2_input_path} --recursive')


# In[7]:

def simplify_mapshaper(keep_fraction):
    """
    Simplify geometry using mapshaper's Visvalingam algorithm.
    
    See https://github.com/mbloch/mapshaper
    
    Args:
        keep_fraction(double): keep fraction [0.-1.]
    
    Returns:
        command(string): bash command
    
    """
    
    input_filename = INPUT_FILENAME["master_geom"]
    input_path =  "{}/{}".format(ec2_input_path,input_filename)
    
    
    output_filename = "mastergeom_mapshaper_visvalingam_keeppercent{:03.0f}_v01.shp".format(keep_fraction*100)
    output_path  = "{}/{}".format(ec2_output_path,output_filename)
    
    command = "mapshaper -i snap {} -simplify weighted keep-shapes {} -clean -o format=shapefile {}".format(input_path,keep_fraction,output_path)
    return command
    


# In[8]:

keep_fractions = [0.1, 0.2, 0.3, 0.5, 0.8, 1.0]


# In[9]:

for keep_fraction in keep_fractions:
    command = simplify_mapshaper(keep_fraction)
    print(command)
    response = subprocess.check_output(command,shell=True)


# In[10]:

get_ipython().system('aws s3 cp {ec2_output_path} {s3_output_path} --recursive')


# In[11]:

end = datetime.datetime.now()
elapsed = end - start
print(elapsed)


# Previous runs:  
# 0:07:14.833033
# 

# In[ ]:



