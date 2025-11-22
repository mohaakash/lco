#!/usr/bin/env python3
"""Process an uploaded PDF: extract page 3, format text and compute element percentages.

Usage: python tools/process_uploaded_pdf.py [PDF_PATH]

If no PDF_PATH provided it defaults to docs/kepler.pdf. Outputs results to stdout
and writes a small JSON-like text file to tmp/kepler_elements.txt
"""
import sys
from pathlib import Path
import json
import subprocess


# Ensure repository root is on sys.path so we can import calc.*
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('docs/kepler.pdf')
    if not pdf.exists():
        print(f"PDF not found: {pdf}")
        return 2

    # Import element calculator after ensuring sys.path so local package resolves
    try:
        from calc import element_calculator as ec
    except Exception as ie:
        print(f"Failed to import element_calculator: {ie}")
        return 6

    # Prefer PyMuPDF path (ec.process_kepler_pdf) but fall back to the
    # standalone extractor which uses PyPDF2/pdftotext if PyMuPDF isn't installed.
    try:
        planets, scores, percentages = ec.process_kepler_pdf(str(pdf))
    except Exception:
        # Try fallback: call tools/extract_page.py to get page text
        try:
            proc = subprocess.run(
                ["python3", "tools/extract_page.py", str(pdf)], capture_output=True)
            if proc.returncode != 0:
                print("Extractor failed:", proc.stderr.decode(
                    'utf-8', errors='replace'))
                return 4
            text = proc.stdout.decode('utf-8', errors='replace')
            # Now process text directly
            planets, scores, percentages = ec.process_text(text)
        except Exception as e2:
            print(f"Error processing PDF with fallback: {e2}")
            return 5

    out = {
        'planets': planets,
        'scores': scores,
        'percentages': percentages
    }

    print(json.dumps(out, indent=2))
    out_dir = Path('tmp')
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"{pdf.stem}_elements.txt"
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print(f"Wrote results to: {out_file}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
