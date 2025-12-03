import typer
from pathlib import Path
import json
from audioinspector.analysis import analyze_file

app = typer.Typer(
    name="audio-inspector",
    invoke_without_command=True,
    no_args_is_help=True,
    help="Audio Inspector – analyze audio files like a pro",
)


@app.command("analyze")
def analyze_cmd(
    infile: Path = typer.Argument(..., exists=True, help="Input audio file"),
    plot: bool = typer.Option(False, "--plot", help="Generate a spectrogram"),
    json_out: Path = typer.Option(None, "--json", help="Export JSON report"),
):
    """Analyze an audio file"""
    typer.echo(f"[+] Analyzing: {infile}")

    out = analyze_file(str(infile), plot=plot)
    print_report(out)

    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(out, indent=4))
        typer.echo(f"[+] JSON exported to {json_out}")


def print_report(out):
    print("\n===== AUDIO REPORT =====")
    for k, v in out.items():
        print(f"{k}: {v}")
    print("=========================")


if __name__ == "__main__":
    app()
