import pdfplumber
import os
import warnings
warnings.filterwarnings("ignore")


PDF_DIR = "../pdfs/bennett"
TEXT_DIR = "../text/bennett"

os.makedirs(TEXT_DIR, exist_ok=True)

def clean_text(text):
    if not text:
        return ""
    # Remove excessive newlines
    text = text.replace("\n\n\n", "\n\n")
    # Remove page numbers like "Page 3 of 23"
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        if "Page" in line and "of" in line:
            continue
        cleaned.append(line.strip())
    return "\n".join(cleaned)

for file in os.listdir(PDF_DIR):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(PDF_DIR, file)
        txt_path = os.path.join(TEXT_DIR, file.replace(".pdf", ".txt"))

        full_text = ""

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                full_text += clean_text(text) + "\n\n"

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"Converted: {file}")
