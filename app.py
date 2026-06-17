from flask import (
    Flask,
    render_template,
    request,
    send_file,
    jsonify
)

import os
import markdown

from extractor import extract_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
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

    result = extract_pdf(
        filepath
    )

    LAST_MD = result["md_file"]

    html_content = markdown.markdown(
        result["markdown"],
        extensions=[
            "tables",
            "fenced_code"
        ]
    )

    # Updated to include pdf_file parameter
    return render_template(
        "result.html",
        html_content=html_content,
        pdf_file=pdf.filename
    )


# New route to serve uploaded PDFs
@app.route("/pdf/<filename>")
def serve_pdf(filename):

    return send_file(
        os.path.join(
            UPLOAD_FOLDER,
            filename
        )
    )


@app.route(
    "/extract",
    methods=["POST"]
)
def extract_api():

    if "pdf" not in request.files:

        return jsonify({
            "success": False,
            "error": "No PDF uploaded"
        }), 400

    pdf = request.files["pdf"]

    if pdf.filename == "":

        return jsonify({
            "success": False,
            "error": "No PDF selected"
        }), 400

    filepath = os.path.join(
        UPLOAD_FOLDER,
        pdf.filename
    )

    pdf.save(filepath)

    result = extract_pdf(
        filepath
    )

    return jsonify({
        "success": True,
        "filename": result["filename"],
        "markdown": result["markdown"],
        "download_file": result["md_file"]
    })


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


@app.route("/health")
def health():

    return {
        "status": "ok"
    }


if __name__ == "__main__":

    app.run(
        debug=True
    )