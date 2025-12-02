#!/usr/bin/env python3
"""CLI pour audio-inspector"""
from pathlib import Path
import typer
from audioinspector.analysis import analyze_file


app = typer.Typer()


@app.command()
def analyze(
infile: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False),
plot: bool = typer.Option(False, "--plot", help="Exporter le spectrogramme PNG"),
json_out: Path = typer.Option(None, "--json", help="Chemin du fichier JSON de sortie"),
verbose: bool = typer.Option(True, "--verbose", help="Afficher le rapport dans le terminal"),
):
out = analyze_file(str(infile), plot=plot)
if json_out:
json_out.parent.mkdir(parents=True, exist_ok=True)
import json
with open(json_out, 'w', encoding='utf8') as f:
json.dump(out, f, ensure_ascii=False, indent=2)
if verbose:
# affiche résumé
print_report(out)




def print_report(out: dict):
print(f"[+] File: {out.get('path')}")
print(f"[+] Sample rate: {out.get('sr')} Hz | Channels: {out.get('channels')} | Bitdepth: {out.get('bitdepth')}")
app()
