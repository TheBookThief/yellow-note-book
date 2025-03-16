import sys
import re
import librosa
import soundfile as sf
import numpy as np
import os

def make_polynom(coefficients):
    terms = []
    degree = len(coefficients) - 1

    for i, coeff in enumerate(coefficients):
        exp = degree - i

        if coeff == 0:
            continue

        if coeff > 0:
            if not terms:
                term = f"{coeff}" if coeff != 1 else ""
            else:
                term = f"+ {coeff}" if coeff != 1 or exp == 0 else "+ "

        elif coeff < 0:
            term = f"- {-coeff}" if coeff != -1 or exp == 0 else "- "

        if exp > 1:
            term += f"x^{exp}"
        elif exp == 1:
            term += "x"
        
        terms.append(term)

    polynomial = " ".join(terms)

    return polynomial if polynomial else "0"

def find_coefficients(bits, batch_size = 8):
    coefficients = []
    
    for i in range(0, len(bits), batch_size):
        batch = bits[i:i+batch_size]
        binary_str = ''.join(map(str, batch)) 
        coefficients.append(int(binary_str, 2))
    
    return coefficients

def extract_band(audio, sr, low_freq, high_freq, start_time=0, end_time=None):
    if end_time is None:
        end_time = len(audio) / sr 
    start_sample = int(start_time * sr)
    end_sample = int(end_time * sr)
    audio_segment = audio[start_sample:end_sample]
    # Perform the Fourier Transform (FFT)
    spectrum = np.fft.fft(audio_segment)
    frequencies = np.fft.fftfreq(len(audio_segment), d=1/sr)
    freq_mask = (np.abs(frequencies) >= low_freq) & (np.abs(frequencies) <= high_freq)
    magnitude = np.abs(spectrum[freq_mask])
    average_presence = np.mean(magnitude)
    return average_presence

def decode_dabros(audio, sr, golden=[1000,2000], silver=[2000,4000], bitlen=1):
    template = bitlen / 3
    audio_length = len(audio) / sr
    final_pos = audio_length - template
    current_pos = 0
    reading = True
    output = []
    while current_pos < audio_length:
        end_pos = current_pos + template
        golden_state = extract_band(audio, sr, golden[0], golden[1], start_time=current_pos, end_time=end_pos) < 0.5
        silver_state = extract_band(audio, sr, silver[0], silver[1], start_time=current_pos, end_time=end_pos) < 0.5
        # print("Golden:", golden_state, "; Silver:", silver_state)
        if not golden_state and not silver_state:
            reading = True
        if reading and golden_state and not silver_state:
            output.append(1)
            reading = False
        if reading and silver_state and not golden_state:
            output.append(0)
            reading = False
        current_pos += template
    return output


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <audio_path>")
        sys.exit(1)
    
    encoded_audio_path = sys.argv[1]
    
    print(f"Encoded Path: {encoded_audio_path}")    
    y, sr = librosa.load(encoded_audio_path, sr=None)
    binary = decode_dabros(y, sr)
    print(f"Binary: {binary}")
    coeff = find_coefficients(binary, batch_size=8)
    print(f"Coefficients: {coeff}")
    poly = make_polynom(coeff)
    print(f"Polynomial: {poly}")

if __name__ == "__main__":
    main()
