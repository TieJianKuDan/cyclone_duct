### XGboost application on predicting and analysing duct in tropical cyclone
This is a reproduction of Ref. [1] and we get a model with 78% accracy at last. The project includes the following contribution:

1. Crawl all the dropsonde data from aoml.noaa.gov
2. Qauality control to these data using Aspen
3. Label the processed data and make a dataset
4. Train a XGboost model with 78% accuracy

I have not tried larger datasets and parameter tuning yet. Since that, I believe the XGboost function can achieve an accuracy of more than 80% just as the Ref. 1 argued. At last, if you have any problems, please post them to issues. Thank you!

[1] *Huang L, Zhao X, Liu Y, et al. Analysis of the Atmospheric Duct Existence Factors in Tropical Cyclones Based on the SHAP Interpretation of Extreme Gradient Boosting Predictions[J]. Remote Sensing, 2022, 14(16): 3952.*