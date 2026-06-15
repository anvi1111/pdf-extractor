import re
import sys
import os

from PIL import Image

from surya.foundation import FoundationPredictor
from surya.detection import DetectionPredictor
from surya.recognition import RecognitionPredictor

print("Loading Surya...")

foundation = FoundationPredictor()

detector = DetectionPredictor()

recognizer = RecognitionPredictor(
    foundation_predictor=foundation
)

print("Surya Ready")


def ocr_image(image_path):

    img = Image.open(image_path)

    predictions = recognizer(
        [img],
        det_predictor=detector,
        math_mode=False,
        sort_lines=True
    )

    if not predictions:
        return ""

    result = predictions[0]

    lines = []

    for line in result.text_lines:

        text = line.text.strip()

        if text:
            lines.append(text)

    return "\n".join(lines)


md_file = sys.argv[1]

output_dir = os.path.dirname(md_file)

with open(
    md_file,
    "r",
    encoding="utf-8"
) as f:

    markdown_text = f.read()

images = re.findall(
    r'!\[\]\((.*?)\)',
    markdown_text
)

for image_name in images:

    image_path = os.path.join(
        output_dir,
        image_name
    )

    if not os.path.exists(image_path):
        continue

    print(
        "OCR:",
        image_name
    )

    ocr_text = ocr_image(
        image_path
    )

    if len(ocr_text.strip()) < 5:
        continue

    markdown_text = markdown_text.replace(
        f"![]({image_name})",
        f"""

### Figure OCR

{ocr_text}

"""
    )

with open(
    md_file,
    "w",
    encoding="utf-8"
) as f:

    f.write(markdown_text)

print("Done")
