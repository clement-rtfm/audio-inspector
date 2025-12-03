# audio-inspector

Analyseur audio complet : détection de faux FLAC, spectrogrammes, métriques dynamiques, et rapport JSON.

Outil CLI conçu pour audiophiles, archivistes, collectionneurs de musique et engineers qui veulent vérifier l’authenticité et la qualité d’un fichier audio.

---
For the English version, see [README in English](README_EN.md).
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
La détection repose sur plusieurs analyses audio combinées pour repérer les caractéristiques typiques d’un fichier **lossy ré-encodé en FLAC (faux FLAC).**
Le script ne se base pas sur le **bitrate**, mais sur des signatures dans le spectre.

### 🔍 1) Analyse spectrale via STFT
Le fichier est découpé en fenêtres temporelles, puis transformé en spectrogramme (STFT).  
Cela permet d’observer :
- la répartition fréquentielle,
- l’énergie dans les hautes fréquences,
- les coupures anormales.

### ✂️ 2) Détection d’un “cutoff” lossy
Les formats MP3/AAC suppriment l’énergie au-delà :
- ~16 kHz (MP3 320)
- ~18–19 kHz (AAC)
- ~15 kHz (VBR plus bas)
Le script recherche :
- un effondrement brutal du spectre dans les hautes fréquences,
- une transition trop nette pour être un master lossless.
C’est l’indicateur principal d’un faux FLAC.

### ⚖️ 3) Calcul d’un “FLAC Purity Score”
L’outil mesure l’énergie résiduelle au-dessus d’un seuil (par défaut ~16 kHz).  
Il pondère :
- la quantité d’énergie,
- la régularité du spectre,
- la présence d’artefacts lossy (bavures, trous, bruit de haute fréquence artificiel).  
Il produit une note typée :
````bash
0.0 → très probablement lossy
1.0 → très probablement vrai FLAC
````

### 📊 4) Indicateur probabiliste
La détection n’est jamais absolue :  
elle donne une probabilité, utile pour :
- vérifier des collections complètes,
- détecter les faux fichiers récupérés sur Internet,
- comparer plusieurs versions d’un même album.
Ce n’est pas un juge définitif, mais un très bon filtre de qualité.






