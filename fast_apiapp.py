from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os

from extractor import extract_pdf

app = FastAPI(
    title="PDF Extractor API",
    version="1.0.0"
)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post("/extract")
async def extract(
    pdf: UploadFile = File(...)
):

    if not pdf.filename.endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )

    filepath = os.path.join(
        UPLOAD_FOLDER,
        pdf.filename
    )

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(
            pdf.file,
            buffer
        )

    result = extract_pdf(
        filepath
    )

    return {
        "success": True,
        "filename": result["filename"],
        "markdown": result["markdown"],
        "download_file": result["md_file"]
    }