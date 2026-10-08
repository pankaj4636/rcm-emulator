# Data Pipeline Notes

## Phase 4: Doury Repository Expectations

### Expected Variable Names
- 3D variables at specific pressure levels: `zg850, zg700, zg500`, `ta850, ta700, ta500`, `hus850, hus700, hus500`, `ua850, ua700, ua500`, `va850, va700, va500`.
- Surface variable: `pr`.

### Expected Dimensions & Coordinate System
- The repository's `emulator_functions.py` `Predictors` and `Target` classes expect files to have `lon` and `lat` as 1D coordinate dimensions. 
- Slicing relies on `xarray.Dataset.sel(lon=slice(...), lat=slice(...))`.
- The downloaded NCSS data for the CNRM-ALADIN63 model is on a projected Lambert Conformal grid with 1D `x` and `y` coordinates and a `Lambert_Conformal` mapping variable. 

### Decision on "Add 2D Lat/Lon to file"
- If we enable the NCSS `addLatLon=true` parameter, the THREDDS server adds `lat` and `lon` as 2D variables.
- However, `xarray`'s `.sel()` function does not natively support slicing over 2D coordinate variables using `slice()`. 
- **Decision**: We should NOT rely solely on `addLatLon=true` to satisfy the repository's `.sel(lon=..., lat=...)` requirement. Instead, the preprocessing pipeline (`prepare_doury_data.py`) must regrid the downloaded `x`/`y` (Lambert Conformal) variables onto a regular `lon`/`lat` grid matching the spatial domain expected by the U-Net. 

### Expected File Organization & Normalization
- All 2D predictors for a given period are expected to be in a single NetCDF file (with dimensions `time`, `lat`, `lon`), which is passed to the `Predictors` class via `filepath`.
- A reference file `filepath_ref` (often the same grid) is used to compute reference means and std deviations for standardization (`stand=1` or `stand=2`).
- The 1D predictors (GHG, Solar, Ozone, Season) are derived from a `.csv` file (`GHG_RCP85_withONE.csv`), aligned with the `time` coordinate of the predictor NetCDF.
- Normalization (Standardization) is handled internally by the `Predictors` class using `np.nanmean` and `np.nanstd` for `stand=1`.
- However, for the 1D appended features, `INPUT_2D.mean(axis=(1,2))` is used in `Predictors.make`. If the input contains NaNs (e.g., pressure levels below topography like `ta850` in the Alps), `numpy.mean` will produce `NaN`. 

### Expected Domains
- The `Domain` class handles spatial subsets. For `ALP` with `domain_size=(22, 16)`, the limits are: `lon_b=-9, lon_e=22, lat_b=35, lat_e=57`.
- The preprocessing step needs to produce a grid that covers this domain with regular `lat` and `lon` 1D coordinates so that `Domain.applyDom` works correctly.

### Temporal Format
- Daily data (`day`).
- Leap days (February 29th) are explicitly removed in `Predictors.make` and `Target.__init__`. 

### Preprocessing Strategy
1. Download all required variables using NCSS (`download_ncss.py`).
2. Merge them into a single dataset.
3. Regrid the dataset from Lambert Conformal (`x`, `y`) to a regular `lon`/`lat` Cartesian grid.
4. Fill or handle NaNs (e.g., using interpolation or keeping them as is, but we might need to modify `INPUT_2D.mean` to `INPUT_2D.nanmean` or fill NaNs before `Predictors` initialization to avoid NaN collapse in the 1D features).
5. Save the combined, regridded dataset for use with `emulator_functions.py`.
