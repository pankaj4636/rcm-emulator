import os
import glob
import xarray as xr
import numpy as np
from scipy.interpolate import griddata
import time

def regrid_variable(data_values, lat_2d, lon_2d, lat_1d, lon_1d):
    """
    Interpolate 2D data from a projected grid (with 2D lat/lon) 
    onto a regular 1D Cartesian lat/lon grid.
    """
    # Create meshgrid for target
    LON, LAT = np.meshgrid(lon_1d, lat_1d)
    
    # Flatten the source arrays
    points = np.column_stack((lon_2d.ravel(), lat_2d.ravel()))
    values = data_values.ravel()
    
    # Remove NaNs from source data before interpolation
    valid_mask = ~np.isnan(values)
    points = points[valid_mask]
    values = values[valid_mask]
    
    if len(values) == 0:
        return np.full(LON.shape, np.nan)
        
    # Interpolate
    grid_z = griddata(points, values, (LON, LAT), method='linear')
    
    # Fill remaining NaNs (e.g. outside convex hull) with nearest neighbor
    if np.any(np.isnan(grid_z)):
        grid_z_nearest = griddata(points, values, (LON, LAT), method='nearest')
        mask = np.isnan(grid_z)
        grid_z[mask] = grid_z_nearest[mask]
        
    return grid_z

def main():
    print("Preparing Doury Data...")
    raw_dir = r"D:\Doury2024_Data\raw"
    processed_dir = r"D:\Doury2024_Data\processed"
    os.makedirs(processed_dir, exist_ok=True)
    
    # Target regular grid definition for ALP domain
    # Domain ALP (22,16) limits: lon_b=-9, lon_e=22, lat_b=35, lat_e=57
    lon_new = np.linspace(-9, 22, 128)
    lat_new = np.linspace(35, 57, 128)
    
    predictors = [
        "zg850", "zg700", "zg500",
        "ta850", "ta700", "ta500",
        "hus850", "hus700", "hus500",
        "ua850", "ua700", "ua500",
        "va850", "va700", "va500"
    ]
    target_var = "pr"
    
    date_str = "19510101-19510107"
    
    # Process predictors
    ds_pred_list = []
    
    # Keep track of time coordinate
    time_coord = None
    
    for var in predictors:
        filepath = os.path.join(raw_dir, f"{var}_{date_str}.nc")
        print(f"Processing {var}...")
        ds = xr.open_dataset(filepath)
        
        if time_coord is None:
            time_coord = ds.time.values
            
        lat_2d = ds.lat.values
        lon_2d = ds.lon.values
        
        regridded_data = []
        for t in range(len(time_coord)):
            data_t = ds[var].values[t]
            grid_t = regrid_variable(data_t, lat_2d, lon_2d, lat_new, lon_new)
            regridded_data.append(grid_t)
            
        regridded_data = np.array(regridded_data)
        
        # Create DataArray
        da = xr.DataArray(
            regridded_data,
            coords=[time_coord, lat_new, lon_new],
            dims=["time", "lat", "lon"],
            name=var,
            attrs=ds[var].attrs
        )
        ds_pred_list.append(da)
        ds.close()
        
    ds_predictors = xr.merge(ds_pred_list)
    out_pred = os.path.join(processed_dir, f"predictors_{date_str}.nc")
    ds_predictors.to_netcdf(out_pred)
    print(f"Saved predictors to {out_pred}")
    
    # Process target
    print(f"Processing {target_var}...")
    filepath = os.path.join(raw_dir, f"{target_var}_{date_str}.nc")
    ds_tgt = xr.open_dataset(filepath)
    lat_2d = ds_tgt.lat.values
    lon_2d = ds_tgt.lon.values
    
    regridded_data_tgt = []
    for t in range(len(time_coord)):
        data_t = ds_tgt[target_var].values[t]
        grid_t = regrid_variable(data_t, lat_2d, lon_2d, lat_new, lon_new)
        regridded_data_tgt.append(grid_t)
        
    regridded_data_tgt = np.array(regridded_data_tgt)
    da_tgt = xr.DataArray(
        regridded_data_tgt,
        coords=[time_coord, lat_new, lon_new],
        dims=["time", "lat", "lon"],
        name=target_var,
        attrs=ds_tgt[target_var].attrs
    )
    
    ds_target = xr.Dataset({target_var: da_tgt})
    out_tgt = os.path.join(processed_dir, f"target_{target_var}_{date_str}.nc")
    ds_target.to_netcdf(out_tgt)
    print(f"Saved target to {out_tgt}")

if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"Data preparation completed in {time.time()-t0:.2f} seconds.")
