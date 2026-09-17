from app.rag.embeddings import EmbeddingModel

print("Starting embedding test...")

model = EmbeddingModel()

texts = [
    "Employees receive 24 days of annual paid leave.",
    "Machine learning is related to artificial intelligence."
]

embeddings = model.encode(texts)

print("\nEmbedding test successful!")
print("Number of texts:", len(texts))
print("Vector shape:", embeddings.shape)
print("First 5 values:")
print(embeddings[0][:5])