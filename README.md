# 🧠 LangChain AI Orchestration & Next.js Interface

Welcome to the **LangChain AI Architecture** repository. This project is a full-stack, enterprise-grade AI orchestration platform. It integrates a robust **Python-based LangChain backend** for data ingestion, embeddings processing, and LLM reasoning, with a high-performance **Next.js frontend** powered by TailwindCSS, TypeScript, and the Next.js App Router.

Containerization and environment configurations are fully managed via **Docker Compose** and **Conda**, ensuring deterministic deployments across development and production environments.

---

## 🏗️ System Architecture

The platform is split into two primary decoupling layers:

```
  ┌────────────────────────────────────────────────────────┐
  │                   Frontend Interface                   │
  │     Next.js Web Console (App Router, Tailwind, TS)     │
  └──────────────────────────┬─────────────────────────────┘
                             │ (API / MCP Streams)
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │                 AI Orchestration Core                  │
  │    LangChain Engine (Reasoning, Tool Use, Agents)      │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │                 Data & Ingestion Pipeline              │
  │     Embeddings, Document Chunking, Vector Storage      │
  └────────────────────────────────────────────────────────┘
```

1. **AI & Data Processing Core (Python Backend)**
   * **`ingest.py`**: Controls the ETL pipeline. It reads raw document sources, executes deterministic chunking strategies, generates high-dimensional vector embeddings, and seeds them into the vector database.
   * **`main.py`**: Executes the primary agentic loops, LLM chains, and coordinates interactions between specialized AI Agents and tools.
   * **`environment.yml`**: Lockfile for the Python dependency tree, optimized for Conda environments.

2. **User Experience & Management Console (Next.js Frontend)**
   * **`frontend/app/`**: Next.js App Router directory serving a responsive web interface.
   * **`frontend/AGENTS.md` & `CLAUDE.md`**: Specification logs detailing agent architectures, prompt maps, tool constraints, and IDE integration configurations (e.g., Anthropic Claude / MCP server specifications).

---

## 📁 Repository Directory Structure

Below is the pruned codebase directory map, omitting transient dependencies (such as `node_modules`) to focus on key source modules and infrastructural assets:

```assets
LangChain/
├── docker-compose.yml       # Multi-container orchestration (DBs, Vector Stores, Cache)
├── environment.yml          # Deterministic Conda Python environment file
├── ingest.py                # Data ETL, chunking, and embedding generation pipeline
├── main.py                  # AI Agent execution core and runtime loop
├── update_readme.py         # Automations for codebase synchronization
├── frontend/                # Next.js App Router Web Application
│   ├── AGENTS.md            # Architecture specs for AI Agents and Tools
│   ├── CLAUDE.md            # Tool guides & IDE integration settings (MCP/Claude)
│   ├── README.md            # Frontend development runbook
│   ├── eslint.config.mjs    # Static analysis configuration
│   ├── next.config.ts       # Next.js compiler and bundling configuration
│   ├── tsconfig.json        # TypeScript strict compilation options
│   ├── package.json         # Frontend runtime & development dependencies
│   ├── app/                 # Next.js Application Source
│   │   ├── favicon.ico
│   │   ├── globals.css      # Tailwind utility injections
│   │   ├── layout.tsx       # Root layout containing global providers
│   │   └── page.tsx         # AI Console landing page & chat interface
│   └── public/              # Optimized static asset storage
│       ├── file.svg
│       ├── globe.svg
│       ├── next.svg
│       ├── vercel.svg
│       └── window.svg
```

---

## 🛠️ Infrastructure & Setup

### 1. Vector Database & Storage Services (Docker)
The infrastructure uses Docker Compose to run local database engines, caching layers, or Vector Stores (e.g., pgvector, Qdrant, Chroma, or Redis):

```bash
# Start backend infrastructure in detached mode
docker compose up -d
```

### 2. Configure the Python Engine (Conda)
Initialize the Python environment containing all necessary numerical processing libraries, LangChain modules, and AI SDKs:

```bash
# Create the environment from the lockfile
conda env create -f environment.yml

# Activate the virtual environment
conda activate langchain-core
```

### 3. Running Data Ingestion & reasoning loops
Run the ingestion pipeline to process documents, followed by the agent execution loop:

```bash
# Ingest and embed data sources
python ingest.py

# Initialize the AI Agent runtime
python main.py
```

### 4. Configure the Web Console (Next.js)
Navigate to the frontend directory and install the packages to run the interactive server:

```bash
# Navigate to workspace
cd frontend

# Install Node dependencies
npm install

# Run the development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) inside your browser to view the operational dashboard.

---

## 🤖 Strategy Pods & AI Agents

The platform uses specialized agents designed to accomplish task-specific actions. Comprehensive architecture rules, tooling definitions, and configurations are maintained in **`frontend/AGENTS.md`** and **`frontend/CLAUDE.md`**.

* **Document Ingestion Agent**: Analyzes metadata structures, validates chunk overlaps, and optimizes search queries for vector lookups.
* **Orchestration Agent**: Evaluates incoming user prompts, selects the best agentic toolpath, handles errors gracefully, and structures the final response.
* **Model Context Protocol (MCP) Integration**: Implements the Model Context Protocol (found in `node_modules/@modelcontextprotocol/sdk`) to expose context and tools dynamically to external developer environments (like Claude Desktop).

---

## 📊 Development Workflows

To ensure technical documentation matches structural realities, update scripts are provided:

* **Automated Updates**: Run `update_readme.py` to automatically analyze the folder architecture, identify newly added modules, and flag differences.
```bash
python update_readme.py