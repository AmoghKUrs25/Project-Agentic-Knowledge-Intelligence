from app.agent.graph import agent

print("\n===== AGENTIC RAG TEST =====\n")

question = "What technologies are related to machine learning?"

print("Question:", question)

result = agent.invoke({
    "question": question,
    "route": "",
    "vector_results": [],
    "graph_results": [],
    "context": "",
    "answer": ""
})

print("\nRoute selected:")
print(result["route"])

print("\nKnowledge Graph results:")
print(result["graph_results"])

print("\nFinal Answer:")
print(result["answer"])

print("\n===== TEST COMPLETE =====")