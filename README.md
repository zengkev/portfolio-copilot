# 🧠 LangChain AI Orchestration & Next.js Interface

Welcome to the **LangChain AI Architecture** platform—a production-ready, enterprise-grade cognitive orchestration framework. This repository integrates a high-performance **Python-based LangChain backend** (orchestrating document parsing, semantic chunking, high-dimensional vector embeddings, and real-time agentic reasoning loops) with a state-of-the-art **Next.js 15 frontend web console** powered by TailwindCSS, TypeScript, and Next.js App Router compilation.

Deterministic, multi-environment deployments are managed via **Docker Compose** (for database, vector store, and supporting containerized services) and **Conda** virtual environment configurations, ensuring absolute parity between local development and cloud production platforms.

---

## 🏗️ System Architecture

The platform's logical blueprint is built upon four decoupled, highly specialized layers designed to guarantee high concurrency, low latency, and modular scalability:

```
  ┌────────────────────────────────────────────────────────┐
  │              Frontend User Experience Layer            │
  │     Next.js Web Console (App Router, Tailwind, TS)     │
  └──────────────────────────┬─────────────────────────────┘
                             │ (REST / Real-time SSE / MCP Streams)
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │                 Modular Service Layer                  │
  │      Python API Gateway (`backend/main.py` FastAPI)    │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │                 AI Orchestration Core                  │
  │     LangChain Execution Engine (ReAct Agent Loops)     │
  │        (Agent Tools, Memory Pools, Model Routing)      │
  └──────────────────────────┬─────────────────────────────┘
                             │ (ETL Pipeline Ingestion)
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │               Enterprise Data Pipeline                 │
  │  Unstructured Document Parsing (`Offering_Plan_Final.pdf`)│
  │   Deterministic Token Chunking & Vector DB Embeddings  │
  └────────────────────────────────────────────────────────┘
```

1. **Enterprise Data Pipeline (Ingestion & ETL)**
   * **`backend/ingest.py`**: Controls the ingestion pipeline. It parses complex, unstructured target assets (e.g., **`backend/Offering_Plan_Final.pdf`**), runs recursive/semantic splitters to preserve context boundaries, generates high-dimensional mathematical vector embeddings, and seeds them into the vector database.

2. **AI Orchestration Core (LangChain Engine)**
   * **`backend/main.py`**: Executes the agentic reasoning and decisioning engine. It coordinates LangChain-native ReAct (Reasoning and Action) execution loops, tracks memory windows, routes prompts to specialized sub-agents, and dynamically binds custom execution tools (math engine, vector retriever, filesystem, system shell) directly to the LLM's workspace context.

3. **Modular Service Layer (FastAPI gateways)**
   * Exposes high-throughput, secure REST and streaming endpoints to the frontend. It features server-sent events (SSE) for fluid token-by-token generation, comprehensive JSON request validation, and embeds the **Model Context Protocol (MCP)**, allowing external developer clients to easily tap into our reasoning pipeline and custom agents.

4. **Next.js Web Console (Frontend)**
   * Implemented using Next.js 15, React 19, TypeScript, and TailwindCSS. Leverages Next.js App Router architecture (`frontend/app/`) for rapid server-side layout hydration, state-of-the-art bundling, and real-time chat visualization components that communicate seamlessly with FastAPI agents.

---

## 📁 Repository Directory Structure

The repository configuration is organized as follows, omitting transient build files and dependency folders (such as `node_modules` and Python `__pycache__` directories) to focus entirely on application modules and configuration vectors:

```text
LangChain/
├── backend/                    # Python AI Reasoning & Ingestion Services
│   ├── Offering_Plan_Final.pdf # Target enterprise PDF document for ingestion
│   ├── environment.yml         # Conda environment package manifest
│   ├── ingest.py               # ETL pipeline (parsing, chunking, and embedding)
│   └── main.py                 # FastAPI Gateway & LangChain agent logic
├── frontend/                   # Next.js App Router Web Interface
│   ├── app/                    # Next.js App Router Directory
│   │   ├── favicon.ico         # Chat Console favicon
│   │   ├── globals.css         # Tailwind CSS global rules
│   │   ├── layout.tsx          # Root HTML layout and context providers
│   │   └── page.tsx            # Main Chat interface UI view
│   ├── public/                 # Static asset delivery directory
│   │   ├── file.svg
│   │   ├── globe.svg
│   │   ├── next.svg
│   │   ├── vercel.svg
│   │   └── window.svg
│   ├── AGENTS.md               # Tool blueprints and agent orchestration guidelines
│   ├── CLAUDE.md               # IDE rules, Claude configurations & MCP guidelines
│   ├── README.md               # Dedicated frontend execution manual
│   ├── eslint.config.mjs       # ESLint static code analysis rules
│   ├── next-env.d.ts           # Next.js TypeScript types
│   ├── next.config.ts          # Core Next.js compiler properties
│   ├── package-lock.json       # Strict NPM dependency tree lockfile
│   ├── package.json            # Node.js run scripts and dependencies
│   ├── page.tsx                # Fallback layout entrypoint
│   ├── postcss.config.mjs      # CSS post-processing rules
│   └── tsconfig.json           # TypeScript compilation configurations
├── history/                    # Persistent storage of session histories
│   └── chat_log.txt            # Real-time chat interaction logs
├── README copy.md              # Legacy documentation backup
├── README.md                   # System documentation (This file)
├── docker-compose.yml          # Container orchestration configuration (Vector DB, etc.)
└── update_readme.py            # Automated codebase structure analysis script
```

---

## 🛠️ Infrastructure & Setup

### 1. Vector Database & Infrastructure Containers (Docker)
Initialize local storage, cache nodes, and vector databases required by the retrieval system using Docker Compose:

```bash
# Spin up infrastructure containers in detached mode
docker compose up -d
```

### 2. Configure the Python Engine (Conda)
Provision the high-performance local virtual environment optimized for scientific computing, natural language parsing, and vector modeling using the Conda spec:

```bash
# Create the virtual environment from the manifest
conda env create -f backend/environment.yml

# Activate the isolated environment
conda activate portfolio-copilot
```

### 3. Run the Data Ingestion Pipeline (ETL)
Parse, chunk, and embed your source documents (such as **`backend/Offering_Plan_Final.pdf`**) into the local vector index:

```bash
# Run the ETL pipeline to populate the vector space
python backend/ingest.py
```

### 4. Launch the FastAPI Reasoning Loop
Execute the core Python server to expose the REST API and active Model Context Protocol (MCP) servers:

```bash
# Launch the API service gateway
python backend/main.py
```

To run with hot-reloading for local code iteration:
```bash
uvicorn backend.main:app --reload --port 8000
```

### 5. Start the Next.js Web Console
In a new terminal window, traverse into the frontend directory, resolve dependencies, and initiate the Next.js development server:

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies matching the lockfile
npm install

# Run local dev environment with hot-module reload and Turbopack
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your web browser to access the active AI Orchestration Interface.

---

## 🤖 Strategy Pods & AI Agents

The backend architecture implements specialized agent strategy patterns to fulfill distinct operations. Detailed tool specs and configurations are detailed in **`frontend/AGENTS.md`** and **`frontend/CLAUDE.md`**.

* **ETL Document Processor (`ingest.py`)**: Responsible for layout extraction, handling document page structures (specifically targeting multi-page real estate/financial assets), running token boundary recursive splitters, generating vectors, and seeding metadata.
* **Orchestrator Agent (`main.py`)**: Intercepts chat inputs, coordinates semantic history buffers, maps dependency toolpaths, dynamically routes execution blocks, and handles LLM output validation.
* **Model Context Protocol (MCP) Interface**: Exposes local quantitative tool wrappers, search tools, and document retrieval endpoints to external developers and workspaces compatible with `@modelcontextprotocol/sdk`.

---

## 📊 Development Workflows

### Codebase Verification & Sync
To automatically verify, map, and synchronize files across system boundaries, use the system verification module:

```bash
# Execute repository analysis and check path structures
python update_readme.py
```

### Git Management Protocol
Ensure all architectural updates, backend configuration changes, or Next.js app page enhancements are correctly versioned:

```bash
# 1. Stage the modifications
git add .

# 2. Commit the structural changes
git commit -m "feat(orchestration): synchronize backend routing, update directory map, and document mcp bindings"

# 3. Push to upstream repository
git push
```

---

## 💡 System Design Under the Hood

### 1. The Knowledge Base (`ingest.py`)
Large Language Models (LLMs) are restricted by their pre-training cutoff limits. To feed private enterprise documents (like **`Offering_Plan_Final.pdf`**) to the model without expensive fine-tuning, the platform implements **Retrieval-Augmented Generation (RAG)**:
* **Parsing**: Unstructured PDF loaders process documents into clean text.
* **Recursive Chunking**: Text is split into overlapping chunks to prevent context loss at chunk boundaries.
* **Vector Embeddings**: Text chunks are passed to an embeddings model, yielding high-dimensional vectors (e.g., 1536 dimensions).
* **Vector Store Persistence**: Vectors and their associated text metadata are indexed in the database for low-latency similarity queries.

### 2. Tool Binding & Schema Generation
Agents interact with the physical world by calling tools. In `backend/main.py`, Python functions are decorated to expose them to LangChain. The engine automatically derives JSON-schema definitions for these functions and injects them into the model's system prompt:
```python
@tool
def calculate_real_estate_cap_rate(net_operating_income: float, purchase_price: float) -> float:
    """Calculates the capitalization rate for a given property asset."""
    return (net_operating_income / purchase_price) * 100
```

### 3. The Agentic Reasoning Loop (ReAct)
The core interaction loop follows a structured cognitive architecture:
1. **Thought**: The LLM analyzes the user input and determines if it requires external data or computations.
2. **Action**: The LLM outputs a formatted tool call payload.
3. **Execution**: The FastAPI/LangChain backend intercepts the request, blocks model execution, runs the local Python tool, and captures the result.
4. **Observation**: The tool output is appended to the model's message history.
5. **Synthesis**: The model reads the original prompt alongside the tool's output to construct a conversational, highly accurate response for the user.