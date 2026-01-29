# Simple OCR using Tesseract & EasyOCR

This is a simple OCR setup to test Optical Character Recognition with Tesseract (HP) and EasyOCR. Both open-sourced tools for document and image text extraction.

## Install

Tesseract installation is meant for Ubuntu / Unix machines:

```bash
sudo apt update
sudo apt install tesseract-ocr
pip install easyocr
pip install opencv-python # for grayscale and anti-noise pre-processing
```

## Run

```bash
python run_ocr.py --path '/path/to/image'
```

## Tesseract cheat sheet

When passing psm argument into tesseract configuration, we need to make sure we select the right one. Default is auto but takes more time and could not be as accurate as others.

```bash
# Example use
text = pytesseract.image_to_string(thresh, config="--psm 6")
```

| PSM  | Use case                  |
| ---- | ------------------------- |
| `3`  | Fully automatic (default) |
| `4`  | Multiple columns          |
| `6`  | Single text block ⭐      |
| `11` | Sparse text               |
| `13` | Raw line (no layout)      |