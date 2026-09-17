from app.knowledge_graph.graph_store import KnowledgeGraph

graph = KnowledgeGraph()

print("Knowledge Graph test started...")

print("\nMachine Learning relationships:")
print(graph.search("Machine Learning"))

print("\nMachine Learning related nodes:")
print(graph.related_nodes("Machine Learning"))

print("\nCybersecurity relationships:")
print(graph.search("Cybersecurity"))

print("\nKnowledge Graph test successful!")