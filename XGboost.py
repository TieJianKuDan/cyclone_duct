import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score  

if __name__ == "__main__":
    dataset_path = "data/dataset.csv"
    dataset = pd.read_csv(dataset_path).sample(frac=1).dropna()
    train = dataset.head(6000)
    test = dataset.tail(1000)
    features = [x for x in train.columns if x not in ["sonde", "sid", "duct"]]
    train_f = np.array(train[features])
    train_l = np.array(train["duct"]).astype(int)
    dtrain = xgb.DMatrix(train_f, train_l)
    params = {
        "learn_rate": 0.05,
        "max_depth": 10,
        "n_estimators": 3000,
        "min_child_weight": 1,
        "reg_lamda": 1,
        "reg_alpha": 0.1,
        "subsample": 0.9,
        "colsample_bytree": 0.9,
        "gamma": 0,
        "silent": 1,
        "objective": "binary:logistic", 
        "eval_metric": "logloss",
        "nthread": 4,
        "num_class": 1
    }
    model = xgb.train(params, dtrain)

    test_f = np.array(test[features])
    test_l = np.array(test["duct"]).astype(int)
    dtest = xgb.DMatrix(test_f)
    preds = model.predict(dtest)
    preds_binary = [1 if i > 0.5 else 0 for i in preds]  
    
    accuracy = accuracy_score(test_l, preds_binary)  
    print("Accuracy: %.2f%%" % (accuracy * 100.0))