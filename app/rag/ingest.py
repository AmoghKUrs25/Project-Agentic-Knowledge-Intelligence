from pathlib import Path
from pypdf import PdfReader


def load_documents(directory="data/documents"):
    documents = []

    for file in Path(directory).glob("*"):

        if file.suffix.lower() == ".txt":
            text = file.read_text(encoding="utf-8")

            documents.append({
                "text": text,
                "source": file.name
            })

        elif file.suffix.lower() == ".pdf":
            reader = PdfReader(str(file))

            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""

                documents.append({
                    "text": text,
                    "source": file.name,
                    "page": page_number
                })

    return documents


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks