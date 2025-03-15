from fourier import remove_band
import librosa
import soundfile as sf

def encode_dabros(audio, sr, bits, golden=[1000,2000], silver=[2000,4000], bitlen=0.5):
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

# Example usage
input_file = 'C:/Users/SURF Student/Hackaton/DABROS/DABROS/audio/violin.wav'  # Input WAV file
output_file = 'C:/Users/SURF Student/Hackaton/DABROS/DABROS/audio/encoded_song_filtered.wav'  # Output WAV file
y, sr = librosa.load(input_file, sr=None) 
lowcut = 1000  # Lower bound of the frequency band (in Hz)
highcut = 2000  # Upper bound of the frequency band (in Hz)
start_time = 30  # Start time (in seconds) to apply the filter
end_time = 40  # End time (in seconds) to apply the filter

# output = encode_dabros(y, sr, [1,1,0,0,1,0,1,0,1,1,1,0,0])

output = encode_dabros(y, sr, [1,0,0,1,0,0,1,1,1,0,1,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0,1,0,0,1,0,0,1,1,1,0,1,1,0])

sf.write(output_file, output, sr)
print(f"Processed file saved as {output_file}")
