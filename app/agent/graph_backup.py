from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.rag.retriever import RAGRetriever
from app.knowledge_graph.graph_store import KnowledgeGraph
from app.llm.gemini import generate_answer


# Create retrieval components
retriever = RAGRetriever()
knowledge_graph = KnowledgeGraph()


class AgentState(TypedDict):
    question: str
    route: str
    vector_results: list
    graph_results: list
    context: str
    answer: str


# -----------------------------
# 1. QUERY ROUTER
# -----------------------------

def route_query(state):
    question = state["question"].lower()

    graph_keywords = [
        "related",
        "relationship",
        "connected",
        "technologies",
        "associated",
        "connection"
    ]

    if any(keyword in question for keyword in graph_keywords):
        route = "hybrid"
    else:
        route = "vector"

    print(f"Agent route selected: {route}")

    return {
        "route": route
    }


# -----------------------------
# 2. VECTOR SEARCH
# -----------------------------

def vector_search(state):

    results = retriever.search(
        state["question"],
        k=5
    )

    return {
        "vector_results": results
    }


# -----------------------------
# 3. KNOWLEDGE GRAPH SEARCH
# -----------------------------

def graph_search(state):

    question = state["question"].lower()

    entity = None

    if "machine learning" in question:
        entity = "Machine Learning"

    elif "cybersecurity" in question:
        entity = "Cybersecurity"

    elif "cloud" in question:
        entity = "Cloud Computing"

    elif "training" in question:
        entity = "Training"

    if entity:
        results = knowledge_graph.related_nodes(entity)
    else:
        results = []

    return {
        "graph_results": results
    }


# -----------------------------
# 4. BUILD CONTEXT
# -----------------------------

def build_context(state):

    context_parts = []

    # Add vector evidence
    for result in state.get("vector_results", []):

        document = result["document"]

        context_parts.append(
            f"""
SOURCE: {document["source"]}

{document["text"]}
"""
        )

    # Add graph evidence
    graph_results = state.get(
        "graph_results",
        []
    )

    if graph_results:

        context_parts.append(
            "KNOWLEDGE GRAPH RELATIONSHIPS:\n"
            + ", ".join(graph_results)
        )

    return {
        "context": "\n\n".join(context_parts)
    }


# -----------------------------
# 5. GENERATE ANSWER
# -----------------------------

def generate(state):

    answer = generate_answer(
        state["question"],
        state["context"]
    )

    return {
        "answer": answer
    }


# -----------------------------
# BUILD LANGGRAPH WORKFLOW
# -----------------------------

workflow = StateGraph(AgentState)

workflow.add_node(
    "router",
    route_query
)

workflow.add_node(
    "vector_search",
    vector_search
)

workflow.add_node(
    "graph_search",
    graph_search
)

workflow.add_node(
    "build_context",
    build_context
)

workflow.add_node(
    "generate",
    generate
)


# Starting point
workflow.add_edge(
    START,
    "router"
)


# Routing decision
def route_condition(state):

    if state["route"] == "hybrid":
        return "hybrid"

    return "vector"


workflow.add_conditional_edges(
    "router",
    route_condition,
    {
        "vector": "vector_search",
        "hybrid": "graph_search"
    }
)


# Hybrid path
workflow.add_edge(
    "graph_search",
    "vector_search"
)


# Both paths eventually build context
workflow.add_edge(
    "vector_search",
    "build_context"
)

workflow.add_edge(
    "build_context",
    "generate"
)

workflow.add_edge(
    "generate",
    END
)


# Compile the agent
agent = workflow.compile()

print("LangGraph Agent initialized successfully.")