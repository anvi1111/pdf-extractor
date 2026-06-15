from flask import (
    Flask,
    render_template,
    request,
    send_file
)

import subprocess
import sys
import os
from pathlib import Path
import markdown
import re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

LAST_MD = None


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    global LAST_MD

    if "pdf" not in request.files:

        return "No PDF uploaded"

    pdf = request.files["pdf"]

    if pdf.filename == "":

        return "No PDF selected"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        pdf.filename
    )

    pdf.save(filepath)

    print(
        f"Processing: {filepath}"
    )

    subprocess.run(
        [
            "marker_single",
            filepath,
            "--output_dir",
            OUTPUT_FOLDER
        ],
        check=True
    )

    pdf_name = Path(
        filepath
    ).stem

    md_file = None

    for md in Path(
        OUTPUT_FOLDER
    ).rglob("*.md"):

        if pdf_name.lower() in str(md).lower():

            md_file = str(md)
            break

    print(
        "FOUND MD:",
        md_file
    )

    if md_file is None:

        return "Markdown file not found."

    script_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
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

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    if result.returncode != 0:

        return f"figure_ocr.py failed:\n{result.stderr}"

    output_dir = os.path.dirname(
        md_file
    )

    print(
        "OUTPUT DIR:",
        output_dir
    )

    print("FILES:")

    for f in os.listdir(
        output_dir
    ):

        print(
            "   ",
            f
        )

    LAST_MD = md_file

    with open(
        md_file,
        "r",
        encoding="utf-8"
    ) as f:

        extracted_text = f.read()

    print(
        "TEXT LENGTH:",
        len(extracted_text)
    )

    html_content = markdown.markdown(
        extracted_text,
        extensions=[
            "tables",
            "fenced_code"
        ]
    )

    return render_template(
        "result.html",
        html_content=html_content
    )


@app.route("/download/md")
def download_md():

    if LAST_MD is None:

        return (
            "No markdown file available."
        )

    return send_file(
        LAST_MD,
        as_attachment=True
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )