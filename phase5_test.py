import os
import xarray as xr
from download_ncss import download_ncss

variables = [
    "zg850", "zg700", "zg500",
    "ta850", "ta700", "ta500",
    "hus850", "hus700", "hus500",
    "ua850", "ua700", "ua500",
    "va850", "va700", "va500",
    "pr"
]

start_date = "1951-01-01"
end_date = "1951-01-07"
output_dir = r"D:\Doury2024_Data\raw"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(r"D:\Doury2024_Data\processed", exist_ok=True)
os.makedirs(r"D:\Doury2024_Data\test", exist_ok=True)

# 1. Download data
for var in variables:
    outfile = os.path.join(output_dir, f"{var}_{start_date.replace('-','')}-{end_date.replace('-','')}.nc")
    
    success = download_ncss(
        variable=var,
        start_date=start_date,
        end_date=end_date,
        north=57, west=-9, east=22, south=35,
        stride=1,
        output_filename=outfile
    )
    if not success:
        print(f"Failed to download {var} for Phase 5. Exiting.")
        exit(1)

# 2. Validate temporal consistency
print("\n--- Validating Temporal Consistency ---")
time_arrays = []
for var in variables:
    outfile = os.path.join(output_dir, f"{var}_{start_date.replace('-','')}-{end_date.replace('-','')}.nc")
    ds = xr.open_dataset(outfile)
    time_arrays.append(ds.time.values)

base_time = time_arrays[0]
for i, var in enumerate(variables):
    if not (time_arrays[i] == base_time).all():
        print(f"ERROR: Variable {var} has a time dimension mismatch!")
        exit(1)
    else:
        print(f"Variable {var}: time dimension matches ({len(base_time)} days).")

print("\nPhase 5 test completed successfully. Temporal consistency validated.")
