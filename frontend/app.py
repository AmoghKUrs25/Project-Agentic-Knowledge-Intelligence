import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.agent.graph import agent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Agentic Knowledge Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        opacity: 0.75;
        margin-bottom: 25px;
    }

    .status-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        text-align: center;
        margin-bottom: 10px;
    }

    .status-title {
        font-size: 14px;
        opacity: 0.7;
    }

    .status-value {
        font-size: 20px;
        font-weight: 600;
        margin-top: 5px;
    }

    .answer-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-top: 10px;
        margin-bottom: 20px;
    }

    .route-box {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🧠 System Architecture")

    st.markdown(
        """
        **Agent Pipeline**

        👤 User Query  
        ↓  
        🧠 LangGraph Agent  
        ↓  
        🔀 Query Router  
        ↓  
        📚 Vector RAG / 🔗 Knowledge Graph  
        ↓  
        🔍 Evidence Evaluation  
        ↓  
        🤖 Gemini  
        ↓  
        💬 Grounded Answer
        """
    )

    st.divider()

    st.markdown("### ⚡ System Status")

    st.success("RAG — READY")
    st.success("Knowledge Graph — READY")
    st.success("LangGraph — READY")
    st.success("Gemini — READY")
    st.success("MCP — READY")

    st.divider()

    st.markdown("### 🛠️ Technology Stack")

    st.markdown(
        """
        - Python
        - LangGraph
        - FAISS
        - Sentence Transformers
        - NetworkX
        - Gemini
        - MCP
        - Streamlit
        """
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🧠 Agentic Knowledge Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Hybrid RAG + Knowledge Graph + LangGraph + Gemini + MCP'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# STATUS CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">Vector Database</div>
            <div class="status-value">FAISS ✓</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">Knowledge Graph</div>
            <div class="status-value">NetworkX ✓</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">Agent Framework</div>
            <div class="status-value">LangGraph ✓</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">Tool Protocol</div>
            <div class="status-value">MCP ✓</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# QUERY SECTION
# ============================================================

st.markdown("## 🔎 Ask Your Knowledge Base")

question = st.text_input(
    "Enter your question",
    placeholder="Example: What technologies are related to machine learning?",
    label_visibility="collapsed"
)


ask_button = st.button(
    "🚀 Ask Agent",
    type="primary",
    use_container_width=False
)


# ============================================================
# AGENT EXECUTION
# ============================================================

if ask_button:

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("🧠 Agent is reasoning..."):

            result = agent.invoke(
                {
                    "question": question,
                    "route": "",
                    "vector_results": [],
                    "graph_results": [],
                    "context": "",
                    "answer": "",
                    "retry_count": 0
                }
            )


        st.divider()


        # ====================================================
        # ANSWER
        # ====================================================

        st.markdown("## 🤖 Agent Answer")

        st.markdown(
            f"""
            <div class="answer-box">
                {result["answer"]}
            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # AGENT DECISION
        # ====================================================

        st.markdown("## 🔀 Agent Decision")

        route = result.get("route", "unknown")

        if route == "hybrid":

            st.success(
                "HYBRID RETRIEVAL  •  Knowledge Graph + Vector RAG"
            )

        else:

            st.info(
                "VECTOR RETRIEVAL  •  Semantic RAG"
            )


        # ====================================================
        # EVIDENCE SCORE
        # ====================================================

        st.markdown("## 🔍 Evidence Evaluation")

        vector_results = result.get(
            "vector_results",
            []
        )

        if vector_results:

            best_score = max(
                item.get("score", 0.0)
                for item in vector_results
            )

            col_score, col_bar = st.columns(
                [1, 3]
            )

            with col_score:

                st.metric(
                    "Best Score",
                    f"{best_score:.3f}"
                )

            with col_bar:

                st.progress(
                    min(max(best_score, 0.0), 1.0)
                )

        else:

            st.warning(
                "No vector evidence was retrieved."
            )


        # ====================================================
        # KNOWLEDGE GRAPH
        # ====================================================

        graph_results = result.get(
            "graph_results",
            []
        )

        if graph_results:

            st.markdown(
                "## 🔗 Knowledge Graph Relationships"
            )

            graph_columns = st.columns(3)

            for index, node in enumerate(
                graph_results
            ):

                with graph_columns[
                    index % 3
                ]:

                    st.markdown(
                        f"• **{node}**"
                    )


        # ====================================================
        # SOURCES
        # ====================================================

        st.markdown("## 📚 Retrieved Sources")

        if vector_results:

            for index, item in enumerate(
                vector_results,
                start=1
            ):

                document = item["document"]

                source = document.get(
                    "source",
                    "Unknown source"
                )

                score = item.get(
                    "score",
                    0.0
                )

                with st.expander(
                    f"📄 Source {index}  •  "
                    f"{source}  •  "
                    f"Score: {score:.3f}"
                ):

                    st.write(
                        document.get(
                            "text",
                            ""
                        )
                    )

                    page = document.get(
                        "page"
                    )

                    if page:

                        st.caption(
                            f"Page {page}"
                        )

        else:

            st.write(
                "No sources available."
            )


        # ====================================================
        # SELF-CORRECTION
        # ====================================================

        st.markdown(
            "## ♻️ Retrieval Self-Correction"
        )

        retry_count = result.get(
            "retry_count",
            0
        )

        if retry_count > 0:

            st.warning(
                f"Retrieval was automatically improved. "
                f"Retry count: {retry_count}"
            )

        else:

            st.success(
                "Initial retrieval provided sufficient evidence."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Agentic Knowledge Intelligence System  •  "
    "LangGraph  •  FAISS  •  NetworkX  •  Gemini  •  MCP"
)