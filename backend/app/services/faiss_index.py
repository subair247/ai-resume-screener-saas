import faiss
import numpy as np

class FaissSearchIndex:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []

    def add_vector(self, vector: list, meta: dict):
        vec_np = np.array([vector]).astype("float32")
        self.index.add(vec_np)
        self.metadata.append(meta)

    def search(self, query_vector: list, k: int = 5):
        vec_np = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(vec_np, k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.metadata) and idx != -1:
                results.append({"meta": self.metadata[idx], "distance": float(dist)})
        return results

faiss_db = FaissSearchIndex()