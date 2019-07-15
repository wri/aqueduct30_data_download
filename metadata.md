This document will help you understand the downloaded Aqueduct data. Before diving into the results, make sure to familiarize yourself with our technical notes (todo:insert link). For questions, check out our FAQ page (todo:insert link)

Downloaded data comes in three flavors:
1. [Annual Baseline](https://github.com/wri/aqueduct_analyze_locations/blob/master/data_download/instructions.md#annual-baseline
)
1. [Monthly Baseline](https://github.com/wri/aqueduct_analyze_locations/blob/master/data_download/instructions.md#monthly-baseline)
1. [Future Projections](https://github.com/wri/aqueduct_analyze_locations/blob/master/data_download/instructions.md#future-projections)

This [script](https://colab.research.google.com/drive/1wtWUCm7JHHwhGZ8LdrrLcUJkkZsAXNDe), can help you generate the column names programatically. 


# Location columns
These columns are only added to your data if you analyzed your locations in the online tool. Users that download the entire dataset will not have these.  


| Column Name     | Data Type | Description |
|------------------|-------------|-----|
| **location_name** |(string) | the user-defined name for your location.| 
| **input_address** |(string) | a copy of the address as specified by the user. Only if using addresses as input file. |
| **match_address** |(string) | the address as matched by our geocode API. You can check if the match was succesful by comparing with the input_address. Only if using addresses as input file. |  
| **latitude** | (double) | location latitude (y) in decimal degres. Either specified by the user or derived from the geocoder API. |
| **longtitude** | (double)| location longitude (x) in decimal degrees. Either specified by the user or derived from the geocoder API. |
| **major_basin_name** | (string)| Name of the major river basin name. |
| **minor_basin_name** | (string) | Name of the minor river basin name. |
| **aquifer_name**| (string)| Name of the groundwater aquifer system. |


# Annual Baseline  

The columns in the Annual baseline results can be grouped into "identifiers", "indicators" and "grouped water risk"  

## Identifiers:  
| Column Name     | Data Type | Description |
|------------------|-------------|-----|
|**string_id**|(string)| contains a unique string for each geometry. Geometries are the union of hydrological basins, provinces and groundwater aquifers. The string_id is a combination of pfaf_id-gid_1-aqid. See the description of those columns.  |
|**aq30_id**|(integer)| unique identifier in numeric format.|  
|**pfaf_id**| (integer)| six digit Pfafstetter code for the hydrological basins.| 
|**gid_1**| (string)| identifier for sub-national units based on the [GADM](https://gadm.org/data.html) dataset. It contains the Iso A3 country code, followed by numeric values separated by underscores for each sub-national unit.|   
|**aqid**| (integer)| identifier for groundwater Aquifers based on WHYMAP.|
|**gid_0** | (string)| ISO A3 country code based on [GADM](https://gadm.org/data.html).|   
|**name_0**| (string)| National or political entity name based on [GADM](https://gadm.org/data.html).|    
|**name_1**| (string)| Sub-national or political entity name based on [GADM](https://gadm.org/data.html).|  
|**area_km2**| (double)| area of the geometry in km2 (union of sub-basin, province and groundwater aquifer).|  

## Indicators: 

For each of the 13 indicators the columns contain the indicator abbreviation plus the type {indicator}\_{type}, e.g.:  
"bws_raw" is baseline water stress, raw value. The indicator abbreviations and types are listed below.  

### Physical risk quantity: 
| Short    | Full |
|-------------|-----|
|**bws**| Baseline water stress|  
|**bwd**| Baseline water depletion|  
|**iav**| Interannual variability|  
|**sev**| Seasonal variability|  
|**gtd**| Groundwater table decline|  
|**rfr**| Riverine flood risk|  
|**cfr**| Coastal flood risk|  
|**drr**| Drought risk|

### Physical risk quality:
| Short    | Full |
|-------------|-----|
|**ucw**| Untreated connected wastewater|  
|**cep**| Coastal eutrophication potential|

### Regulatory and reputational risk:
| Short    | Full |
|-------------|-----|
|**udw**| Unimproved/no drinking water|    
|**usa**| Unimproved/no sanitation|  
|**rri**| Peak RepRisk ESG index|  

## Types:  
| Type   | Data Type | Description |
|------------------|-------------|-----|
|**\_raw**| (double) | raw value. Units depend on the indicator. See the technical note.|  
|**\_score**| (double) | each indicator is mapped to a [0-5] scale.|  
|**\_label**| (string) | A label explaining the category of the indicator including threshold. e.g. "Extremely High (more than 1 in 100)".|  
|**\_cat**| (integer) | integer for each category [-1,4], can be used for visuals.|  

## Grouped water risk

see the technical note for a description of aggregating the 13 indicators into sub-groups and an overall water risk score using the composite index approach. The grouped water risk scores use the follwing format:

w_awr_{weightingscheme}\_{group}\_{type}  

w_awr, stand for weighted aggregated water risk. Mainly used to keep them separate from the remaining indicators.    

e.g. w_awr_min_rrr_score is the aggregated score using the mining weighting scheme for the regulatory and reputational risk group.


### Weighting Scheme
| Short  | Full |
|-------------|-----|
|**def**| Default | 
|**agr**| Agriculture |  
|**che**| Chemicals  |
|**con**| Construction Materials  |
|**elp**| Electric Power  |
|**fnb**| Food & Beverage  |
|**min**| Mining  |
|**ong**| Oil & Gas |  
|**smc**| Semiconductor |  
|**tex**| Textile  |

### Groups
| Short  | Full |
|-------------|-----|
|**qan**| Physical risk quantity  |
|**qal**| Physical risk quality | 
|**rrr**| Regulatory and reputational risk |
|**tot**| Total, Overall water risk. |

### Types

| Type   | Data Type | Description |
|------------------|-------------|-----|
|**\_raw**| (double)| raw value on 0-5 scale. Result of weighted composite approach|  
|**\_score**| (double) | score [0-5], result of applying a quantile approach to raw values. See technical note |  
|**\_label**| (string) | A label explaining the category of the grouped water risk.|  
|**\_cat**| (integer)| integer for each category [-1,4], can be used for visuals.|  
|**\_weight_fraction**| (double)| the fraction [0-1] of the group towards the overall water risk score. NoData is excluded from the weights and therefore the fractions can be lower than 1 depending on data availability. See the technical note for the weights per industy and indicator. |

# Monthly Baseline

## Identifiers:  

**pfaf_id**, (integer), six digit Pfafstetter code for the hydrological basins.  
**month**, (integer), Month of the year.

## Indicators: 
**bws**, Baseline water stress,  
**bwd**, Baseline water depletion,  
**iav**, Interannual variability,  

## Types:  
**\_raw**, double, raw value. Units depend on the indicator. See the technical note.  
**\_score**, double, each indicator is mapped to a [0-5] scale.  
**\_label**, string, A label explaining the category of the indicator includin threshold. e.g. "Extremely High (more than 1 in 100)"  
**\_cat**, integer, integer for each category [-1,4], can be used for visuals.  

# Future Projections

There are four indicators, three target years, three scenarios, three data types	

## Identifiers  
**BasinID**, integer, Sub-basin identifiers.   
**dwnBasinID**, integer, Next downstream sub-basin.   
**Area_km2**, double, Area of sub-basin in square kilometer.  
**Shape_Leng**, double, Perimeter of the sub-basin in kilometer.  
	
## Indicators  
The indicators use the following format:  
{II}{YY}{SS}{R}{X}	 

II,	indicator code  
YY,	year code   
SS, scenario code    
T, data type code    
X, suffix    

### {II}	Indicator codes  
ws	water stress  
sv	seasonal variability  
ut	water demand  
bt	water supply  
	
### {YY}	Year codes  
20	2020  
30	2030  
40	2040  
	
### {SS}	Scenario codes  
24	ssp2 rcp45 (optimistic)  
28	ssp2 rcp85 (business as usual)  
38	ssp3 rcp85 (pessimistic)  
	
### {T}	Data types  
c	change from baseline  
t	future value  
u	uncertainty value  
	
### {X}	Suffixes  
l	label string  
r	raw value  
	
For example the layer {ws4028cl} is "projected change in water stress by the year 2040 under a business as usual (ssp2 rcp85) scenario"	 










