from pathlib import Path
import typer
from audioinspector.analysis import analyze_file, print_report
import json

app = typer.Typer(help="Audio Inspector CLI")

@app.command()
def analyze(
    infile: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False),
    plot: bool = typer.Option(False, "--plot", help="Exporter le spectrogramme PNG"),
    json_out: Path = typer.Option(None, "--json", help="Chemin du fichier JSON de sortie"),
    verbose: bool = typer.Option(True, "--verbose", help="Afficher le rapport dans le terminal"),
):
    """Analyse un fichier audio et génère un rapport"""
    out = analyze_file(str(infile), plot=plot)
    
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        with open(json_out, 'w', encoding='utf8') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
    
    if verbose:
        print_report(out)

# ✅ Le point d'entrée pour Typer
if __name__ == "__main__":
    app()
