import os
# Suppress TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from emulator_functions import Predictors, Target, wrapModel, launch_gpu

def main():
    print("--- Phase 8: End-to-End Test ---")
    
    # We will use CPU for testing as per instructions
    # launch_gpu is skipped or we just let TF default to CPU since CUDA is not present
    
    # 1. Prepare Predictors
    domain = 'ALP'
    domain_size = (22, 16)
    
    var0_nosfc1 = [
        'zg850', 'zg700', 'zg500',
        'ta850', 'ta700', 'ta500',
        'hus850', 'hus700', 'hus500',
        'ua850', 'ua700', 'ua500',
        'va850', 'va700', 'va500'
    ]
    
    filepath = r'D:\Doury2024_Data\processed\predictors_19510101-19510107.nc'
    filepath_ref = filepath # Using same file for ref since we only have 7 days
    ref_period = ['1951', '1951']
    filepath_forc = 'GHG_RCP85_withONE.csv'
    
    print("\nInitializing Predictors...")
    input_1 = Predictors(
        domain=domain,
        domain_size=domain_size,
        filepath=filepath,
        filepath_ref=filepath_ref,
        var_list=var0_nosfc1,
        stand=1,
        ref_period=ref_period,
        means='r',
        stds='r',
        aero_ext=False,
        filepath_forc=filepath_forc,
        opt_ghg='ONE',
        seas=True
    )
    
    print(f"2D Input Shape: {input_1.input2D.shape}")
    print(f"1D Input Shape: {input_1.input1D.shape}")
    
    # 2. Prepare Target
    print("\nInitializing Target...")
    target_var = 'pr'
    filepath_target = r'D:\Doury2024_Data\processed\target_pr_19510101-19510107.nc'
    
    target_1 = Target(
        target_var=target_var,
        filepath=filepath_target,
        filepath_grid=None
    )
    # The paper subtracts 273.16 for 'tas' (temperature), but for 'pr' it is not necessary.
    # We pass the raw values.
    target_values = target_1.target.values
    
    print(f"Target Shape: {target_values.shape}")
    
    # 3. Train Model (Small Test)
    print("\nRunning wrapModel for training test...")
    filepath_model = r'D:\Doury2024_Data\checkpoints\test_model_pr.keras'
    os.makedirs(r'D:\Doury2024_Data\checkpoints', exist_ok=True)
    
    # Remove existing model to force training
    if os.path.exists(filepath_model):
        os.remove(filepath_model)
        
    # We train with batch_size=2 and learning rate=0.0005
    amodel = wrapModel(
        inputIn=[input_1],
        targetIn=[target_values],
        target_var=target_var,
        filepath_model=filepath_model,
        filepath_grid=filepath_target, # target file has the grid
        filepath_gamma_param=None, # will fall back to mse
        batch_size=2,
        LR=0.0005
    )
    
    print("\n--- End-to-End Test Completed ---")

if __name__ == "__main__":
    main()
