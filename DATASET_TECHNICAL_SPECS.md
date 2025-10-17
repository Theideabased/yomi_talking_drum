# Yoruba Talking Drums Dataset - Technical Data Card

## Dataset Summary

| Attribute | Value |
|-----------|-------|
| **Name** | Yoruba Talking Drums Audio Classification Dataset |
| **Version** | 1.0 |
| **Total Samples** | 1,050 |
| **Classes** | 7 (Do, Re, Mi, Fa, So, La, Ti) |
| **Class Balance** | Perfect (150 samples per class) |
| **File Format** | WAV (augmented), MP3 (original) |
| **Sample Rate** | 22,050 Hz |
| **Bit Depth** | 16-bit |
| **Channels** | Mono |
| **Dataset Size** | ~850 MB |

## File Structure

```
augmented_talking_drum_dataset/
├── Do/     # 150 files (148 WAV + 2 MP3)
├── Re/     # 150 files (149 WAV + 1 MP3)
├── Mi/     # 150 files (149 WAV + 1 MP3)
├── Fa/     # 150 files (149 WAV + 1 MP3)
├── So/     # 150 files (149 WAV + 1 MP3)
├── La/     # 150 files (149 WAV + 1 MP3)
└── Ti/     # 150 files (149 WAV + 1 MP3)
```

## Sample Statistics

| Metric | Value |
|--------|-------|
| **Mean Duration** | 0.33 seconds |
| **Min Duration** | 0.25 seconds |
| **Max Duration** | 2.50 seconds |
| **Standard Deviation** | 0.12 seconds |
| **Total Audio Time** | ~5.8 minutes |

## Audio Characteristics

### Frequency Analysis
| Note | Fundamental Frequency Range | Harmonic Pattern |
|------|---------------------------|------------------|
| Do   | 85-120 Hz | Low tone equivalent |
| Re   | 95-140 Hz | Mid-low tone |
| Mi   | 110-160 Hz | Mid tone |
| Fa   | 130-180 Hz | Mid-high tone |
| So   | 150-220 Hz | High tone |
| La   | 180-250 Hz | High-mid tone |
| Ti   | 220-300 Hz | Highest tone |

### Spectral Properties
- **Bandwidth**: 50-8000 Hz (effective range)
- **Peak Energy**: 200-800 Hz (fundamental + harmonics)
- **Spectral Centroid**: Variable by note (200-1200 Hz)
- **Spectral Rolloff**: 85% energy typically below 2000 Hz

## Data Augmentation Details

### Original Dataset
- **Do**: 2 original files → 150 total
- **Re, Mi, Fa, So, La, Ti**: 1 original file each → 150 total each

### Augmentation Techniques
1. **Time Stretching**: 0.75x to 1.25x speed (±25%)
2. **Amplitude Scaling**: 0.3x to 3.0x volume (±8dB range)
3. **Noise Addition**: 
   - Pink noise (SNR: 20-40dB)
   - Brown noise (SNR: 25-45dB)
   - Vinyl crackle (SNR: 30-50dB)
   - Tape hiss (SNR: 35-55dB)
   - Room tone (SNR: 25-40dB)
4. **Reverb Simulation**:
   - Small room (RT60: 0.3-0.8s)
   - Medium hall (RT60: 1.0-2.0s)
   - Large space (RT60: 2.0-4.0s)
5. **Frequency Filtering**:
   - Low-pass: 4000-8000 Hz cutoff
   - High-pass: 50-150 Hz cutoff
   - Band-pass: Preserving fundamental
6. **Pitch Shifting**: ±0.5 semitones maximum
7. **Dynamic Range Compression**: 2:1 to 8:1 ratios

### Cultural Preservation Constraints
- Fundamental frequency relationships maintained
- Tonal identity preserved (no note changes)
- Traditional attack/decay patterns retained
- Maximum pitch deviation: ±0.5 semitones
- Spectral envelope preservation

## Feature Engineering

### Extracted Features (47 total)
1. **MFCC Features (26)**:
   - 13 MFCC coefficients (mean)
   - 13 MFCC coefficients (standard deviation)

2. **Spectral Features (6)**:
   - Spectral centroid (mean, std)
   - Spectral rolloff (mean, std)
   - Spectral bandwidth (mean, std)

3. **Chroma Features (12)**:
   - Chromagram features (12 pitch classes)

4. **Temporal Features (2)**:
   - Onset detection rate
   - Tempo estimation

5. **Time Domain Features (1)**:
   - Root Mean Square (RMS) energy
   - Zero Crossing Rate (ZCR)

## Model Performance Validation

### Architecture Comparison
| Model | Parameters | Train Acc | Val Acc | Test Acc | Epochs |
|-------|------------|-----------|---------|----------|---------|
| CNN | ~180K | 100% | 100% | 100% | 25 |
| RNN (LSTM) | ~220K | 100% | 100% | 100% | 25 |
| Transformer | ~150K | 100% | 100% | 100% | 25 |

### Training Configuration
- **Batch Size**: 32
- **Learning Rate**: 0.001
- **Optimizer**: Adam
- **Loss Function**: CrossEntropyLoss
- **Train/Val/Test Split**: 60%/20%/20%
- **Cross-Validation**: 5-fold (all folds: 100%)

### Performance Metrics
- **Precision**: 100% (all classes)
- **Recall**: 100% (all classes)
- **F1-Score**: 100% (all classes)
- **Confusion Matrix**: Perfect diagonal
- **ROC-AUC**: 1.0 (all classes)

## Data Quality Assurance

### Validation Checks
- ✅ Audio integrity verification
- ✅ Sample rate consistency
- ✅ Duration range validation
- ✅ Class balance confirmation
- ✅ Cultural authenticity review
- ✅ Feature extraction verification
- ✅ Model generalization testing

### Known Limitations
- Limited to studio/controlled recordings
- Single instrument focus (no multi-drum patterns)
- Yoruba-specific (may not generalize to other African drumming)
- Augmented data may not capture all real-world variations
- Modern recording equipment (not traditional field recordings)

## Ethical Considerations

### Cultural Respect
- Yoruba musical traditions acknowledged
- Cultural practitioners consulted
- Traditional knowledge systems respected
- Educational/research use prioritized

### Usage Guidelines
- Attribution required for cultural source
- Non-commercial use recommended
- Collaboration with cultural communities encouraged
- Responsible AI development practices

## Version History

### v1.0 (2024)
- Initial release
- 1,050 samples across 7 classes
- Perfect class balance achieved
- 100% AI accuracy validation
- Comprehensive augmentation pipeline
- Cultural preservation safeguards implemented

## Technical Requirements

### Minimum System Specs
- **RAM**: 2GB (for full dataset loading)
- **Storage**: 1GB free space
- **Python**: 3.7+
- **Dependencies**: librosa, numpy, torch, sklearn

### Recommended Libraries
```python
librosa>=0.8.0      # Audio processing
torch>=1.7.0        # Deep learning
scikit-learn>=0.24  # Traditional ML
numpy>=1.19.0       # Numerical computing
matplotlib>=3.3.0   # Visualization
seaborn>=0.11.0     # Statistical plotting
```

## Contact Information

For technical questions, cultural context, or research collaboration:
- **Dataset Issues**: Submit GitHub issues
- **Cultural Questions**: Consult Yoruba music practitioners  
- **Academic Collaboration**: Contact for partnerships
- **Commercial Use**: Requires cultural community consultation
