import typer
from pathlib import Path
import json
from audioinspector.analysis import analyze_file

app = typer.Typer(name="audio-inspector", no_args_is_help=True)


@app.command()
def analyze(
    infile: Path = typer.Argument(..., exists=True),
    plot: bool = typer.Option(False, "--plot", help="Generate a spectrogram PNG"),
    json_out: Path = typer.Option(None, "--json", help="Export results to JSON"),
):
    """
    Analyze an audio file and print a detailed report.
    """
    typer.echo(f"[+] Analyzing: {infile} …")
    out = analyze_file(str(infile), plot=plot)

    # PRINT REPORT
    print_report(out)

    # WRITE JSON IF NEEDED
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(out, indent=4))
        typer.echo(f"[+] JSON exported to {json_out}")


def print_report(out: dict):
    print("")
    print("========== AUDIO REPORT ==========")
    print(f"File: {out.get('path')}")
    print(f"Sample rate: {out.get('samplerate')} Hz")
    print(f"Channels: {out.get('channels')}")
    print(f"Bit depth: {out.get('bitdepth')}")
    print("")
    print(f"RMS: {out.get('rms'):.2f} dB")
    print(f"Peak: {out.get('peak'):.2f} dB")
    print(f"DR (est.): {out.get('dr'):.1f}")
    print("")
    if out.get("lowpass"):
        print(f"[!] Lowpass detected around {out['lowpass']} Hz → possible lossy upscale.")
    else:
        print("[+] No lowpass detected.")
    print(f"FLAC Integrity Score: {out.get('flac_score')}/100")
    print("")
    if out.get("spectrogram_path"):
        print(f"[+] Spectrogram saved to: {out['spectrogram_path']}")

    print("==================================")


if __name__ == "__main__":
    app()
