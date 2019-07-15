
# coding: utf-8

# In[1]:

"""
Process and export monthly data.

When users want to download the entire dataset, this is what they will get. 

Author: Rutger Hofste
Date: 20190712
Kernel: python35
Docker: rutgerhofste/gisdocker:ubuntu16.04

"""

TESTING = 0

SCRIPT_NAME = "Y2019M07D11_RH_Aqueduct30_Data_Download_Annual_V01"
OUTPUT_VERSION = 2

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


# In[ ]:



