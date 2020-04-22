# Additional datasets

In addition to the data shared on our website under Creative Commons 4.0 SA license, we have various other datasets. 
These other datasets are currently not shared with the exception of Aqueducut Alliance or Data Partners members. This page contains the metadata of selected datasets. 

## PCR-GLOBWB data

### Auxiliary data

#### Local Drainage Direction
Spatial range: global  
Spatial resolution: 5 arc minutes (underlying DEM 3 arc seconds)  
Temporal range: Snapshot based on SRTM
Temporal resolution: N/a
Data types: GeoTIFF  
Description:  
Predominant drainage direction of surface water. 

#### Flow accumulation
Spatial range: global  
Spatial resolution: 5 arc minutes (underlying DEM 3 arc seconds)  
Temporal range: Snapshot based on SRTM
Temporal resolution: N/a
Data types: GeoTIFF  
Description:  
Number of upstream gridcells. 

### water withdrawal

#### Gridded
Spatial range: global  
Spatial resolution: 5 arc minutes  
Temporal range: 1960-2014  
Temporal resolution: monthly and annual  
Data types: NETCDF, GeoTIFF, Earth Engine ImageCollection  
Description: See the [technical note](https://www.wri.org/publication/aqueduct-30) for an overview of the PCR-GLOBWB. Water withdrawal data is available for two types of withdrawal: total withdrawal or consumptive withdrawal. Total withdrawal is simply consumptive withdrawal plus non-consumptive withdrawal. The data is available for four sectors:  
1. livestock
1. irrigated agriculture
1. industry
1. domestic

#### Vector | Tabular
Spatial range: global  
Spatial resolution: HydroBASINS level 6 
Temporal range: 1960-2014  
Temporal resolution: monthly and annual
Data types: Tabular: .csv, Google BigQuery and PostgreSQL. Geometry: Geopackage

Same data as the gridded water withdrawal aggregated to HydroBASINS level 6. See the [technical note](https://www.wri.org/publication/aqueduct-30) for the methodology. In addition to the monthly or annual values, we've calculated certain statistical parameters including simple regressions.


### water supply
Spatial range: global  
Spatial resolution: 5 arc minutes  
Temporal range: 1960-2014  
Temporal resolution: monthly and annual  
Data types: NETCDF, GeoTIFF, Earth Engine ImageCollection  
Description: See the [technical note](https://www.wri.org/publication/aqueduct-30) for an overview of the PCR-GLOBWB. Water withdrawal data is available for two types of withdrawal: total withdrawal or consumptive withdrawal. Total withdrawal is simply consumptive withdrawal plus non-consumptive withdrawal. The data is available for four sectors:  
1. livestock
1. irrigated agriculture
1. industry
1. domestic





