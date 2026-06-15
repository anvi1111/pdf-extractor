import requests

with open("sample.pdf", "rb") as f:

    response = requests.post(
        "http://127.0.0.1:5000/extract",
        files={
            "pdf": f
        }
    )

print(response.json())