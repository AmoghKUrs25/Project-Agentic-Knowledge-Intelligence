from app.rag.retriever import RAGRetriever


print("Starting RAG test...")

retriever = RAGRetriever()

results = retriever.search(
    "How many days of annual leave do employees receive?",
    k=3
)

print("\n========== SEARCH RESULTS ==========")

for result in results:

    print("\nSCORE:", result["score"])

    document = result["document"]

    print("SOURCE:", document["source"])

    print("TEXT:")
    print(document["text"])

print("\n========== RAG TEST COMPLETE ==========")