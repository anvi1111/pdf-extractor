
import os
import sys
import subprocess
from pathlib import Path

OUTPUT_FOLDER = "outputs"


def extract_pdf(pdf_path):

    pdf_path = os.path.abspath(pdf_path)

    # Run Marker
    subprocess.run(
        [
            "marker_single",
            pdf_path,
            "--output_dir",
            OUTPUT_FOLDER
        ],
        check=True
    )

    pdf_name = Path(pdf_path).stem

    md_file = None

    # Find generated markdown
    for md in Path(OUTPUT_FOLDER).rglob("*.md"):

        if pdf_name.lower() in str(md).lower():

            md_file = str(md)
            break

    if md_file is None:

        raise Exception(
            "Markdown file not found."
        )

    # Run figure OCR
    script_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "figure_ocr.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            script_path,
            md_file
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        raise Exception(
            f"Figure OCR failed:\n{result.stderr}"
        )

    # Read markdown
    with open(
        md_file,
        "r",
        encoding="utf-8"
    ) as f:

        markdown_text = f.read()

    return {
        "success": True,
        "markdown": markdown_text,
        "md_file": md_file,
        "filename": os.path.basename(pdf_path)
    }
