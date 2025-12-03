
# audio-inspector

A complete audio analysis tool: fake FLAC detection, spectrograms, dynamic metrics, and JSON reporting.

A CLI tool designed for audiophiles, archivists, music collectors, and engineers who want to verify the authenticity and quality of an audio file.

---
For the French version, see **[README in French](README.md)**.
---

## 🚀 Main Features
- **Fake FLAC / upscaled MP3 detection** (lowpass analysis + high-frequency energy)
- **High-quality spectrograms** exported as PNG
- **Essential audio metrics**: RMS, peak, estimated DR
- **Wide compatibility**: FLAC, WAV, MP3, OGG, AAC (via `librosa` + `soundfile`)
- **JSON export** for metrics
- **Simple, clean CLI** powered by `typer`

---

## 📦 Installation (Windows, Linux, macOS)

### 1) Clone the repository
```bash
git clone https://github.com/clement-rtfm/audio-inspector.git
cd audio-inspector
````

### 🐍 2) Create a Python virtual environment

* 🔹 Linux / macOS

```bash
python3 -m venv .venv
# then
source .venv/bin/activate
```

* 🔹 Windows (PowerShell)

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

* 🔹 Windows (CMD)

```bash
python -m venv .venv
.\.venv\Scripts\activate.bat
```

Make sure the virtual environment is active:
your terminal prompt should start with `(.venv)`.

### 📚 3) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**⚠️ Possible system dependencies**

Depending on your OS, you may need to install additional libraries:

* Linux (Debian, Ubuntu, Mint…)

```bash
sudo apt install ffmpeg libsndfile1 libasound2
```

* Arch / Manjaro

```bash
sudo pacman -S ffmpeg libsndfile alsa-lib
```

* Fedora

```bash
sudo dnf install ffmpeg libsndfile alsa-lib
```

* macOS (Homebrew)

```bash
brew install ffmpeg libsndfile
```

* Windows
  No package manager installation required.

`ffmpeg` is recommended for improved analysis:
→ download the Windows build from ffmpeg.org and add the `bin/` folder to your PATH.

---

## 🧪 Quick Usage

### Basic analysis

```bash
python cli.py music.flac
```

### Analysis + spectrogram export

```bash
python cli.py music.flac --plot
```

This generates:

```bash
out/music_spectrogram.png
```

### Analysis + JSON export (for automation or scripting)

```bash
python cli.py music.flac --json out/report.json
```

### Full analysis (spectrogram + JSON + terminal log)

```bash
python cli.py music.flac --plot --json out/report.json --verbose
```

---

## 📝 Example terminal output

```bash
[+] File: music.flac
[+] Sample rate: 44100 Hz | Channels: 2 | Bitdepth: 24
[+] RMS: -15.23 dB | Peak: -1.40 dB
[+] DR (est.): 13.8
[!] Lowpass detected at ~16500 Hz → possible upscaled lossy source
[+] FLAC purity score: 32/100
Spectrogram saved to out/music_spectrogram.png
```

---

## 🧠 How fake FLAC detection works

The detection is based on multiple combined audio analyses to identify the typical characteristics of a **lossy file re-encoded as FLAC (fake FLAC)**.
The script does **not** rely on bitrate, but on spectral signatures.

### 🔍 1) Spectral analysis via STFT

The file is split into time windows, then transformed into a spectrogram (STFT).
This reveals:

* the frequency distribution
* the high-frequency energy
* abnormal cutoffs or spectral gaps

### ✂️ 2) Detection of lossy lowpass cutoffs

Lossy codecs remove most energy above:

* ~16 kHz (MP3 320)
* ~18–19 kHz (AAC)
* ~15 kHz (lower MP3 VBR)

The script looks for:

* a **sharp drop** in high-frequency content
* a transition too clean to come from a true lossless master

This is the primary indicator of a fake FLAC.

### ⚖️ 3) Computing the “FLAC Purity Score”

The tool measures the residual high-frequency energy above a threshold (default: ~16 kHz).
It evaluates:

* amount of HF energy
* spectral smoothness
* presence of lossy artifacts (holes, smearing, HF noise patterns)

It outputs a normalized score:

```
0.0 → very likely lossy
1.0 → very likely true FLAC
```

### 📊 4) Probabilistic indicator

Detection is **never absolute**.
It provides a probability, useful to:

* verify entire libraries
* detect fake files downloaded online
* compare different editions of the same album

It’s not a definitive judgment, but a powerful **quality filter**.
