# Judge whether is atmospheric duct in somewhere
import libs.banner
import libs.tools as tools
import xarray as xr
import os
import pandas as pd
import sys
from datetime import datetime

if __name__ == "__main__":
    # Record log
    sys.stdout = tools.Logger(
        "logs/judge_duct_" + datetime.now().strftime(r"%Y_%m_%d_%H_%M_%S") + ".log")

    folder_path = "data/sondes/qc/HURR1_/"
    sondes = {"sonde_path": [], "is_duct": [], "duct_type": []}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".nc"):
                sonde_path = os.path.join(root, file)
                sonde = xr.open_dataset(sonde_path)
                is_duct, duct_type = tools.is_duct(sonde, False)
                print(f"{sonde_path}==>({is_duct}, {duct_type})")
                if duct_type != "error":
                    sondes["sonde_path"].append(sonde_path)
                    sondes["is_duct"].append(is_duct)
                    sondes["duct_type"].append(duct_type)
    df = pd.DataFrame(sondes)
    print(df)
    df.to_csv("data/sondes/good_sondes.csv", index=False)
