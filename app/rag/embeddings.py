from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):
        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Embedding model loaded successfully.")

    def encode(self, texts):

        return self.model.encode(
            texts,
            normalize_embeddings=True
        )