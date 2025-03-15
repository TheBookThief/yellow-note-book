import numpy as np
import librosa

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