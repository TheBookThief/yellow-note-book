from fourier import extract_band
import librosa
import soundfile as sf

def decode_dabros(audio, sr, golden=[1000,2000], silver=[2000,4000], bitlen=1):
    template = bitlen / 3
    audio_length = len(audio) / sr
    final_pos = audio_length - template
    current_pos = 0
    reading = True
    output = []
    while current_pos < audio_length:
        end_pos = current_pos + template
        golden_state = extract_band(audio, sr, golden[0], golden[1], start_time=current_pos, end_time=end_pos) < 0.4
        silver_state = extract_band(audio, sr, silver[0], silver[1], start_time=current_pos, end_time=end_pos) < 0.4
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

input_file = './audio/violin.wav'  # Input WAV file
output_file = './audio/encoded_song_filtered.wav'  # Output WAV file
y, sr = librosa.load(output_file, sr=None) 
lowcut = 1000  # Lower bound of the frequency band (in Hz)
highcut = 2000  # Upper bound of the frequency band (in Hz)
start_time = 30  # Start time (in seconds) to apply the filter
end_time = 40  # End time (in seconds) to apply the filter

output = decode_dabros(y, sr)
print(output)
#sf.write(output_file, output, sr)
#print(f"Processed file saved as {output_file}")