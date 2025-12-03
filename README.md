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

### PIP
````bash
pip install -i https://test.pypi.org/simple --extra-index-url https://pypi.org/simple audio-inspector==0.1.0
````

---

## 🧪 Utilisation rapide

### Analyse simple
```bash
audio-inspector "path/musique.flac"
```
### Analyse + export du spectrogramme
```bash
audio-inspector "path/musique.flac" --plot
```
→ génère automatiquement :
```bash
out/musique_spectrogram.png
```
### Analyse + export JSON (pour automatiser ou intégrer dans un script)
```bash
audio-inspector "path/musique.flac" --json out/rapport.json
```
### Tout en même temps (spectrogramme + JSON + log terminal)
```bash
audio-inspector "path/musique.flac" --plot --json out/rapport.json --verbose
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






