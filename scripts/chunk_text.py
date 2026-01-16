import os
import json

TEXT_DIR = "../text/bennett"
OUT_DIR = "../processed/bennett"
os.makedirs(OUT_DIR, exist_ok=True)

CHUNK_MIN = 150
CHUNK_MAX = 300

def guess_domain(filename):
    name = filename.lower()
    if "exam" in name or "supplement" in name:
        return "examination"
    if "hostel" in name:
        return "hostel"
    if "conduct" in name or "discipline" in name:
        return "discipline"
    if "grievance" in name:
        return "grievance"
    if "ragging" in name:
        return "anti_ragging"
    if "calendar" in name:
        return "calendar"
    return "academics"

def chunk_text(text):
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
    chunks = []

    current = ""
    for p in paragraphs:
        words = p.split()
        if len(current.split()) + len(words) <= 200:
            current += " " + p
        else:
            chunks.append(current.strip())
            current = p

    if current.strip():
        chunks.append(current.strip())

    return chunks


all_chunks = []

for file in os.listdir(TEXT_DIR):
    if file.endswith(".txt"):
        with open(os.path.join(TEXT_DIR, file), "r", encoding="utf-8") as f:
            text = f.read()

        domain = guess_domain(file)
        chunks = chunk_text(text)

        for idx, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{file}_{idx}",
                "text": chunk,
                "domain": domain,
                "source": file
            })

out_path = os.path.join(OUT_DIR, "chunks.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2)

print(f"Created {len(all_chunks)} chunks")
