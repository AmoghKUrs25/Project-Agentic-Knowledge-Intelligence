from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.rag.retriever import RAGRetriever
from app.knowledge_graph.graph_store import KnowledgeGraph
from app.llm.gemini import generate_answer
from app.agent.evaluator import evaluate_context


# ---------------------------------------------------------
# INITIALIZE COMPONENTS
# ---------------------------------------------------------

print("Loading RAG system...")

retriever = RAGRetriever()
knowledge_graph = KnowledgeGraph()

print("LangGraph Agent initialized successfully.")


# ---------------------------------------------------------
# AGENT STATE
# ---------------------------------------------------------

class AgentState(TypedDict):
    question: str
    route: str
    vector_results: list
    graph_results: list
    context: str
    answer: str
    retry_count: int


# ---------------------------------------------------------
# 1. QUERY ROUTER
# ---------------------------------------------------------

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
        "route": route,
        "retry_count": 0
    }


# ---------------------------------------------------------
# 2. VECTOR SEARCH
# ---------------------------------------------------------

def vector_search(state):

    question = state["question"]

    print("\nRunning vector retrieval...")

    results = retriever.search(
        question,
        k=5
    )

    print(f"Vector results retrieved: {len(results)}")

    return {
        "vector_results": results
    }


# ---------------------------------------------------------
# 3. KNOWLEDGE GRAPH SEARCH
# ---------------------------------------------------------

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

        print(f"\nSearching Knowledge Graph for: {entity}")

        results = knowledge_graph.related_nodes(entity)

    else:

        results = []

    print(f"Knowledge Graph results: {len(results)}")

    return {
        "graph_results": results
    }


# ---------------------------------------------------------
# 4. EVALUATE RETRIEVED EVIDENCE
# ---------------------------------------------------------

def evaluate_retrieval(state):

    results = state.get("vector_results", [])

    is_good = evaluate_context(results)

    if is_good:

        print("Evidence quality: GOOD")

    else:

        print("Evidence quality: WEAK")

    return {
        "retrieval_good": is_good
    }


# ---------------------------------------------------------
# 5. RETRY RETRIEVAL
# ---------------------------------------------------------

def retry_retrieval(state):

    retry_count = state.get("retry_count", 0) + 1

    original_question = state["question"]

    # Slightly expand the query to improve semantic retrieval
    improved_question = (
        original_question
        + " relevant information details policy technologies relationships"
    )

    print("\nSelf-correction activated.")
    print(f"Retry attempt: {retry_count}")
    print("Improved retrieval query:")
    print(improved_question)

    results = retriever.search(
        improved_question,
        k=5
    )

    print(f"Retry results retrieved: {len(results)}")

    return {
        "vector_results": results,
        "retry_count": retry_count
    }


# ---------------------------------------------------------
# 6. BUILD CONTEXT
# ---------------------------------------------------------

def build_context(state):

    context_parts = []

    # Vector retrieval context
    for result in state.get("vector_results", []):

        document = result["document"]

        context_parts.append(
            f"""
SOURCE: {document['source']}

{document['text']}
"""
        )

    # Knowledge graph context
    graph_results = state.get("graph_results", [])

    if graph_results:

        context_parts.append(
            "KNOWLEDGE GRAPH RELATIONSHIPS:\n"
            + ", ".join(graph_results)
        )

    context = "\n\n".join(context_parts)

    print("\nContext successfully built.")

    return {
        "context": context
    }


# ---------------------------------------------------------
# 7. GENERATE FINAL ANSWER
# ---------------------------------------------------------

def generate(state):

    print("\nGenerating final answer with Gemini...")

    answer = generate_answer(
        state["question"],
        state["context"]
    )

    print("Final answer generated successfully.")

    return {
        "answer": answer
    }


# ---------------------------------------------------------
# CREATE LANGGRAPH WORKFLOW
# ---------------------------------------------------------

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
    "evaluate_retrieval",
    evaluate_retrieval
)

workflow.add_node(
    "retry_retrieval",
    retry_retrieval
)

workflow.add_node(
    "build_context",
    build_context
)

workflow.add_node(
    "generate",
    generate
)


# ---------------------------------------------------------
# WORKFLOW CONNECTIONS
# ---------------------------------------------------------

workflow.add_edge(
    START,
    "router"
)


# Router decides retrieval strategy
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


# Hybrid route → graph → vector
workflow.add_edge(
    "graph_search",
    "vector_search"
)


# Vector retrieval → evaluator
workflow.add_edge(
    "vector_search",
    "evaluate_retrieval"
)


# ---------------------------------------------------------
# SELF-CORRECTION DECISION
# ---------------------------------------------------------

def retrieval_condition(state):

    good = state.get("retrieval_good", False)

    retry_count = state.get("retry_count", 0)

    if good:

        return "good"

    # Allow only one automatic retry
    if retry_count < 1:

        return "retry"

    return "good"


workflow.add_conditional_edges(
    "evaluate_retrieval",
    retrieval_condition,
    {
        "good": "build_context",
        "retry": "retry_retrieval"
    }
)


# Retry → evaluate again
workflow.add_edge(
    "retry_retrieval",
    "evaluate_retrieval"
)


# Context → Gemini
workflow.add_edge(
    "build_context",
    "generate"
)


# Gemini → END
workflow.add_edge(
    "generate",
    END
)


# ---------------------------------------------------------
# COMPILE AGENT
# ---------------------------------------------------------

agent = workflow.compile()

print("Self-correcting LangGraph Agent ready!")