3!/usr/bin/env python3
"""
Export scaler and label_encoder from the training notebook.
This script extracts the scaler and label_encoder that were used during training.
"""

import pickle
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np

# Create model directory if it doesn't exist
os.makedirs('model', exist_ok=True)

# Create scaler with the same configuration used in training
# The scaler needs to be fitted on the same features
print("Creating feature scaler...")
scaler = StandardScaler()

# Note: Since we don't have the training data here, we'll create a placeholder
# You need to run this in your notebook where the actual scaler exists
# OR we can load from the deployment package if it contains the scaler

# For now, let's create the label encoder which we know the classes
print("Creating label encoder...")
label_encoder = LabelEncoder()
# The 7 tonic solfa notes in order
classes = np.array(['Do', 'Fa', 'La', 'Mi', 'Re', 'So', 'Ti'])
label_encoder.fit(classes)

# Save label encoder
with open('model/label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
print("✅ Label encoder saved to model/label_encoder.pkl")

# For the scaler, we need to get it from your notebook
# Let me create a cell you can add to your notebook instead
notebook_cell = """
# Add this cell to your Jupyter notebook and run it:

import pickle
import os

# Create model directory
os.makedirs('../model', exist_ok=True)

# Save the scaler (this already exists in your notebook)
with open('../model/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
    
print("✅ Scaler saved to ../model/scaler.pkl")
"""

print("\n" + "="*60)
print("⚠️  IMPORTANT: You need to export the scaler from your notebook!")
print("="*60)
print("\nOpen your Jupyter notebook and add this cell:\n")
print(notebook_cell)
print("\n" + "="*60)
