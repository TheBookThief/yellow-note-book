import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys

def generate_spectrogram(audio_path, save_path=None):
    y, sr = librosa.load(audio_path, sr=None)
    
    # Compute Short-Time Fourier Transform (STFT)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    
    plt.figure(figsize=(10, 5))
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='linear')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    
    if save_path:
        plt.savefig(save_path)
    else:
        print("Showing")
        plt.show(block=False)
        print("Done")
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <audio_file> [output_image]")
    else:
        audio_file = sys.argv[1]
        output_image = sys.argv[2] if len(sys.argv) > 2 else None
        print("Generating spectogram now:")
        generate_spectrogram(audio_file, output_image)
        print("Spectogram generated ----")