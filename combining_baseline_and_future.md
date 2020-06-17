# Intro

In August 2019, we updated the Aqueduct Water Risk Atlas and Country Rankings tools. Part of the update involved improving our underlying hydrological models. In the August 2019 update, we ONLY updated the Baseline data and NOT the future projections data. The result is that the baseline and future projections data are inconsistent. This document provides guidance on how to use baseline and future projections data until we update the future projections data.

The update of the future projections is a bigger undertaking and is not expected anytime soon. If you like to know more about the status of the update or support us, please contact us directly (Aqueduct@wri.org).

# The problem:

Aqueduct&#39;s future projection data and the baseline use vastly different approaches. Please see the technical notes ([link1](https://www.wri.org/publication/aqueduct-30), [link2](https://www.wri.org/publication/aqueduct-water-stress-projections-decadal-projections-water-supply-and-demand-using)) for further details. The datasets use different geometries: [Global Drainage Basin Database](http://www.cger.nies.go.jp/db/gdbd/gdbd_index_e.html) for future projections versus [HydroBASINS](https://hydrosheds.org/) for the baseline.

# The solution:

User can still leverage our future projections dataset in combination with our baseline data for two selected indicators: Water stress and Seasonal Variability. The approach is described below.

Step 1:

Go to the Aqueduct [risk atlas tool](https://www.wri.org/applications/aqueduct/water-risk-atlas)

Step 2:

Import your locations, leaving the settings as is (baseline, annual). Follow the instructions on our tool to import your locations.

Step 3:

Export the baseline data as .csv file

Step 4:

In the online tool, change the settings to Future

Step 5:

Export the future data as .csv file

Step 6:

Open Excel and[import](https://support.office.com/en-us/article/import-or-export-text-txt-or-csv-files-5250ac4c-663c-47ce-937b-339e391393ba?omkt=en-US&amp;ui=en-US&amp;rs=en-US&amp;ad=US) both csv files using the import data function. Using the import function will prevent data loss.

Step 7:

Multiply the baseline water stress (bws\_raw) or seasonal variability (sev\_raw) with the &quot;change from baseline&quot; raw values from the future projections dataset. The metadata can be found [here](https://github.com/wri/aqueduct30_data_download/blob/master/metadata.md#future-projections). For instance, water stress in 2040 under a business as usual scenario would be: ws 40 28 c r

Step 8:

If you prefer a score rather than a raw value. Use the equations from the technical [note](https://wriorg.s3.amazonaws.com/s3fs-public/aqueduct-30-updated-decision-relevant-global-water-risk-indicators_1.pdf) to convert from raw value to score.

TODO: Add exact column names for the use in Excel.

Limitations:

Although we feel this approach works in many cases there are clear limitations. Bear in mind that the limitations of the underlying datasets still apply. The main limitation of this combination approach stems from the difference in basin delineation between the baseline and future projections datasets. The issue will predominantly affect the available water parameter that is used to calculate seasonal variability and water stress. Depending on the basin delineation, certain locations will share their water resources within the basin.
