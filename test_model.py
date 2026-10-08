import os
# Suppress TensorFlow logging for clean output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
from emulator_functions import wrapModel

# We bypass the __init__ of wrapModel since it expects full data objects and starts training
model_wrapper = wrapModel.__new__(wrapModel)

# Create the smallest valid parameters for the model
nb_inputs = 2
size_target_domain = 4 # Target domain size of 4x4
shape_inputs = [(4, 4, 3), (1, 1, 2)] # 2D branch: 4x4 spatial with 3 features; 1D branch: 1x1 with 2 global features
filters = 8

print("Building the U-Net model...")
model = model_wrapper.unet_maker(
    nb_inputs=nb_inputs, 
    size_target_domain=size_target_domain, 
    shape_inputs=shape_inputs, 
    filters=filters
)

print("\nModel Summary:")
model.summary()

# Create random dummy data for a forward pass
batch_size = 2
input_2d_shape = (batch_size,) + shape_inputs[0] # (2, 4, 4, 3)
input_1d_shape = (batch_size,) + shape_inputs[1] # (2, 1, 1, 2)

input_2d_data = np.random.rand(*input_2d_shape).astype(np.float32)
input_1d_data = np.random.rand(*input_1d_shape).astype(np.float32)

print("\n--- Forward Pass Test ---")
print(f"2D Input Shape generated: {input_2d_data.shape}")
print(f"1D Input Shape generated: {input_1d_data.shape}")

print("Running model.predict()...")
output = model.predict([input_2d_data, input_1d_data], verbose=0)

print(f"Prediction Output Shape: {output.shape}")
print("Test completed successfully!")
