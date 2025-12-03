import soundfile as sf
import numpy as np
import os
from .spectrogram import generate_spectrogram


def analyze_file(path, plot=False):
    data, samplerate = sf.read(path)
    channels = data.shape[1] if len(data.shape) > 1 else 1

    # Ensure 2D data for analysis
    if channels == 1:
        mono = data
    else:
        mono = np.mean(data, axis=1)

    bitdepth = guess_bit_depth(data)

    # RMS / Peak
    rms = 20 * np.log10(np.sqrt(np.mean(mono ** 2)) + 1e-12)
    peak = 20 * np.log10(np.max(np.abs(mono)) + 1e-12)

    # DR estimation
    dr = estimate_dr(mono)

    # Lowpass detection
    lowpass = detect_lowpass(mono, samplerate)

    # FLAC quality score
    flac_score = flac_integrity_score(lowpass, dr)

    spectrogram_path = None
    if plot:
        os.makedirs("out", exist_ok=True)
        spectrogram_path = generate_spectrogram(mono, samplerate, path)

    return {
        "path": path,
        "samplerate": int(samplerate),
        "channels": channels,
        "bitdepth": bitdepth,
        "rms": float(rms),
        "peak": float(peak),
        "dr": float(dr),
        "lowpass": int(lowpass) if lowpass else None,
        "flac_score": int(flac_score),
        "spectrogram_path": spectrogram_path,
    }


# -------------------------
#  ANALYSIS UTILITIES
# -------------------------

def guess_bit_depth(data):
    if data.dtype == np.int16:
        return 16
    if data.dtype == np.int32:
        return 24
    if data.dtype == np.float32:
        return 24
    return 16


def estimate_dr(mono):
    # DR = peak - RMS
    peak = 20 * np.log10(np.max(np.abs(mono)) + 1e-12)
    rms = 20 * np.log10(np.sqrt(np.mean(mono ** 2)) + 1e-12)
    return peak - rms


def detect_lowpass(mono, sr):
    spectrum = np.abs(np.fft.rfft(mono))
    freqs = np.fft.rfftfreq(len(mono), 1 / sr)
    threshold = max(spectrum) * 0.015  # 1.5%

    valid = freqs[spectrum > threshold]

    if len(valid) == 0:
        return None

    limit = valid[-1]

    if limit < 18000:  # typical mp3 cutoff
        return int(limit)

    return None


def flac_integrity_score(lowpass, dr):
    base = 100
    if lowpass:
        base -= 40
    if dr < 8:
        base -= 20
    if dr < 5:
        base -= 30
    return max(0, base)
