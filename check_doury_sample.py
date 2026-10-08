import xarray as xr

ds = xr.open_dataset('X_EUC12_fullvar_smth3_aero_2000-01-01.nc')
print("--- Sample file X_EUC12 ---")
print("Dims:", ds.dims)
print("Coords:", ds.coords.keys())
if 'lon' in ds.coords:
    print("lon shape:", ds['lon'].shape, "dims:", ds['lon'].dims)
if 'lat' in ds.coords:
    print("lat shape:", ds['lat'].shape, "dims:", ds['lat'].dims)
if 'x' in ds.coords:
    print("x shape:", ds['x'].shape)
print("Data vars:", list(ds.data_vars.keys())[:10]) # list first 10
