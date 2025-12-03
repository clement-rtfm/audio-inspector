import matplotlib.pyplot as plt
import numpy as np
import os


def generate_spectrogram(mono, sr, original_path):
    name = os.path.splitext(os.path.basename(original_path))[0]
    outfile = f"out/{name}_spectrogram.png"

    plt.figure(figsize=(10, 6))
    plt.specgram(mono, Fs=sr, NFFT=2048, noverlap=1024)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title("Spectrogram")
    plt.savefig(outfile, dpi=200)
    plt.close()

    return outfile
