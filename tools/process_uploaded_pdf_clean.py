#!/usr/bin/env python3
"""Clean processor: extracts page text (via tools/extract_page.py) and computes elements using calc.element_calculator.

This avoids touching the existing potentially corrupted process_uploaded_pdf.py.
"""
import sys
from pathlib import Path
import json
import subprocess

# Ensure repo root is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('docs/kepler.pdf')
    if not pdf.exists():
        print(f"PDF not found: {pdf}")
        return 2

    try:
        # call the extractor script which prints the page text
        proc = subprocess.run(
            ["python3", "tools/extract_page.py", str(pdf)], capture_output=True)
        if proc.returncode != 0:
            print("Extractor failed:", proc.stderr.decode(
                'utf-8', errors='replace'))
            return 3
        text = proc.stdout.decode('utf-8', errors='replace')
    except Exception as e:
        print(f"Failed to run extractor: {e}")
        return 4

    try:
        from calc import element_calculator as ec
    except Exception as e:
        print(f"Failed to import element_calculator: {e}")
        return 5

    try:
        planets, scores, percentages = ec.process_text(text)
    except Exception as e:
        print(f"Error computing elements: {e}")
        return 6

    out = {'planets': planets, 'scores': scores, 'percentages': percentages}
    print(json.dumps(out, indent=2))
    out_file = Path('tmp') / f"{pdf.stem}_elements_clean.txt"
    out_file.parent.mkdir(exist_ok=True)
    out_file.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(f"Wrote results to: {out_file}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
