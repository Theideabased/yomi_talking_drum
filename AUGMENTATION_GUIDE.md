# Talking Drum Dataset Augmentation - Usage Guide

This standalone script augments your talking drum dataset by creating 150 variations per note while preserving cultural authenticity.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_augmentation.txt
```

### 2. Run Full Dataset Augmentation
```bash
python dataset_augmentation.py
```

### 3. Check Results
The augmented dataset will be saved to `augmented_talking_drum_dataset/` folder.

## Advanced Usage

### Custom Input/Output Paths
```bash
python dataset_augmentation.py --input /path/to/your/dataset --output /path/to/augmented/dataset
```

### Change Target Sample Count
```bash
python dataset_augmentation.py --target 200  # Creates 200 samples per note
```

### Process Single Note
```bash
python dataset_augmentation.py --note Do  # Only process "Do" folder
```

### Quiet Mode (Minimal Output)
```bash
python dataset_augmentation.py --quiet
```

### Help
```bash
python dataset_augmentation.py --help
```

## Expected Results

For your current dataset:
- **Do folder**: 2 files → 150 total samples (148 augmented)
- **Re folder**: 1 file → 150 total samples (149 augmented)
- **Mi, Fa, So, La, Ti folders**: Similar expansion to 150 samples each

## Augmentation Types Applied

1. **Time Stretching** (±25% tempo variation)
2. **Volume Changes** (±8dB variation)  
3. **Frequency Filtering** (EQ adjustments)
4. **Noise Addition** (Pink, brown, vinyl, tape hiss, room tone)
5. **Reverb Simulation** (Different acoustic spaces)
6. **Subtle Pitch Shifting** (±0.5 semitones - very careful)
7. **Dynamic Compression** (Varying dynamics)

## File Structure

```
augmented_talking_drum_dataset/
├── Do/
│   ├── original_Do_amp.mp3      # Original file (copied)
│   ├── original_Do-up.mp3       # Original file (copied)
│   ├── Do_amp_aug_00_001.wav    # Augmented variation
│   ├── Do_amp_aug_00_002.wav    # Augmented variation
│   └── ...                      # Up to 150 total files
├── Re/
│   ├── original_Re.mp3          # Original file (copied)
│   ├── Re_aug_00_001.wav        # Augmented variation
│   └── ...                      # Up to 150 total files
└── ... (Mi, Fa, So, La, Ti)
```

## Cultural Sensitivity Features

- ✅ Preserves fundamental frequency relationships
- ✅ Maintains traditional attack/decay patterns
- ✅ Never alters musical note identity
- ✅ Respects cultural significance of each sound
- ✅ Only applies subtle, realistic variations

## Performance

- Processes ~10-20 files per minute (depending on file size)
- Uses efficient audio processing libraries
- Progress bars show real-time status
- Memory-efficient processing

## Troubleshooting

### Common Issues:

1. **"No audio files found"**: Ensure your dataset has .mp3, .wav, .m4a, or .aac files
2. **"Dataset not found"**: Check the input path is correct
3. **Memory errors**: Try processing one note at a time with `--note`
4. **Audio loading errors**: Some file formats may need conversion

### Support

If you encounter issues, check:
1. File permissions on input/output directories
2. Available disk space for augmented files
3. Audio file formats are supported
4. All dependencies are installed correctly
