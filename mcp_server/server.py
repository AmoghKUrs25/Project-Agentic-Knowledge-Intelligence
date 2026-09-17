from mcp.server import MCPServer

from app.rag.retriever import RAGRetriever
from app.knowledge_graph.graph_store import KnowledgeGraph


# ---------------------------------------------------------
# MCP SERVER
# ---------------------------------------------------------

mcp = MCPServer("Agentic Knowledge Server")


# ---------------------------------------------------------
# INITIALIZE RETRIEVAL SYSTEMS
# ---------------------------------------------------------

print("Loading MCP retrieval systems...")

retriever = RAGRetriever()
knowledge_graph = KnowledgeGraph()

print("MCP retrieval systems ready.")


# ---------------------------------------------------------
# MCP TOOL 1 — DOCUMENT SEARCH
# ---------------------------------------------------------

@mcp.tool()
def search_documents(query: str) -> str:
    """
    Search enterprise documents using semantic vector retrieval.
    """

    results = retriever.search(
        query,
        k=5
    )

    if not results:
        return "No relevant documents found."

    output = []

    for result in results:

        document = result["document"]

        output.append(
            f"""
SOURCE: {document['source']}
SCORE: {result['score']:.3f}

{document['text']}
"""
        )

    return "\n".join(output)


# ---------------------------------------------------------
# MCP TOOL 2 — KNOWLEDGE GRAPH SEARCH
# ---------------------------------------------------------

@mcp.tool()
def search_knowledge_graph(entity: str) -> str:
    """
    Search relationships in the enterprise knowledge graph.
    """

    results = knowledge_graph.related_nodes(entity)

    if not results:
        return f"No relationships found for: {entity}"

    return (
        f"Knowledge graph relationships for {entity}:\n"
        + "\n".join(f"- {item}" for item in results)
    )


# ---------------------------------------------------------
# SERVER ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":

    print("Starting Agentic Knowledge MCP Server...")

    mcp.run(
        transport="stdio"
    )