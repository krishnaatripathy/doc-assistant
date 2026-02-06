from pypdf import PdfReader
import os

UPLOAD_DIR = "data/uploads"
OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_file(filename):
    input_path = os.path.join(UPLOAD_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, f"{filename}.txt")

    text = ""

    if filename.lower().endswith(".pdf"):
        reader = PdfReader(input_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    elif filename.lower().endswith(".txt"):
        with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    else:
        raise ValueError("Unsupported file type")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return output_path

