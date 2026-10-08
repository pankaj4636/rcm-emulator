import requests

url = (
    "https://thredds-su.ipsl.fr/thredds/ncss/grid/"
    "CNRM-WCRP-Data/CORDEX/output/EUR-11/CNRM/"
    "CNRM-CERFACS-CNRM-CM5/historical/r1i1p1/"
    "CNRM-ALADIN63/v2/day/pr/v20190510/"
    "pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_"
    "r1i1p1_CNRM-ALADIN63_v2_day_19510101-19551231.nc"
)

params = {
    "var": "pr",
    "north": 57,
    "west": -9,
    "east": 22,
    "south": 35,
    "horizStride": 1,
    "time": "1951-01-01T12:00:00Z",
    "accept": "netcdf3"
}

output_file = "test_pr_19510101.nc"

print("Downloading precipitation subset...")

response = requests.get(url, params=params, timeout=300)

response.raise_for_status()

with open(output_file, "wb") as f:
    f.write(response.content)

print("Download complete!")
print("Saved as:", output_file)
print("Size:", len(response.content) / 1024, "KB")