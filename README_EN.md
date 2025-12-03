# audio-inspector

Complete audio analyzer: detects fake FLAC files, generates spectrograms, dynamic range metrics, and provides a JSON report.

A CLI tool designed for audiophiles, archivists, music collectors, and engineers who want to verify the authenticity and quality of an audio file.

--- Pour la version francaise, voir [README en francais](README.md).

---

## 🚀 Main Features
- **Detection of fake upscaled FLAC/MP3 files** (lowpass and high-frequency energy analysis)
- **High-quality spectrograms** exported as PNGs
- **Essential audio metrics**: RMS, peak, estimated DR
- **Wide compatibility**: FLAC, WAV, MP3, OGG, AAC (via `librosa` + `soundfile`)
- **JSON export** of metrics
- **Simple and clean CLI** with `typer`

---

## 📦 Installation (Windows, Linux, macOS)

### PIP
````bash
pip install -i https://test.pypi.org/simple --extra-index-url https://pypi.org/simple audio-inspector==0.1.0
````

---

## 🧪 Usage Quick

### Simple Analysis
```bash
audio-inspector "path/music.flac"
```
### Analysis + Spectrogram Export
```bash
audio-inspector "path/music.flac" --plot
```
→ Automatically generates:
```bash
out/music_spectrogram.png
```
### Analysis + JSON Export (for automation or integration into a script)
```bash
audio-inspector "path/music.flac" --json out/report.json
```
### All at the same time (spectrogram + JSON + terminal log)
```bash
audio-inspector "path/music.flac" --plot --json out/report.json --verbose
```

## 📝 Terminal Output Example
```bash
[+] File: music.flac
[+] Sample rate: 44100 Hz | Channels: 2 | Bitdepth: 24
[+] RMS: -15.23 dB | Peak: -1.40 dB
[+] DR (est.): 13.8
[!] Lowpass detected at ~16500 Hz → possible upscaled lossy
[+] FLAC purity score: 32/100
Spectrogram saved to out/music_spectrogram.png
```

## 🧠 How does fake FLAC detection work?
Detection relies on several combined audio analyses to identify the typical characteristics of a **lossy file re-encoded in FLAC (fake FLAC).**
The script is not based on the **bitrate**, but on signatures in the spectrum.

### 🔍 1) Spectral Analysis via STFT
The file is divided into time windows and then transformed into a spectrogram (STFT).

This allows us to observe:

- the frequency distribution,

- the energy in the high frequencies,

- any abnormal cutoffs.

### ✂️ 2) Detection of a Lossy Cutoff
MP3/AAC formats remove energy beyond:
- ~16 kHz (MP3 320)
- ~18–19 kHz (AAC)
- ~15 kHz (lower VBR)
The script looks for:
- a sharp drop in the spectrum in the high frequencies,

- a transition too abrupt to be a lossless master.

This is the main indicator of a fake FLAC.

### ⚖️ 3) Calculating a “FLAC Purity Score”
This tool measures the residual energy above a threshold (by default ~16 kHz).

It weights:

- the amount of energy,

- the regularity of the spectrum,

- the presence of lossy artifacts (blemishes, holes, artificial high-frequency noise).

It produces a typical score:
````bash
0.0 → very likely lossy
1.0 → very likely true FLAC
````

### 📊 4) Probabilistic Indicator
The detection is never absolute:

it provides a probability, useful for:

- verifying complete collections,

- detecting fake files downloaded from the internet,

- comparing several versions of the same album.
It is not a definitive judge, but a very good quality filter.
