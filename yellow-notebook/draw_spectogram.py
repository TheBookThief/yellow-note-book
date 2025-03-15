import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys

def generate_spectrogram(audio_path, save_path=None):
    # Load audio file
    y, sr = librosa.load(audio_path, sr=None)
    
    # Compute Short-Time Fourier Transform (STFT)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    
    # Plot spectrogram
    plt.figure(figsize=(10, 5))
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    
    # Save or show plot
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <audio_file> [output_image]")
    else:
        audio_file = sys.argv[1]
        output_image = sys.argv[2] if len(sys.argv) > 2 else None
        generate_spectrogram(audio_file, output_image)
