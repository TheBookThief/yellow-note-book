import sys
import re
import librosa
import soundfile as sf
import numpy as np
import os

from draw_spectogram import generate_spectrogram, generate_spectrogram_2

def find_coefficients(polynom):
    polynom = polynom.replace(' ', '')
    
    if polynom[0] not in '+-':
        polynom = '+' + polynom
    
    terms = re.findall(r'[+-][^+-]+', polynom)
    variable_match = re.search(r'[a-zA-Z]', polynom)
    variable = variable_match.group(0)

    
    coefficients = {}
    
    for term in terms:
        sign = 1 if term[0] == '+' else -1
        term = term[1:]
        
        if variable in term:
            parts = term.split(variable)
            coef = int(parts[0]) if parts[0] != '' else 1
            coef *= sign 
            
            if '^' in term:
                exponent = int(parts[1].replace('^', ''))
            else:
                exponent = 1
        else:
            coef = int(term) * sign
            exponent = 0
        
        coefficients[exponent] = coef
    
    max_exp = max(coefficients.keys()) if coefficients else 0

    result = [coefficients.get(exp, 0) for exp in range(max_exp, -1, -1)]
    return result

def polynomial_to_binary(coefficients, bits=5):
    binary_sequence = []

    length_binary = format(len(coefficients), f'0{bits}b')
    binary_sequence.extend([int(bit) for bit in length_binary])
    
    for coeff in coefficients:
        binary_coeff = format(coeff, f'0{bits}b')
        binary_sequence.extend([int(bit) for bit in binary_coeff])
    
    return binary_sequence

def remove_band(audio, sr, lowcut, highcut, start_time, end_time):
    start_idx = int(start_time * sr)
    end_idx = int(end_time * sr)
    portion_y = audio[start_idx:end_idx] 
    # Perform Short-Time Fourier Transform (STFT) to work in the frequency domain
    D = librosa.stft(portion_y)
    # Get the frequencies corresponding to each bin
    freqs = librosa.fft_frequencies(sr=sr)
    D[(freqs > lowcut) & (freqs < highcut)] = 0
    D[(freqs < -lowcut) & (freqs > -highcut)] = 0
    # Inverse Short-Time Fourier Transform (ISTFT) to convert back to the time domain
    filtered_portion_y = librosa.istft(D)
    target_length = len(portion_y)
    if len(filtered_portion_y) < target_length:
        padding = target_length - len(filtered_portion_y)
        filtered_portion_y = np.pad(filtered_portion_y, (0, padding), mode='constant')
    elif len(filtered_portion_y) > target_length:
        filtered_portion_y = filtered_portion_y[:target_length]
    audio[start_idx:end_idx] = filtered_portion_y
    return audio

def encode_dabros(audio, sr, bits, golden=[1000,2000], silver=[2000,4000], bitlen=1):
    audio_length = len(audio) / sr
    if audio_length < 2 * len(bits) * bitlen:
        raise Exception("Data is too long.")
    current_pos = 0
    for bit in bits:
        lowcut = golden[0] if bit else silver[0]
        highcut = golden[1] if bit else silver[1] 
        audio = remove_band(audio, sr, lowcut, highcut, current_pos, current_pos + bitlen)
        current_pos += 2 * bitlen
    return audio


def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <pol> <audio_path>")
        sys.exit(1)
    
    pol = sys.argv[1]
    original_audio_path = sys.argv[2]
    
    # print(f"Polinomial: {pol}")
    # print(f"Audio Path: {original_audio_path}")
    # print(f"Coefficients: {find_coefficients(pol)}")
    # print(f"Binary: {polynomial_to_binary(find_coefficients(pol), bits=5)}")
    
    y, sr = librosa.load(original_audio_path, sr=None)



    directory = r"\public\audio"
    filename = os.path.basename(original_audio_path)
    name, ext = os.path.splitext(filename)
    new_filename = name + '_audio_encoded' + ext
    output_path = "./public/audio/" + new_filename#os.path.join(directory, new_filename)

    # output_path = original_audio_path.replace(".wav", "_encoded.wav")
    # output_path = "C:\\Users\\Maria Drencheva\\Desktop\\FMI\\Competitive\\Hackaton 25\\yellow-note-book\\yellow-notebook\\public\\audio\\audio_encoded.wav"
    
    bits = polynomial_to_binary(find_coefficients(pol), bits=5)
    
    processed_audio = encode_dabros(y, sr, bits)
    
    sf.write(output_path, processed_audio, sr)
    # print(f"Processed file saved as {output_path}")

    generate_spectrogram_2(output_path, "./public/spect/" + name + ".png")
    print("OK")

if __name__ == "__main__":
    main()