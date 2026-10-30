import numpy as np
from sentence_transformers import SentenceTransformer
from ingest import build_chunks

model = SentenceTransformer("all-MiniLM-L6-v2")
chunks = build_chunks()[:200]

if not chunks:
    raise SystemExit("No chunks found. Put PDFs in the data/ folder first.")

texts = [c["text"] for c in chunks]
chunk_vecs = model.encode(texts)


def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


question = "What topics are covered in unit 2?"   # change this each run
q_vec = model.encode(question)

scores = [(cosine(q_vec, v), i) for i, v in enumerate(chunk_vecs)]
scores.sort(reverse=True)

for score, i in scores[:3]:
    print(round(score, 3), chunks[i]["source"], "page", chunks[i]["page"])
    print(texts[i][:200])
    print("---")
