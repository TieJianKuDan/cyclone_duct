# Make datasets for training
from datetime import datetime
import libs.banner
import libs.tools as tools
import xarray as xr
import numpy as np
import pandas as pd
import sys

if __name__ == "__main__":
    # Record log
    sys.stdout = tools.Logger(
        "logs/make_dataset_" + datetime.now().strftime(r"%Y_%m_%d_%H_%M_%S") + ".log")

    IBTrACS_path = "data/cyclones/IBTrACS.ALL.v04r00.nc"
    cyclones = xr.open_dataset(IBTrACS_path)
    good_sondes = pd.read_csv("data/sondes/good_sondes.csv")

    dataset = {"sonde": [], "hr": [], "temp": [], "u_wind": [], "v_wind": [], "sid": [
    ], "sshs": [], "rmw": [], "quad": [], "dist": [], "duct": []}

    for i in range(0, len(good_sondes)):
        sonde_path = good_sondes["sonde_path"][i]
        print(f"==> {sonde_path}")
        sonde = xr.open_dataset(sonde_path)
        sid, sshs, rmw, quad, dist = tools.find_cyclone(sonde, cyclones)
        if type(sid) == str:
            dataset["sonde"].append(sonde_path)
            if not np.isnan(sonde.reference_pres.data[0]):
                pres = sonde.reference_pres.data[0]
            else:
                pres = np.array(pd.Series(sonde.pres.data).interpolate())[-1]

            if not np.isnan(sonde.reference_tdry.data[0]):
                temp = sonde.reference_tdry.data[0] + 273.15
            else:
                temp = np.array(
                    pd.Series(sonde.tdry.data).interpolate())[-1] + 273.15
            if not np.isnan(sonde.reference_rh.data[0]):
                rh = sonde.reference_rh.data[0]
            else:
                rh = np.array(pd.Series(sonde.rh.data).interpolate())[-1]
            u_wind = np.array(pd.Series(sonde.u_wind.data).interpolate())[-1]
            v_wind = np.array(pd.Series(sonde.v_wind.data).interpolate())[-1]
            dataset["hr"].append(tools.calc_q(pres, temp, rh))
            dataset["temp"].append(temp)
            dataset["u_wind"].append(u_wind)
            dataset["v_wind"].append(v_wind)
            dataset["sid"].append(sid)
            dataset["sshs"].append(sshs)
            dataset["rmw"].append(rmw)
            dataset["quad"].append(quad)
            dataset["dist"].append(dist)
            dataset["duct"].append(good_sondes["is_duct"][i])

    pd.DataFrame(dataset).to_csv("data/dataset.csv", index=False)
