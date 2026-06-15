PDF Extractor

A Flask-based PDF extraction application that processes scientific PDFs and generates structured Markdown output.

## Features

- Upload PDF files through a web interface
- Extract text from scientific documents
- OCR processing for figures and images
- Generate Markdown output
- Download extracted results

## Technologies Used

- Flask
- Surya OCR
- Marker PDF
- Python

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

## Project Structure

```text
app.py
figure_ocr.py
templates/
├── index.html
└── result.html
uploads/
outputs/
```