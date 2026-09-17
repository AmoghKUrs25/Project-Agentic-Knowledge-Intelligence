from app.rag.ingest import load_documents, chunk_text
from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore


class RAGRetriever:

    def __init__(self):

        print("Loading documents...")

        self.embedding_model = EmbeddingModel()

        raw_documents = load_documents()

        self.chunks = []

        for document in raw_documents:

            chunks = chunk_text(
                document["text"]
            )

            for chunk in chunks:

                self.chunks.append({
                    "text": chunk,
                    "source": document["source"],
                    "page": document.get("page")
                })

        print("Number of chunks:", len(self.chunks))

        print("Creating embeddings...")

        embeddings = self.embedding_model.encode(
            [item["text"] for item in self.chunks]
        )

        self.vector_store = VectorStore(
            dimension=embeddings.shape[1]
        )

        self.vector_store.add(
            embeddings,
            self.chunks
        )

        print("RAG vector store ready!")

    def search(self, query, k=5):

        query_embedding = self.embedding_model.encode(
            [query]
        )[0]

        return self.vector_store.search(
            query_embedding,
            k
        )