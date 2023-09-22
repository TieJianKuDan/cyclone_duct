import libs.banner
import libs.tools as tools
import xarray as xr
import numpy as np

IBTrACS_path = "data/cyclones/IBTrACS.ALL.v04r00.nc"
cyclones = xr.open_dataset(IBTrACS_path)

sonde_path = "data/sondes/qc/HURR1_/g062839207QC.nc"
sonde = xr.open_dataset(sonde_path)

tools.find_cyclone(sonde, cyclones)