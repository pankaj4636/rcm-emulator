import xarray as xr
import numpy as np
import os
from download_ncss import download_ncss

variables = [
    "zg850", "zg700", "zg500",
    "ta850", "ta700", "ta500",
    "hus850", "hus700", "hus500",
    "ua850", "ua700", "ua500",
    "va850", "va700", "va500",
    "pr"
]

date = "1951-01-01"
output_dir = "data/test"
os.makedirs(output_dir, exist_ok=True)

# Phase 3 download and inspect
for var in variables:
    outfile = os.path.join(output_dir, f"test_{var}_{date.replace('-','')}.nc")
    
    # Download
    success = download_ncss(
        variable=var,
        start_date=date,
        end_date=date,
        north=57, west=-9, east=22, south=35,
        stride=1,
        output_filename=outfile
    )
    
    if not success:
        print(f"Failed to download {var}. Stopping pipeline.")
        exit(1)

    # Inspect
    try:
        ds = xr.open_dataset(outfile)
        if var in ds.data_vars:
            data_var = ds[var]
        else:
            print(f"Variable {var} not found in {outfile}. Available vars: {list(ds.data_vars.keys())}")
            continue

        data = data_var.values
        print(f"\n--- Report for {var} ---")
        print(f"variable: {var}")
        print(f"shape: {data.shape}")
        print(f"dimensions: {data_var.dims}")
        print(f"units: {data_var.attrs.get('units', 'N/A')}")
        print(f"min: {np.nanmin(data)}")
        print(f"max: {np.nanmax(data)}")
        print(f"mean: {np.nanmean(data)}")
        print(f"NaN count: {np.isnan(data).sum()}")
    except Exception as e:
        print(f"Failed to inspect {var} in {outfile}: {e}")
        exit(1)
