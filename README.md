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
# PDF Extractor

A robust PDF extraction application that processes scientific and technical PDFs and generates structured Markdown output, including images and tables. It leverages **Marker PDF** for text extraction and **Surya OCR** for optical character recognition of figures.

The project provides both a **Flask-based web interface** and a **FastAPI-based REST API** for flexibility.

## Features

- **Web Interface:** Upload PDF files and view extracted Markdown with rendered HTML.
- **REST APIs:** Programmatic extraction endpoints via Flask or FastAPI.
- **Advanced Text Extraction:** Built on top of Marker PDF for precise document parsing.
- **Figure OCR:** Integrates Surya OCR to capture text within images and figures.
- **Markdown Generation:** Downloads results in clean, structured Markdown format.

## Technologies Used

- [Flask](https://flask.palletsprojects.com/) (Web UI & API)
- [FastAPI](https://fastapi.tiangolo.com/) (High-performance API)
- [Marker PDF](https://github.com/VikParuchuri/marker)
- [Surya OCR](https://github.com/VikParuchuri/surya)
- Python 3.x

## Installation

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

*(Note: Depending on your system and Marker/Surya requirements, you may need to install additional system-level dependencies for OCR and PDF processing.)*

## Usage

### 1. Flask Web Application
The Flask application provides a user-friendly web interface and basic API endpoints.

**Run the Flask App:**
```bash
python app.py
```
- Web Interface: `http://127.0.0.1:5000/`
- API Endpoint: `http://127.0.0.1:5000/extract`

### 2. FastAPI Application
The FastAPI app provides a modern, fast API with built-in Swagger documentation.

**Run the FastAPI App:**
```bash
uvicorn fast_apiapp:app --reload
```
- Swagger UI Documentation: `http://127.0.0.1:8000/docs`
- API Endpoint: `http://127.0.0.1:8000/extract`

## API Documentation

Both the Flask and FastAPI servers offer a `/extract` endpoint for programmatic PDF extraction.

### Extract PDF Endpoint

**Endpoint:** `/extract`  
**Method:** `POST`  
**Content-Type:** `multipart/form-data`

**Request:**
Send a PDF file using the `pdf` form field.

**Python Example:**
```python
import requests

with open("sample.pdf", "rb") as f:
    response = requests.post(
        "http://127.0.0.1:5000/extract", # or http://127.0.0.1:8000/extract for FastAPI
        files={"pdf": f}
    )

print(response.json())
```

**Response Format:**
```json
{
    "success": true,
    "filename": "sample.pdf",
    "markdown": "# Extracted Content\n\n...",
    "download_file": "outputs/sample_md/sample.md"
}
```

## Project Structure

```text
.
├── app.py              # Flask application (Web UI + API)
├── fast_apiapp.py      # FastAPI application (API only)
├── extractor.py        # Core logic calling Marker PDF and Figure OCR
├── figure_ocr.py       # OCR processing logic using Surya OCR
├── test_api.py         # Sample script to test the /extract API
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates for Flask UI
│   ├── index.html
│   └── result.html
├── uploads/            # Temporary directory for uploaded PDFs
└── outputs/            # Directory where extracted Markdown files are saved
```
