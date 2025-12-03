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

## 📦 Installation
```bash
# clonez le dépôt github sur l'appareil
git clone https://github.com/clement-rtfm/audio-inspector.git
# créer un environnement
python -m venv .venv
source .venv/bin/activate

# installation des dépendances
pip install -r requirements.txt
```

---

## 🧪 Utilisation rapide

### Analyse simple
```bash
python cli.py analyze musique.flac
```
### Analyse + export du spectrogramme
```bash
python cli.py analyze musique.flac --plot
```
→ génère automatiquement :
```bash
out/musique_spectrogram.png
```
### Analyse + export JSON (pour automatiser ou intégrer dans un script)
```bash
python cli.py analyze musique.flac --json out/rapport.json
```
### Tout en même temps (spectrogramme + JSON + log terminal)
```bash
python cli.py analyze musique.flac --plot --json out/rapport.json --verbose
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
