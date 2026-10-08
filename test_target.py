import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from emulator_functions import Target

filepath = 'X_EUC12_fullvar_smth3_aero_2000-01-01.nc'

print("Initializing Target class...")

target = Target(
    target_var='pr',
    filepath=filepath
)

print("\n--- Target Results ---")
print("Target shape:", target.target.shape)
print("Latitude shape:", target.lat.shape)
print("Longitude shape:", target.lon.shape)
print("Y shape:", target.y.shape)
print("X shape:", target.x.shape)

print("\nTarget variable:")
print(target.target)

print("\nTarget test completed successfully!")