import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension=384):
        self.index = faiss.IndexFlatIP(dimension)
        self.documents = []

    def add(self, embeddings, documents):

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)

        self.documents.extend(documents)

    def search(self, query_embedding, k=5):

        if len(self.documents) == 0:
            return []

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        k = min(k, len(self.documents))

        scores, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index == -1:
                continue

            results.append({
                "score": float(score),
                "document": self.documents[index]
            })

        return results