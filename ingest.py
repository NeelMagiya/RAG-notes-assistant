from pathlib import Path
from pypdf import PdfReader


def load_pdf_pages(path):
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append({"page": i + 1, "text": text})
    return pages


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        start += chunk_size - overlap
    return chunks


def build_chunks(data_dir="data", chunk_size=500, overlap=100):
    all_chunks = []
    for pdf in Path(data_dir).glob("*.pdf"):
        for page in load_pdf_pages(pdf):
            pieces = chunk_text(page["text"], chunk_size, overlap)
            for j, piece in enumerate(pieces):
                all_chunks.append({
                    "id": f"{pdf.stem}_p{page['page']}_c{j}",
                    "text": piece,
                    "source": pdf.name,
                    "page": page["page"],
                })
    return all_chunks


if __name__ == "__main__":
    chunks = build_chunks()
    print("Total chunks:", len(chunks))
    for c in chunks[:3]:
        print(c["id"], "->", c["text"][:150])
