import os
# Suppress TensorFlow logging for clean output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from emulator_functions import Predictors

# Target domain settings
domain = 'ALP'
domain_size = (22, 16)

# The list of 15 predictor variables
var0_nosfc1 = [
    'zg850', 'zg700', 'zg500',
    'ta850', 'ta700', 'ta500',
    'hus850', 'hus700', 'hus500',
    'ua850', 'ua700', 'ua500',
    'va850', 'va700', 'va500'
]

# Provided files
filepath = 'X_EUC12_fullvar_smth3_aero_2000-01-01.nc'
filepath_forc = 'GHG_RCP85_withONE.csv'

# NOTE: A proper climatological reference NetCDF file (e.g. 1971-2000) is physically missing 
# from the repository. We use the sample NetCDF as the reference file and restrict the 
# reference period to '2000' to prevent FileNotFoundError and Index errors. 
filepath_ref = filepath
ref_period = ['2000', '2000']

print("Initializing Predictors class and running data processing...")
pred = Predictors(
    domain=domain,
    domain_size=domain_size,
    var_list=var0_nosfc1,
    filepath=filepath,
    filepath_ref=filepath_ref,
    stand=1,
    ref_period=ref_period,
    means='r',       # Set to 'r' (raw) to avoid divide-by-zero since our ref period is too short
    stds='r',        # Set to 'r' (raw) to avoid divide-by-zero
    aero_ext=False,  # Exclude external aerosols since we only have the sample NC file
    filepath_forc=filepath_forc,
    opt_ghg='ONE',
    seas=True
)

print("\n--- Predictors Shape Results ---")
print(f"2D Input Shape generated: {pred.input2D.shape}")
print(f"1D Input Shape generated: {pred.input1D.shape}")
print(f"Number of 2D Features: {len(var0_nosfc1)}")
print(f"Variables used: {var0_nosfc1}")
print("Test completed successfully!")
