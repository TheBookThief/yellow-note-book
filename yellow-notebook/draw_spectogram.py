import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys
import scipy.io.wavfile as wav
from scipy.signal import spectrogram
import imageio


def generate_spectrogram(audio_path, save_path=None):
    y, sr = librosa.load(audio_path, sr=None)
    
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


def generate_spectrogram_2(file_path, save_path=None, nperseg=1024, noverlap=512, cmap='inferno', duration=60, max_frequency=6000):
    sample_rate, audio_data = wav.read(file_path)
    
    max_samples = duration * sample_rate
    
    audio_data = audio_data[:max_samples]

    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)

    frequencies, times, Sxx = spectrogram(audio_data, fs=sample_rate, nperseg=nperseg, noverlap=noverlap)

    Sxx_dB = 10 * np.log10(Sxx + 1e-10)

    freq_limit_idx = frequencies <= max_frequency
    frequencies = frequencies[freq_limit_idx]
    Sxx_dB = Sxx_dB[freq_limit_idx, :]

    fig, ax = plt.subplots(figsize=(10, 6))
    cax = ax.pcolormesh(times, frequencies, Sxx_dB, shading='gouraud', cmap=cmap)
    ax.set_ylabel("Frequency [Hz]")
    ax.set_xlabel("Time [s]")
    fig.colorbar(cax, label="Intensity [dB]")
    ax.set_title(f"Spectrogram of {file_path} (First {duration} Seconds, up to {max_frequency} Hz)")
    plt.show(block=False)

    if save_path:
        img_path = save_path if save_path.endswith('.png') else save_path + '.png'
        fig.savefig(img_path, format='png', bbox_inches='tight')  # Use bbox_inches='tight' to avoid clipping
        print(f"Spectrogram saved as PNG at: {img_path}")