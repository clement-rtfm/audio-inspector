# audio-inspector

Analyseur audio complet : détection de faux FLAC, spectrogrammes, métriques dynamiques, et rapport JSON.

Outil CLI conçu pour audiophiles, archivistes, collectionneurs de musique et engineers qui veulent vérifier l’authenticité et la qualité d’un fichier audio.

---
Pour la version anglaise, consultez [README en anglais](README_EN.md).
---

## 🚀 Fonctionnalités principales
- **Détection de faux FLAC / MP3 upscalés** (analyse du lowpass et énergie haute fréquence)
- **Spectrogrammes haute qualité** exportés en PNG
- **Mesures audio essentielles** : RMS, peak, DR estimé
- **Compatibilité large** : FLAC, WAV, MP3, OGG, AAC (via `librosa` + `soundfile`)
- **Export JSON** des métriques
- **CLI simple et propre** avec `typer`

---

## 📦 Installation (Windows, Linux, macOS)

### 1) Cloner le dépôt
````bash
git clone https://github.com/clement-rtfm/audio-inspector.git
cd audio-inspector
````

### 🐍 2) Créer un environnement Python virtuel
- 🔹 Linux / macOS
```bash
python3 -m venv .venv
# puis
source .venv/bin/activate
```
- 🔹 Windows (PowerShell)
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
- 🔹 Windows (CMD classique)
````bash
python -m venv .venv
.\.venv\Scripts\activate.bat
````
Vérifiez ensuite que l’environnement est actif :
le prompt doit afficher (.venv) au début.

### 📚 3) Installer les dépendances

Si vous utilisez Linux / macOS / Windows
````bash
pip install --upgrade pip
pip install -r requirements.txt
````
**⚠️ Dépendances système éventuellement nécessaires**
Selon votre OS, certaines libs peuvent nécessiter des paquets additionnels :
- Linux (Debian, Ubuntu, Mint…)
 ````bash
sudo apt install ffmpeg libsndfile1 libasound2
````
- Arch / Manjaro
````bash
sudo pacman -S ffmpeg libsndfile alsa-lib
````
- Fedora
````bash
sudo dnf install ffmpeg libsndfile alsa-lib
````
- macOS (Homebrew)
````bash
brew install ffmpeg libsndfile
````
- Windows
  Rien à installer via package manager.

  ffmpeg est recommandé pour une analyse plus complète :
  → télécharger la version Windows sur ffmpeg.org et ajouter le dossier bin/ au PATH.

---

## 🧪 Utilisation rapide

### Analyse simple
```bash
python cli.py musique.flac
```
### Analyse + export du spectrogramme
```bash
python cli.py musique.flac --plot
```
→ génère automatiquement :
```bash
out/musique_spectrogram.png
```
### Analyse + export JSON (pour automatiser ou intégrer dans un script)
```bash
python cli.py musique.flac --json out/rapport.json
```
### Tout en même temps (spectrogramme + JSON + log terminal)
```bash
python cli.py musique.flac --plot --json out/rapport.json --verbose
```


## 📝 Exemple de sortie terminal
```bash
[+] File: musique.flac
[+] Sample rate: 44100 Hz | Channels: 2 | Bitdepth: 24
[+] RMS: -15.23 dB | Peak: -1.40 dB
[+] DR (est.): 13.8
[!] Lowpass détecté à ~16500 Hz → possible upscaled lossy
[+] FLAC purity score: 32/100
Spectrogram saved to out/musique_spectrogram.png
```


## 🧠 Comment fonctionne la détection de faux FLAC ?
- Analyse du spectre moyen via STFT
- Recherche d’un cutoff brutal typique d’un encodage lossy (MP3/AAC)
- Calcul d’un FLAC purity score basé sur l’énergie au-dessus de 16 kHz
- Indication probabiliste, non absolue : utile pour vérifier des bibliothèques entières
