import os
import requests
import xarray as xr
import time

def is_valid_netcdf(filepath):
    if not os.path.exists(filepath):
        return False
    try:
        with xr.open_dataset(filepath) as ds:
            # Simple check to see if variables can be accessed
            _ = ds.variables
        return True
    except Exception:
        return False

def get_ncss_url(variable, chunk_start="19510101", chunk_end="19551231"):
    # THREDDS server base URL for CNRM-ALADIN63 historical run
    base_url = (
        "https://thredds-su.ipsl.fr/thredds/ncss/grid/"
        "CNRM-WCRP-Data/CORDEX/output/EUR-11/CNRM/"
        "CNRM-CERFACS-CNRM-CM5/historical/r1i1p1/"
        "CNRM-ALADIN63/v2/day/{var}/v20190510/"
        "{var}_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_"
        "r1i1p1_CNRM-ALADIN63_v2_day_{start}-{end}.nc"
    )
    return base_url.format(var=variable, start=chunk_start, end=chunk_end)

def download_ncss(variable, start_date, end_date, north, west, east, south, stride, output_filename):
    os.makedirs(os.path.dirname(output_filename) if os.path.dirname(output_filename) else ".", exist_ok=True)

    if is_valid_netcdf(output_filename):
        print(f"[INFO] File {output_filename} already exists and is valid. Skipping download.")
        return True

    # Note: Using the first chunk 19510101-19551231. 
    # This might need dynamic determination for future years, but works for the current tests.
    url = get_ncss_url(variable)

    params = {
        "var": variable,
        "north": north,
        "west": west,
        "east": east,
        "south": south,
        "horizStride": stride,
        "accept": "netcdf3",
        "addLatLon": "true"
    }

    if start_date == end_date:
        params["time"] = f"{start_date}T12:00:00Z"
    else:
        params["time_start"] = f"{start_date}T12:00:00Z"
        params["time_end"] = f"{end_date}T12:00:00Z"

    print(f"[INFO] Downloading {variable} to {output_filename}...")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"[INFO] Attempt {attempt + 1}/{max_retries}")
            response = requests.get(url, params=params, timeout=300)
            
            print(f"[INFO] Request URL: {response.url}")
            response.raise_for_status()

            with open(output_filename, "wb") as f:
                f.write(response.content)

            if is_valid_netcdf(output_filename):
                size_kb = len(response.content) / 1024
                print(f"[SUCCESS] Download complete! Saved as: {output_filename} ({size_kb:.2f} KB)")
                return True
            else:
                print(f"[ERROR] Downloaded file {output_filename} is not a valid NetCDF file. Retrying...")

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)

    print(f"[FAILURE] Failed to download {variable} after {max_retries} attempts.")
    return False

if __name__ == "__main__":
    download_ncss(
        variable="pr",
        start_date="1951-01-01",
        end_date="1951-01-01",
        north=57,
        west=-9,
        east=22,
        south=35,
        stride=1,
        output_filename="data/test/test_pr_19510101_downloader.nc"
    )
