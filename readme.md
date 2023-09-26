### XGboost application on predicting and analysing duct in tropical cyclone
This is a reproduction of Ref. [1] and we get a model with 78% accracy at last. The project includes the following contribution:

1. Crawl all the dropsonde data from aoml.noaa.gov ([download_raw.py](download_raw.py))

2. Qauality control to these data using Aspen ([QC_all_sondes.py](QC_all_sondes.py))

3. Label the processed data and make a dataset ([make_dataset.py](make_dataset.py))

4. Train a XGboost model with 78% accuracy ([XGboost.py](XGboost.py))

I have not tried larger datasets and parameter tuning yet. Since that, I believe the XGboost function can achieve an accuracy of more than 80% just as the Ref. [1] argued. At last, if you have any problems, please post them to issues. Thank you!

Tips: 

1. All excutable scripts is at root dir and libs folder contains manual wrapped functions.
2. Recommend using anaconda or miniconda to install the required package
3. You must install [ASPEN](https://www.eol.ucar.edu/software/aspen) and add it to your environment variables

[1] *Huang L, Zhao X, Liu Y, et al. Analysis of the Atmospheric Duct Existence Factors in Tropical Cyclones Based on the SHAP Interpretation of Extreme Gradient Boosting Predictions[J]. Remote Sensing, 2022, 14(16): 3952.*