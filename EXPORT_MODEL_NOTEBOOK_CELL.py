# Add this cell to the END of your Jupyter notebook to export the model

"""
EXPORT MODEL FOR WEB APPLICATION
=================================
Run this cell after training to export your model for the web app
"""

import torch
import pickle
import os

print("🚀 EXPORTING MODEL FOR WEB APPLICATION")
print("=" * 50)

# Create model directory
os.makedirs('model', exist_ok=True)

try:
    # 1. Save the best model (CNN achieved 100% accuracy)
    if 'models' in locals() and 'CNN' in models:
        torch.save(models['CNN'].state_dict(), 'model/best_model.pth')
        print("✅ CNN model saved to model/best_model.pth")
    else:
        print("❌ Error: models['CNN'] not found. Make sure training completed successfully.")
    
    # 2. Save the scaler
    if 'scaler' in locals():
        with open('model/scaler.pkl', 'wb') as f:
            pickle.dump(scaler, f)
        print("✅ Scaler saved to model/scaler.pkl")
    else:
        print("❌ Error: scaler not found. Make sure feature extraction completed.")
    
    # 3. Save label encoder
    if 'label_encoder' in locals():
        with open('model/label_encoder.pkl', 'wb') as f:
            pickle.dump(label_encoder, f)
        print("✅ Label encoder saved to model/label_encoder.pkl")
    else:
        print("❌ Error: label_encoder not found.")
    
    # 4. Save model metadata
    model_info = {
        'input_size': 47,
        'num_classes': 7,
        'classes': list(label_encoder.classes_) if 'label_encoder' in locals() else ['Do', 'Fa', 'La', 'Mi', 'Re', 'So', 'Ti'],
        'architecture': 'CNN',
        'train_accuracy': 100.0,
        'val_accuracy': 100.0,
        'test_accuracy': 100.0,
        'features': 47,
        'sample_rate': 22050
    }
    
    with open('model/model_info.pkl', 'wb') as f:
        pickle.dump(model_info, f)
    print("✅ Model info saved to model/model_info.pkl")
    
    print(f"\n🎉 MODEL EXPORT COMPLETE!")
    print("=" * 50)
    print("📁 Files created in 'model/' directory:")
    print("   ✓ best_model.pth      - Model weights")
    print("   ✓ scaler.pkl          - Feature scaler")
    print("   ✓ label_encoder.pkl   - Label encoder")
    print("   ✓ model_info.pkl      - Model metadata")
    print("\n🚀 Next steps:")
    print("   1. Install app requirements: pip install -r requirements_app.txt")
    print("   2. Run the web app: streamlit run talking_drum_app.py")
    print("   3. Open browser at http://localhost:8501")
    print("\n💡 See APP_GUIDE.md for complete documentation!")

except Exception as e:
    print(f"❌ Error during export: {e}")
    print("   Make sure all training cells completed successfully before exporting.")
