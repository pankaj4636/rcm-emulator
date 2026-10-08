import xarray as xr
import numpy as np
import sys

def check_file(filepath):
    try:
        ds = xr.open_dataset(filepath)
    except Exception as e:
        print(f"Error opening file: {e}")
        sys.exit(1)

    print("--- Dataset Information ---")
    print(ds)
    
    print("\n--- Dimensions ---")
    for dim in ds.dims:
        print(f"{dim}: {ds.sizes[dim]}")
        
    print("\n--- Coordinates ---")
    for coord in ds.coords:
        print(f"{coord}: {ds[coord].values.shape}, min={np.min(ds[coord].values)}, max={np.max(ds[coord].values)}")

    print("\n--- Variables ---")
    for var in ds.data_vars:
        print(f"{var}: shape={ds[var].shape}, units={ds[var].attrs.get('units', 'N/A')}")
        data = ds[var].values
        print(f"  min: {np.nanmin(data)}")
        print(f"  max: {np.nanmax(data)}")
        print(f"  mean: {np.nanmean(data)}")
        print(f"  NaN count: {np.isnan(data).sum()}")

if __name__ == "__main__":
    check_file("test_pr_19510101.nc")
