# audio-inspector

Comprehensive audio analyzer: detects fake FLACs, generates spectrograms, calculates dynamic metrics, and exports JSON reports.

A CLI tool designed for audiophiles, archivists, music collectors, and engineers who want to verify the authenticity and quality of audio files.

---
For the French version, see [README in French](README_FR.md).
---

## 🚀 Key Features
- **Fake FLAC / Upscaled MP3 detection** (analyzes lowpass and high-frequency energy)
- **High-quality spectrograms** exported as PNG
- **Essential audio measurements**: RMS, peak, estimated DR
- **Wide format support**: FLAC, WAV, MP3, OGG, AAC (via `librosa` + `soundfile`)
- **JSON export** of metrics
- **Clean and simple CLI** powered by `typer`

---

## 📦 Installation
```bash
# create a virtual environment
python -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

---

## 🧪 Quick Usage

### Basic analysis
```bash
python cli.py analyze music.flac
```
### Analysis + spectrogram export
```bash
python cli.py analyze music.flac --plot
```
Automatically generates:
```bash
out/music_spectrogram.png
```
### Analysis + JSON export (for automation or script integration)
```bash
python cli.py analyze music.flac --json out/report.json
```
### All-in-one (spectrogram + JSON + terminal log)
```bash
python cli.py analyze music.flac --plot --json out/report.json --verbose
```

## 📝 Example terminal output
```bash
[+] File: music.flac
[+] Sample rate: 44100 Hz | Channels: 2 | Bit depth: 24
[+] RMS: -15.23 dB | Peak: -1.40 dB
[+] DR (est.): 13.8
[!] Lowpass detected at ~16500 Hz → possible upscaled lossy
[+] FLAC purity score: 32/100
Spectrogram saved to out/music_spectrogram.png
```

## 🧠 How does fake FLAC detection work?
- Analyzes the average spectrum using STFT
- Looks for sharp cutoffs typical of lossy encoding (MP3/AAC)
- Computes a FLAC purity score based on energy above 16 kHz
- Probabilistic indication, not absolute: useful for checking entire libraries
