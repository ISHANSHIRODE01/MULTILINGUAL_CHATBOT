#!/usr/bin/env python3
"""
Create a simple test audio file for ASR testing
"""
import numpy as np
import soundfile as sf
import os

def create_test_audio():
    """Create a simple sine wave audio file for testing"""
    try:
        # Generate a 2-second sine wave at 440Hz (A note)
        sample_rate = 16000
        duration = 2.0
        frequency = 440.0
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = np.sin(2 * np.pi * frequency * t) * 0.3
        
        # Save as WAV file
        output_path = "test_audio.wav"
        sf.write(output_path, audio, sample_rate)
        
        print(f"Created test audio file: {output_path}")
        print(f"Duration: {duration}s, Sample rate: {sample_rate}Hz")
        return True
        
    except Exception as e:
        print(f"Failed to create test audio: {e}")
        return False

if __name__ == "__main__":
    create_test_audio()