#!/usr/bin/env python3
"""
Talking Drum Dataset Augmentation System

This script multiplies your talking drum dataset by creating culturally-sensitive
audio variations while preserving the fundamental characteristics of each musical note.

Author: AI Assistant
Date: September 9, 2025
Purpose: Expand talking drum dataset from original files to 150 samples per note
"""

import os
import librosa
import soundfile as sf
import numpy as np
from scipy.signal import butter, filtfilt, hilbert
from scipy.io import wavfile
import random
from pathlib import Path
import shutil
import argparse
import time
from tqdm import tqdm

class TalkingDrumAugmentationSystem:
    """
    Advanced audio augmentation system for talking drum dataset multiplication
    Preserves cultural and musical authenticity while creating training variations
    """
    
    def __init__(self, dataset_path, output_path=None, target_samples_per_note=150):
        self.dataset_path = Path(dataset_path)
        self.output_path = Path(output_path) if output_path else self.dataset_path.parent / "augmented_talking_drum_dataset"
        self.target_samples_per_note = target_samples_per_note
        self.sample_rate = 22050  # Standard for audio processing
        
        # Enhanced augmentation parameters for 150 samples (more variations)
        self.augmentation_params = {
            'time_stretch': {
                'rate_range': (0.75, 1.25),  # ±25% tempo variation (increased range)
                'preserve_pitch': True
            },
            'volume_variation': {
                'db_range': (-8, 8),  # ±8dB variation (increased range)
                'preserve_dynamics': True
            },
            'frequency_filtering': {
                'low_shelf': {'freq': 200, 'gain_range': (-4, 4)},  # Increased range
                'mid_boost': {'freq': 800, 'gain_range': (-3, 3)},  # Increased range
                'high_shelf': {'freq': 4000, 'gain_range': (-4, 4)},  # Increased range
                'presence': {'freq': 2500, 'gain_range': (-2, 2)}  # Added presence band
            },
            'noise_addition': {
                'noise_level_range': (-45, -25),  # Wider noise range
                'noise_types': ['pink', 'brown', 'room_tone', 'vinyl_noise', 'tape_hiss']
            },
            'reverb': {
                'room_size_range': (0.05, 0.8),  # Larger room size range
                'decay_time_range': (0.1, 2.0)   # Wider decay time range
            },
            'pitch_shift': {
                'semitone_range': (-0.5, 0.5),  # Very subtle pitch variations
                'preserve_formants': True
            },
            'compression': {
                'ratio_range': (1.5, 4.0),  # Dynamic range compression
                'threshold_range': (-20, -5)  # dB threshold
            }
        }
    
    def load_audio_file(self, file_path):
        """Load audio file and normalize"""
        try:
            # Try loading with librosa first
            audio, sr = librosa.load(file_path, sr=self.sample_rate)
            return audio, sr
        except Exception as e:
            print(f"⚠️  Error loading {file_path}: {e}")
            return None, None
    
    def apply_time_stretch(self, audio, stretch_factor):
        """Apply time stretching without changing pitch"""
        return librosa.effects.time_stretch(audio, rate=stretch_factor)
    
    def apply_volume_variation(self, audio, db_change):
        """Apply volume changes while preserving dynamics"""
        linear_gain = 10 ** (db_change / 20.0)
        return audio * linear_gain
    
    def apply_frequency_filtering(self, audio, sr):
        """Apply subtle EQ changes"""
        filtered_audio = audio.copy()
        
        # Random EQ adjustments
        params = self.augmentation_params['frequency_filtering']
        
        # Low shelf filter
        low_gain = np.random.uniform(*params['low_shelf']['gain_range'])
        if abs(low_gain) > 0.5:
            filtered_audio = self._apply_shelf_filter(filtered_audio, sr, 
                                                    params['low_shelf']['freq'], 
                                                    low_gain, 'low')
        
        # Mid frequency boost/cut
        mid_gain = np.random.uniform(*params['mid_boost']['gain_range'])
        if abs(mid_gain) > 0.5:
            filtered_audio = self._apply_peaking_filter(filtered_audio, sr,
                                                       params['mid_boost']['freq'],
                                                       mid_gain, 1.0)
        
        # High shelf filter
        high_gain = np.random.uniform(*params['high_shelf']['gain_range'])
        if abs(high_gain) > 0.5:
            filtered_audio = self._apply_shelf_filter(filtered_audio, sr,
                                                     params['high_shelf']['freq'],
                                                     high_gain, 'high')
        
        # Presence boost/cut
        presence_gain = np.random.uniform(*params['presence']['gain_range'])
        if abs(presence_gain) > 0.5:
            filtered_audio = self._apply_peaking_filter(filtered_audio, sr,
                                                       params['presence']['freq'],
                                                       presence_gain, 2.0)
        
        return filtered_audio
    
    def _apply_shelf_filter(self, audio, sr, freq, gain_db, shelf_type):
        """Apply shelving filter"""
        # Simple implementation using butterworth filter
        nyquist = sr / 2
        normalized_freq = freq / nyquist
        
        if shelf_type == 'low':
            b, a = butter(2, normalized_freq, btype='low')
        else:  # high
            b, a = butter(2, normalized_freq, btype='high')
        
        filtered = filtfilt(b, a, audio)
        
        # Apply gain
        linear_gain = 10 ** (gain_db / 20.0)
        return audio + (filtered - audio) * (linear_gain - 1)
    
    def _apply_peaking_filter(self, audio, sr, freq, gain_db, q_factor):
        """Apply peaking filter for mid frequencies"""
        # Simple bandpass implementation
        nyquist = sr / 2
        low_freq = freq / (q_factor * 2)
        high_freq = freq * (q_factor * 2)
        
        low_norm = max(0.01, min(0.99, low_freq / nyquist))
        high_norm = max(0.01, min(0.99, high_freq / nyquist))
        
        if low_norm < high_norm:
            b, a = butter(2, [low_norm, high_norm], btype='band')
            filtered = filtfilt(b, a, audio)
            
            linear_gain = 10 ** (gain_db / 20.0)
            return audio + filtered * (linear_gain - 1)
        
        return audio
    
    def add_realistic_noise(self, audio, noise_level_db):
        """Add realistic background noise with more variety"""
        noise_type = np.random.choice(self.augmentation_params['noise_addition']['noise_types'])
        
        # Generate noise based on type
        if noise_type == 'pink':
            noise = self._generate_pink_noise(len(audio))
        elif noise_type == 'brown':
            noise = self._generate_brown_noise(len(audio))
        elif noise_type == 'vinyl_noise':
            noise = self._generate_vinyl_noise(len(audio))
        elif noise_type == 'tape_hiss':
            noise = self._generate_tape_hiss(len(audio))
        else:  # room_tone
            noise = self._generate_room_tone(len(audio))
        
        # Scale noise to desired level
        signal_power = np.mean(audio ** 2)
        noise_power = np.mean(noise ** 2)
        
        noise_linear_level = 10 ** (noise_level_db / 20.0)
        scaling_factor = noise_linear_level * np.sqrt(signal_power / (noise_power + 1e-10))
        
        return audio + noise * scaling_factor
    
    def _generate_pink_noise(self, length):
        """Generate pink noise (1/f noise)"""
        # Simple pink noise approximation
        white_noise = np.random.normal(0, 1, length)
        # Apply 1/f filter approximation
        b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
        a = [1, -2.494956002, 2.017265875, -0.522189400]
        try:
            pink_noise = filtfilt(b, a, white_noise)
            return pink_noise / np.std(pink_noise)
        except:
            return white_noise * 0.1
    
    def _generate_brown_noise(self, length):
        """Generate brown noise (1/f² noise)"""
        white_noise = np.random.normal(0, 1, length)
        # Integrate white noise to get brown noise
        brown_noise = np.cumsum(white_noise)
        return brown_noise / np.std(brown_noise) * 0.1
    
    def _generate_room_tone(self, length):
        """Generate subtle room tone noise"""
        # Very low level pink noise with some characteristic frequencies
        base_noise = self._generate_pink_noise(length) * 0.05
        
        # Add some subtle resonances (room modes)
        t = np.linspace(0, length / self.sample_rate, length, endpoint=False)
        room_resonances = (0.02 * np.sin(2 * np.pi * 60 * t) +  # 60Hz hum
                          0.01 * np.sin(2 * np.pi * 120 * t) +  # 120Hz harmonic
                          0.005 * np.sin(2 * np.pi * 300 * t))  # Mid resonance
        
        return base_noise + room_resonances
    
    def _generate_vinyl_noise(self, length):
        """Generate vinyl record surface noise"""
        # High frequency crackling noise
        white_noise = np.random.normal(0, 1, length) * 0.02
        # Apply high-pass filtering to simulate surface noise
        b, a = butter(2, 1000 / (self.sample_rate / 2), btype='high')
        vinyl_noise = filtfilt(b, a, white_noise)
        return vinyl_noise
    
    def _generate_tape_hiss(self, length):
        """Generate analog tape hiss"""
        # High frequency white noise
        hiss = np.random.normal(0, 1, length) * 0.03
        # Filter to simulate tape hiss frequency response
        b, a = butter(2, [2000 / (self.sample_rate / 2), 8000 / (self.sample_rate / 2)], btype='band')
        tape_hiss = filtfilt(b, a, hiss)
        return tape_hiss
    
    def apply_subtle_pitch_shift(self, audio, semitones):
        """Apply very subtle pitch shifting while preserving note identity"""
        if abs(semitones) < 0.1:  # Skip if change is too small
            return audio
        
        # Use librosa's pitch shifting with high quality
        try:
            shifted = librosa.effects.pitch_shift(audio, sr=self.sample_rate, n_steps=semitones)
            return shifted
        except:
            return audio  # Return original if pitch shift fails
    
    def apply_dynamic_compression(self, audio, ratio, threshold_db):
        """Apply dynamic range compression"""
        threshold_linear = 10 ** (threshold_db / 20.0)
        
        # Simple compression algorithm
        compressed = audio.copy()
        
        # Find samples above threshold
        above_threshold = np.abs(compressed) > threshold_linear
        
        if np.any(above_threshold):
            # Apply compression ratio to samples above threshold
            excess = np.abs(compressed[above_threshold]) - threshold_linear
            compressed_excess = excess / ratio
            
            # Maintain original sign
            compressed[above_threshold] = np.sign(compressed[above_threshold]) * (threshold_linear + compressed_excess)
        
        return compressed
    
    def apply_subtle_reverb(self, audio):
        """Apply subtle reverb simulation"""
        # Simple reverb using multiple delayed copies with exponential decay
        room_size = np.random.uniform(*self.augmentation_params['reverb']['room_size_range'])
        decay_time = np.random.uniform(*self.augmentation_params['reverb']['decay_time_range'])
        
        # Create reverb impulse response
        impulse_length = int(decay_time * self.sample_rate)
        
        # Multiple reflections with random delays
        num_reflections = 8
        reverb_signal = np.zeros(len(audio) + impulse_length)
        reverb_signal[:len(audio)] = audio
        
        for i in range(num_reflections):
            delay = int(np.random.uniform(0.01, decay_time) * self.sample_rate)
            amplitude = room_size * (0.7 ** i)  # Exponential decay
            
            if delay < impulse_length and delay > 0:
                delayed_audio = np.zeros(len(audio) + impulse_length)
                delayed_audio[delay:delay+len(audio)] = audio * amplitude
                reverb_signal += delayed_audio
        
        return reverb_signal[:len(audio)]  # Trim to original length
    
    def create_augmented_variation(self, audio, variation_id):
        """Create a single augmented variation with random parameters"""
        augmented = audio.copy()
        applied_augmentations = []
        
        # Time stretching (80% probability for more variations)
        if np.random.random() < 0.8:
            stretch_factor = np.random.uniform(*self.augmentation_params['time_stretch']['rate_range'])
            augmented = self.apply_time_stretch(augmented, stretch_factor)
            applied_augmentations.append(f"time_stretch_{stretch_factor:.3f}")
        
        # Volume variation (85% probability)
        if np.random.random() < 0.85:
            db_change = np.random.uniform(*self.augmentation_params['volume_variation']['db_range'])
            augmented = self.apply_volume_variation(augmented, db_change)
            applied_augmentations.append(f"volume_{db_change:.1f}dB")
        
        # Frequency filtering (70% probability)
        if np.random.random() < 0.7:
            augmented = self.apply_frequency_filtering(augmented, self.sample_rate)
            applied_augmentations.append("freq_filter")
        
        # Noise addition (50% probability)
        if np.random.random() < 0.5:
            noise_level = np.random.uniform(*self.augmentation_params['noise_addition']['noise_level_range'])
            augmented = self.add_realistic_noise(augmented, noise_level)
            applied_augmentations.append(f"noise_{noise_level:.1f}dB")
        
        # Reverb (40% probability)
        if np.random.random() < 0.4:
            augmented = self.apply_subtle_reverb(augmented)
            applied_augmentations.append("reverb")
        
        # Subtle pitch shift (20% probability - very careful with this)
        if np.random.random() < 0.2:
            pitch_shift = np.random.uniform(*self.augmentation_params['pitch_shift']['semitone_range'])
            augmented = self.apply_subtle_pitch_shift(augmented, pitch_shift)
            applied_augmentations.append(f"pitch_shift_{pitch_shift:.2f}")
        
        # Dynamic compression (30% probability)
        if np.random.random() < 0.3:
            ratio = np.random.uniform(*self.augmentation_params['compression']['ratio_range'])
            threshold = np.random.uniform(*self.augmentation_params['compression']['threshold_range'])
            augmented = self.apply_dynamic_compression(augmented, ratio, threshold)
            applied_augmentations.append(f"compress_{ratio:.1f}:{threshold:.0f}")
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(augmented))
        if max_val > 0.95:
            augmented = augmented / max_val * 0.95
        
        return augmented, applied_augmentations
    
    def process_note_folder(self, note_name, verbose=True):
        """Process all files in a specific note folder"""
        note_folder = self.dataset_path / note_name
        output_folder = self.output_path / note_name
        
        if not note_folder.exists():
            print(f"⚠️  Note folder {note_name} not found")
            return 0
        
        # Create output directory
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Get all audio files in the folder
        audio_files = []
        for ext in ['*.mp3', '*.wav', '*.m4a', '*.aac']:
            audio_files.extend(note_folder.glob(ext))
        
        if not audio_files:
            print(f"⚠️  No audio files found in {note_name} folder")
            return 0
        
        if verbose:
            print(f"\n🎵 Processing {note_name} folder:")
            print(f"   Found {len(audio_files)} original files")
        
        # Copy original files first
        for original_file in audio_files:
            original_output = output_folder / f"original_{original_file.name.replace(' ', '_')}"
            shutil.copy2(original_file, original_output)
        
        # Calculate how many augmentations needed per file
        augmentations_per_file = max(1, (self.target_samples_per_note - len(audio_files)) // len(audio_files))
        
        if verbose:
            print(f"   Creating {augmentations_per_file} variations per original file")
            print(f"   Target: {self.target_samples_per_note} total samples")
        
        # Process each original file with progress bar
        total_created = len(audio_files)  # Start with originals
        
        for file_idx, audio_file in enumerate(audio_files):
            if verbose:
                print(f"   📊 Processing: {audio_file.name}")
            
            # Load audio
            audio, sr = self.load_audio_file(audio_file)
            if audio is None:
                continue
            
            # Create augmented variations with progress bar
            pbar_desc = f"   Augmenting {audio_file.stem}"
            for var_idx in tqdm(range(augmentations_per_file), desc=pbar_desc, leave=False):
                augmented_audio, applied_augs = self.create_augmented_variation(audio, var_idx)
                
                # Generate output filename
                base_name = audio_file.stem.replace(' ', '_')
                output_name = f"{base_name}_aug_{file_idx:02d}_{var_idx:03d}.wav"
                output_path = output_folder / output_name
                
                # Save augmented audio
                sf.write(output_path, augmented_audio, self.sample_rate)
                total_created += 1
                
                # Log applied augmentations for first variation
                if var_idx == 0 and verbose:
                    print(f"      Example augmentations: {', '.join(applied_augs)}")
        
        if verbose:
            print(f"   ✅ Created {total_created} total samples for {note_name}")
        
        return total_created
    
    def augment_full_dataset(self, verbose=True):
        """Process the entire dataset"""
        if verbose:
            print("🥁 TALKING DRUM DATASET AUGMENTATION")
            print("=" * 60)
        
        # Get all note folders
        note_folders = [d.name for d in self.dataset_path.iterdir() if d.is_dir()]
        note_folders.sort()  # Consistent order
        
        if verbose:
            print(f"📁 Found {len(note_folders)} note folders: {', '.join(note_folders)}")
            print(f"🎯 Target samples per note: {self.target_samples_per_note}")
            print(f"📤 Output directory: {self.output_path}")
        
        total_samples_created = 0
        processing_summary = {}
        
        # Process each note folder with overall progress
        for note in tqdm(note_folders, desc="Processing notes", unit="note"):
            samples_created = self.process_note_folder(note, verbose=verbose)
            if samples_created:
                processing_summary[note] = samples_created
                total_samples_created += samples_created
        
        if verbose:
            print(f"\n📊 AUGMENTATION SUMMARY:")
            print("=" * 40)
            for note, count in processing_summary.items():
                original_files = len([f for f in (self.dataset_path / note).glob('*') 
                                    if f.suffix.lower() in ['.mp3', '.wav', '.m4a', '.aac']])
                augmented_files = count - original_files
                print(f"   {note}: {original_files} original → {count} total ({augmented_files} augmented)")
            
            print(f"\n✅ Total samples created: {total_samples_created}")
            print(f"📁 Augmented dataset saved to: {self.output_path}")
        
        return processing_summary


def main():
    """Main function to run the augmentation from command line"""
    parser = argparse.ArgumentParser(description='Talking Drum Dataset Augmentation System')
    
    parser.add_argument('--input', '-i', type=str, 
                       default='/home/user/Documents/yomi_talking_drum/talking_drum_dataset',
                       help='Path to original dataset folder')
    
    parser.add_argument('--output', '-o', type=str,
                       default='/home/user/Documents/yomi_talking_drum/augmented_talking_drum_dataset',
                       help='Path to output augmented dataset folder')
    
    parser.add_argument('--target', '-t', type=int, default=150,
                       help='Target number of samples per note (default: 150)')
    
    parser.add_argument('--note', '-n', type=str, default=None,
                       help='Process only specific note (e.g., "Do", "Re")')
    
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Run in quiet mode with minimal output')
    
    args = parser.parse_args()
    
    # Initialize augmentation system
    augmenter = TalkingDrumAugmentationSystem(
        dataset_path=args.input,
        output_path=args.output,
        target_samples_per_note=args.target
    )
    
    # Check if input dataset exists
    if not os.path.exists(args.input):
        print(f"❌ Error: Dataset not found at {args.input}")
        print(f"   Please ensure the talking_drum_dataset folder exists")
        return
    
    # Start processing
    start_time = time.time()
    verbose = not args.quiet
    
    if verbose:
        print("🚀 Starting Talking Drum Dataset Augmentation")
        print(f"📁 Input: {args.input}")
        print(f"📤 Output: {args.output}")
        print(f"🎯 Target: {args.target} samples per note")
        print("-" * 50)
    
    if args.note:
        # Process single note
        samples_created = augmenter.process_note_folder(args.note, verbose=verbose)
        if samples_created > 0:
            print(f"✅ Successfully created {samples_created} samples for note '{args.note}'")
        else:
            print(f"❌ Failed to process note '{args.note}'")
    else:
        # Process full dataset
        results = augmenter.augment_full_dataset(verbose=verbose)
        
        if verbose:
            elapsed_time = time.time() - start_time
            print(f"\n🎉 AUGMENTATION COMPLETED!")
            print(f"⏱️  Total time: {elapsed_time:.1f} seconds")
            print(f"📊 Processed {len(results)} note folders")
            print(f"🎯 Dataset ready for AI training!")


if __name__ == "__main__":
    main()
