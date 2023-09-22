import libs.banner
import libs.tools as tools
import xarray as xr
import numpy as np
import pandas as pd

if __name__ == "__main__":
    IBTrACS_path = "data/cyclones/IBTrACS.ALL.v04r00.nc"
    cyclones = xr.open_dataset(IBTrACS_path)
    good_sondes = pd.read_csv("data/sondes/good_sondes.csv")
    dataset = {"sonde": [], "hr": [], "tem": [], "u_wind": [], "v_wind": [], "sid": [
    ], "sshs": [], "rmw": [], "quad": [], "dist": [], "duct": []}

    for i in range(0, len(good_sondes)):
        sonde_path = good_sondes["sonde_path"][i]
        sonde = xr.open_dataset(sonde_path)
        print(sonde_path)
        sid, sshs, rmw, quad, dist = tools.find_cyclone(sonde, cyclones)
        if type(sid) == str:
            dataset["sonde"].append(sonde_path)
            pres = sonde.reference_pres.data[0]
            temp = sonde.reference_tdry.data[0] + 273.15
            rh = sonde.reference_rh.data[0]
            u_winds = sonde.u_wind.data
            s = pd.Series(u_winds)
            u_wind = np.array(s.interpolate())[-1]
            v_winds = sonde.v_wind.data
            s = pd.Series(v_winds)
            v_wind = np.array(s.interpolate())[-1]
            dataset["hr"].append(tools.calc_q(pres, temp, rh))
            dataset["tem"].append(temp)
            dataset["u_wind"].append(u_wind)
            dataset["v_wind"].append(v_wind)
            dataset["sid"].append(sid)
            dataset["sshs"].append(sshs)
            dataset["rmw"].append(rmw)
            dataset["quad"].append(quad)
            dataset["dist"].append(dist)
            dataset["duct"].append(good_sondes["duct_type"][i])

    pd.DataFrame(dataset).to_csv("data/dataset.csv", index=False)
