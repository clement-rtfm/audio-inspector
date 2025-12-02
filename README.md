# audio-inspector

# audio-inspector


Détecteur de faux FLAC & analyse audiophile (v1)


Outil CLI en Python pour analyser des fichiers audio (FLAC/WAV/MP3), générer des spectrogrammes, mesurer quelques métriques basiques et détecter si un FLAC est probablement un MP3 ré-encodé.


## Fonctionnalités
- Lecture de nombreux formats via `soundfile` / `librosa`
- Calcul de spectrogramme et export PNG
- Détection simple de lowpass (artefact typique des ré-encodages avec perte)
- Calcul RMS, peak, estimation approximative de Dynamic Range
- Export JSON avec métriques


## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
