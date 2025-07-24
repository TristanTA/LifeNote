import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class FolderRetriever:
    def __init__(self):
        self.index = None
        self.paths = []

    def build(self, folder_pairs):
        # folder_pairs: list of (folder_path, summary)
        self.paths = [fp for fp, _ in folder_pairs]
        vecs = embed_model.encode([summ for _, summ in folder_pairs], normalize_embeddings=True)
        dim = vecs.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(vecs.astype(np.float32))

    def top_k(self, query_text, k=5):
        qvec = embed_model.encode([query_text], normalize_embeddings=True).astype(np.float32)
        D, I = self.index.search(qvec, k)
        return [(self.paths[i], float(D[0][rank])) for rank, i in enumerate(I[0])]