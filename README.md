


# 🧠 Agentic Knowledge Intelligence System

An AI-powered enterprise knowledge assistant that combines **Agentic RAG, Vector Search, Knowledge Graphs, LangGraph, Gemini, MCP, and Streamlit** to provide grounded and explainable answers from a knowledge base.

---



## 🚀 Overview

Traditional RAG systems retrieve documents and generate answers using a fixed pipeline.

This project introduces an **agentic retrieval workflow** where the system decides how to retrieve information based on the user's question.

The agent can:

- Route queries to vector retrieval
- Perform knowledge graph retrieval for relationship-based questions
- Combine vector and graph evidence
- Evaluate retrieval quality
- Automatically retry weak retrieval
- Generate grounded answers using Gemini
- Expose retrieval capabilities through MCP tools
- Display evidence, sources, scores, and agent decisions through a Streamlit UI

---





## 🏗️ System Architecture

```text
                    ┌─────────────────┐
                    │    User Query   │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   LangGraph Agent   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    Query Router     │
                  └──────────┬──────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
       ┌────────────────┐       ┌──────────────────┐
       │   Vector RAG   │       │ Knowledge Graph  │
       │ FAISS + ST     │       │    NetworkX      │
       └───────┬────────┘       └─────────┬────────┘
               │                          │
               └──────────┬───────────────┘
                          ▼
                ┌─────────────────────┐
                │ Evidence Evaluation │
                └──────────┬──────────┘
                           │
                     Weak Evidence?
                       /         \
                     Yes          No
                     │             │
                     ▼             │
              ┌─────────────┐      │
              │ Self-Correct │──────┘
              │ & Re-retrieve│
              └─────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Gemini LLM      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Grounded Answer │
                  │ + Evidence      │
                  └─────────────────┘







✨ Key Features
1. Agentic Query Routing

The LangGraph agent analyzes the user's question and selects an appropriate retrieval strategy.

User Query
    ↓
LangGraph Agent
    ↓
Query Router
    ├── Vector Retrieval
    └── Hybrid Retrieval
          ├── Vector Search
          └── Knowledge Graph





2. Semantic Vector Search

Documents are:

Loaded from the knowledge base
Split into chunks
Converted into embeddings
Stored in a FAISS vector index
Retrieved using semantic similarity




Embedding model:

sentence-transformers/all-MiniLM-L6-v2

Vector database/index:

FAISS





3. Knowledge Graph Retrieval

The system maintains relationships between entities using NetworkX.

Example:

Machine Learning
├── Artificial Intelligence
├── Data Science
├── Python
├── PyTorch
├── TensorFlow
├── Cloud Computing
└── Training

This allows the system to answer relationship-oriented questions.

Example:

What technologies are related to machine learning?

The agent can use the knowledge graph to identify related technologies.






4. Hybrid Retrieval

For relationship-oriented queries, the agent combines:

Vector Evidence
       +
Knowledge Graph Relationships
       ↓
Combined Context
       ↓
Gemini
       ↓
Grounded Answer

This allows the system to use both semantic document evidence and structured relationships.





5. Evidence Evaluation

Retrieved evidence is evaluated before answer generation.

The system checks the retrieval score and determines whether the retrieved information is sufficiently relevant.

Retrieved Evidence
       ↓
Quality Evaluation
       │
       ├── Good → Generate Answer
       │
       └── Weak → Retry Retrieval





6. Self-Correcting Retrieval

When retrieval quality is weak, the agent automatically modifies the query and performs another retrieval attempt.

Example:

Original Query
      ↓
Vector Retrieval
      ↓
Weak Evidence
      ↓
Self-Correction
      ↓
Improved Query
      ↓
Re-retrieval
      ↓
Context
      ↓
Gemini

This provides an agentic feedback loop instead of relying on a single retrieval attempt.




7. Grounded Answer Generation

Gemini receives the retrieved evidence as context.

The generation prompt instructs the model to:

Use supplied evidence
Avoid inventing facts
Return a knowledge-base limitation when evidence is insufficient

Example:

The available knowledge base does not contain enough information.

This reduces unsupported answers.





8. MCP Integration

The project exposes retrieval capabilities through Model Context Protocol (MCP).

Available MCP tools:

search_documents
search_knowledge_graph

These tools allow external MCP-compatible agents or clients to access the project's retrieval capabilities.






9. Interactive Streamlit UI

The Streamlit interface provides:

Knowledge base querying
Agent decisions
Retrieval strategy
Evidence evaluation score
Knowledge graph relationships
Retrieved sources
Retrieval self-correction status
System component status




🛠️ Technology Stack

Technology	Purpose
Python	Core development
LangGraph	Agent orchestration
LangChain	AI/RAG ecosystem
Sentence Transformers	Text embeddings
FAISS	Vector similarity search
NetworkX	Knowledge graph
Gemini	LLM answer generation
MCP	Tool interoperability
Streamlit	User interface
FastAPI	API-ready backend support
Docker	Containerization
NumPy	Numerical operations
PyPDF	PDF document ingestion







📁 Project Structure
agentic-knowledge-intelligence/
│
├── app/
│   ├── agent/
│   │   ├── graph.py
│   │   ├── evaluator.py
│   │   └── graph_backup.py
│   │
│   ├── knowledge_graph/
│   │   └── graph_store.py
│   │
│   ├── llm/
│   │   └── gemini.py
│   │
│   └── rag/
│       ├── embeddings.py
│       ├── ingest.py
│       ├── retriever.py
│       └── vector_store.py
│
├── data/
│   └── documents/
│       └── company_policy.txt
│
├── frontend/
│   └── app.py
│
├── mcp_server/
│   └── server.py
│
├── tests/
│   └── evaluation.py
│
├── Dockerfile
├── README.md
├── requirements.txt
├── .env
└── .gitignore







⚙️ Installation



1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd agentic-knowledge-intelligence


2. Create a virtual environment

Windows PowerShell:

python -m venv venv

Activate it:

.\venv\Scripts\Activate.ps1


3. Install dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file:

GEMINI_API_KEY=your_gemini_api_key

Never commit the .env file to GitHub.




▶️ Run the Application

From the project root:

streamlit run frontend/app.py

Then open:

http://localhost:8501




🐳 Run with Docker

Build the image:

docker build -t agentic-knowledge-intelligence:1.0 .

Run the container:

docker run -d --name agentic-knowledge-intelligence -p 8501:8501 --env-file .env agentic-knowledge-intelligence:1.0

Verify:

docker ps

The application will be available at:

http://localhost:8501




🧪 Evaluation

The retrieval system was evaluated using five knowledge-base questions.

Test	Result
Annual paid leave allowance	PASS
Service leave eligibility	PASS
Technical training	        PASS
Password security requirements	PASS
Machine learning technologies	PASS
Evaluation Result
Tests Passed: 5/5
Evaluation Accuracy: 100%

The evaluation measures whether the expected information was successfully retrieved for the defined test questions.



🔍 Example Queries

Policy Query
What is the annual paid leave allowance?

Expected retrieval strategy:

Vector RAG
Relationship Query
What technologies are related to machine learning?

Expected retrieval strategy:

Hybrid

The system can combine vector evidence with knowledge graph relationships.

Unknown Information
What is the company policy for pet insurance?

The system can identify insufficient evidence and return:

The available knowledge base does not contain enough information.




🔄 Agent Workflow

The complete workflow is:

1. Receive user question
          ↓
2. Analyze query
          ↓
3. Select retrieval strategy
          ↓
4. Retrieve relevant evidence
          ↓
5. Evaluate evidence quality
          ↓
6. Retry retrieval if evidence is weak
          ↓
7. Build grounded context
          ↓
8. Generate answer using Gemini
          ↓
9. Display answer + evidence




💡 Why This Project Is Different

This project goes beyond a basic chatbot or traditional RAG pipeline.

Traditional RAG
Query
 ↓
Vector Search
 ↓
LLM
 ↓
Answer
This Project
Query
 ↓
Agent
 ↓
Routing
 ↓
Vector / Graph / Hybrid Retrieval
 ↓
Evidence Evaluation
 ↓
Self-Correction
 ↓
Grounded Generation
 ↓
Answer + Evidence

The architecture demonstrates concepts used in modern AI Agent and Retrieval-Augmented Generation systems.





🎯 Learning Outcomes

This project demonstrates practical experience with:

Agentic AI
Retrieval-Augmented Generation
Semantic search
Vector databases
Knowledge graphs
Graph-based retrieval
LangGraph workflows
LLM integration
Retrieval evaluation
Self-correcting agents
MCP tool development
Streamlit application development
Docker containerization





🔮 Future Improvements

Potential extensions include:

Persistent vector database
Larger enterprise document collections
Advanced query classification
Reranking models
Hybrid search scoring
Knowledge graph extraction from documents
Authentication and authorization
REST API deployment
Observability and tracing
Automated evaluation benchmarks
Cloud deployment




👨‍💻 Author

Amogh K Urs

Computer Science & Engineering

Interested in:
Artificial Intelligence
AI Agents
RAG Systems
Backend Development
DevOps
Software Engineering