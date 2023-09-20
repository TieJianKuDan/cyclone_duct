# Judge whether is atmospheric duct in somewhere
import libs.tools as tools
import xarray as xr

if __name__ == "__main__":
    sonde_path = "data/sondes/raw/HURR19/20190710H1/g182530336QC.nc"
    sonde = xr.open_dataset(sonde_path)
    is_duct, duct_type = tools.is_duct(sonde, True)
    print((is_duct, duct_type))
    