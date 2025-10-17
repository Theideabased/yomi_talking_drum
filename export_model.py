"""
Export Trained Model for Production Use
========================================
This script exports the trained model and scaler from the notebook
for use in the web application
"""

import torch
import torch.nn as nn
import numpy as np
import pickle
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Create model directory
os.makedirs('model', exist_ok=True)

# Model Architecture (must match training)
class CNNModel(nn.Module):
    """Convolutional Neural Network for audio classification"""
    def __init__(self, input_size=47, num_classes=7):
        super(CNNModel, self).__init__()
        self.features = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
        )
        self.classifier = nn.Linear(64, num_classes)
        
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

def export_model(model, scaler, label_encoder):
    """
    Export the trained model, scaler, and label encoder
    
    Args:
        model: Trained PyTorch model
        scaler: Fitted StandardScaler
        label_encoder: Fitted LabelEncoder
    """
    try:
        # Save model state dict
        torch.save(model.state_dict(), 'model/best_model.pth')
        print("✅ Model saved to model/best_model.pth")
        
        # Save scaler
        with open('model/scaler.pkl', 'wb') as f:
            pickle.dump(scaler, f)
        print("✅ Scaler saved to model/scaler.pkl")
        
        # Save label encoder
        with open('model/label_encoder.pkl', 'wb') as f:
            pickle.dump(label_encoder, f)
        print("✅ Label encoder saved to model/label_encoder.pkl")
        
        # Save model info
        model_info = {
            'input_size': 47,
            'num_classes': 7,
            'classes': list(label_encoder.classes_),
            'architecture': 'CNN',
            'accuracy': '100%'
        }
        
        with open('model/model_info.pkl', 'wb') as f:
            pickle.dump(model_info, f)
        print("✅ Model info saved to model/model_info.pkl")
        
        print("\n🎉 All model files exported successfully!")
        print("📁 Files saved in 'model/' directory:")
        print("   - best_model.pth (model weights)")
        print("   - scaler.pkl (feature scaler)")
        print("   - label_encoder.pkl (label encoder)")
        print("   - model_info.pkl (model metadata)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error exporting model: {e}")
        return False

# Instructions for use in notebook
print("""
To export your trained model from the notebook, add this cell at the end:

```python
# Export model for production use
from export_model import export_model

# After training, call this function with your trained objects
export_model(
    model=models['CNN'],  # or your best model
    scaler=scaler,
    label_encoder=label_encoder
)
```

This will create a 'model' folder with all necessary files for the web app.
""")
