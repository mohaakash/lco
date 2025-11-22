#!/usr/bin/env python3
"""Extract text from a single page of a PDF.

Usage: python tools/extract_page.py [PDF_PATH] [PAGE_NUMBER]

If PAGE_NUMBER is omitted it defaults to 3 (third page). The script
prints the extracted text to stdout and writes it to tmp/kepler_page3.txt
when PDF_PATH points to docs/kepler.pdf.
"""
import sys
import os
from pathlib import Path


def extract_with_pypdf2(pdf_path, page_number):
    try:
        from PyPDF2 import PdfReader
    except Exception as e:
        raise
    reader = PdfReader(str(pdf_path))
    num = len(reader.pages)
    if page_number < 1 or page_number > num:
        raise ValueError(f"Page {page_number} out of range (1..{num})")
    page = reader.pages[page_number - 1]
    # use extract_text()
    text = page.extract_text()
    return text or ""


def extract_with_pdftotext(pdf_path, page_number):
    import subprocess
    # pdftotext supports -f and -l to limit pages, and - layout options
    cmd = ["pdftotext", "-f", str(page_number),
           "-l", str(page_number), str(pdf_path), "-"]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return out.decode('utf-8', errors='replace')
    except FileNotFoundError:
        raise
    except subprocess.CalledProcessError as e:
        return ""


def main():
    if len(sys.argv) > 1:
        pdf_path = Path(sys.argv[1])
    else:
        pdf_path = Path(__file__).resolve().parents[1] / 'docs' / 'kepler.pdf'

    page_number = 3
    if len(sys.argv) > 2:
        try:
            page_number = int(sys.argv[2])
        except Exception:
            pass

    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        sys.exit(2)

    text = None
    # Try PyPDF2 first
    try:
        text = extract_with_pypdf2(pdf_path, page_number)
    except Exception:
        text = None

    if not text:
        # Fallback to pdftotext if available
        try:
            text = extract_with_pdftotext(pdf_path, page_number)
        except FileNotFoundError:
            print(
                "Neither PyPDF2 nor pdftotext found. Install PyPDF2 (pip) or poppler-utils.")
            sys.exit(3)
    if not text:
        print("No text extracted from page. The page may be scanned image or use unusual encoding.")
        sys.exit(4)

    # Print to stdout and save to tmp file
    print(text)
    out_dir = Path('tmp')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{pdf_path.stem}_page{page_number}.txt"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Wrote extracted text to: {out_file}")


if __name__ == '__main__':
    main()
