import numpy as np
import librosa


def detect_lowpass(y, sr, freq_threshold=16000.0):
    """
    Détecte la présence d'un lowpass artificiel typique des ré-encodages lossy.
    Méthode simple : calcule l'énergie moyenne par bande et cherche chute brusque > freq_threshold.
    Retourne (detected: bool, cutoff_freq_hz: float approx, purity_score: 0-100)
    """
    # compute magnitude spectrum via STFT and average over time
    S = np.abs(librosa.stft(y, n_fft=4096, hop_length=2048))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=4096)

    # mean spectrum
    mean_spec = np.mean(S, axis=1)

    # normalize
    norm = mean_spec / (np.max(mean_spec) + 1e-12)

    # find highest freq where energy > threshold_ratio
    threshold_ratio = 0.01  # 1% of peak
    indices = np.where(norm >= threshold_ratio)[0]
    if len(indices) == 0:
        return True, 0.0, 0
    max_idx = indices[-1]
    max_freq = freqs[max_idx]

    # purity score: proportion of energy above 16kHz
    high_band = freqs >= 16000
    if np.sum(mean_spec) <= 0:
        purity = 0
    else:
        purity = float(np.sum(mean_spec[high_band]) / np.sum(mean_spec))
    # map to 0-100
    purity_score = int(np.clip(purity * 400, 0, 100))

    # detected if max_freq < freq_threshold
    detected = max_freq < freq_threshold
    return detected, float(max_freq), purity_score
