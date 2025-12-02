from pathlib import Path
import soundfile as sf
import numpy as np
import librosa
from .utils import dbfs, peak_db, ensure_mono
from .spectrogram import save_spectrogram
from .detector import detect_lowpass


def guess_bitdepth(subtype: str):
    if not subtype:
        return None
    subtype = subtype.lower()
    if '24' in subtype:
        return 24
    if '16' in subtype:
        return 16
    if '32' in subtype:
        return 32
    return None


def analyze_file(path: str, plot: bool = True):
    p = Path(path)
    y, sr = librosa.load(path, sr=None, mono=False)
    # librosa loads as float32 normalized -1..1

    # try to get file info via soundfile
    try:
        info = sf.info(path)
        subtype = info.subtype
        bitdepth = guess_bitdepth(subtype)
        channels = info.channels
    except Exception:
        subtype = None
        bitdepth = None
        # infer channels from y
        channels = 1 if y.ndim == 1 else y.shape[0]

    # ensure mono for spectral detection
    y_mono = ensure_mono(y)

    # compute rms and peak (in dB)
    rms = dbfs(y_mono)
    peak = peak_db(y_mono)

    # simple DR estimate: peak_db - rms_db
    dr_est = peak - rms

    # detect lowpass / fake flac
    lp_detected, cutoff_freq, purity_score = detect_lowpass(y_mono, sr)

    spectrogram_path = None
    if plot:
        out_png = Path('out') / f"{p.stem}_spectrogram.png"
        spectrogram_path = save_spectrogram(y_mono, sr, out_png)

    out = {
        'path': str(p),
        'sr': int(sr),
        'channels': int(channels),
        'bitdepth': int(bitdepth) if bitdepth else None,
        'dr_est': dr_est,
        'lowpass_detected': lp_detected,
        'cutoff_freq': cutoff_freq,
        'purity_score': purity_score,
        'spectrogram_path': spectrogram_path
    }

    return out
