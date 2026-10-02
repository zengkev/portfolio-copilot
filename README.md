# 🧠 LangChain AI Orchestration & Next.js Interface

Welcome to the **LangChain AI Architecture** repository. This project is a full-stack, enterprise-grade AI orchestration platform. It integrates a robust **Python-based LangChain backend** for data ingestion, embeddings processing, and LLM reasoning, with a high-performance **Next.js frontend** powered by TailwindCSS, TypeScript, and the Next.js App Router.

Containerization and environment configurations are fully managed via **Docker Compose** and **Conda**, ensuring deterministic deployments across development and production environments.

---

## 🏗️ System Architecture

The platform is split into three primary decoupled layers:

```
  ┌────────────────────────────────────────────────────────┐
  │                   Frontend Interface                   │
  │     Next.js Web Console (App Router, Tailwind, TS)     │
  └──────────────────────────┬─────────────────────────────┘
                             │ (API / MCP Streams)
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │                  Modular Service Layer                 │
  │     Python API Service Gateway (`backend/main.py`)     │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │                 AI Orchestration Core                  │
  │    LangChain Engine (Reasoning, Tool Use, Agents)      │
  │    (`backend/main.py` & Ingestion `backend/ingest.py`) │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │                 Data & Ingestion Pipeline              │
  │     Embeddings, Document Chunking, Vector Storage      │
  └────────────────────────────────────────────────────────┘
```

1. **AI & Data Processing Core (Python Backend & Orchestrator)**
   * **`backend/ingest.py`**: Controls the ETL pipeline. It reads raw document sources, executes deterministic chunking strategies, generates high-dimensional vector embeddings, and seeds them into the vector database.
   * **`backend/main.py`**: Executes the primary agentic loops, LLM chains, and coordinates interactions between specialized AI Agents and tools.
   * **`backend/environment.yml`**: Lockfile for the Python dependency tree, optimized for Conda environments.

2. **Modular Service Layer**
   * **`backend/main.py`**: A modularized service execution layer acting as the API gateway or microservice interface (e.g., FastAPI/Uvicorn), decoupling frontend clients from the primary LangChain execution runtimes.

3. **User Experience & Management Console (Next.js Frontend)**
   * **`frontend/app/`**: Next.js App Router directory serving a responsive web interface.
   * **`frontend/page.tsx`**: High-level component routing and view layout.
   * **`frontend/AGENTS.md` & `CLAUDE.md`**: Specification logs detailing agent architectures, prompt maps, tool constraints, and IDE integration configurations (e.g., Anthropic Claude / MCP server specifications).

---

## 📁 Repository Directory Structure

Below is the repository codebase directory map, omitting transient build artifacts and library files (such as `node_modules` and Python cache directories) to focus on key source modules and infrastructural assets:

```text
LangChain/
├── backend/                 # Modular Python backend services
│   ├── environment.yml      # Deterministic Conda environment specification
│   ├── ingest.py            # Data ETL, chunking, and embedding generation pipeline
│   └── main.py              # AI Agent execution core and FastAPI gateway
├── docker-compose.yml       # Multi-container orchestration (DBs, Vector Stores, Cache)
├── update_readme.py         # Automations for codebase synchronization
└── frontend/                # Next.js App Router Web Application
    ├── app/                 # Next.js Application Source
    │   ├── favicon.ico      # Web favicon
    │   ├── globals.css      # Tailwind CSS injections
    │   ├── layout.tsx       # Root layout containing global providers
    │   └── page.tsx         # AI Console landing page & chat interface
    ├── public/              # Static assets (SVGs, branding, and images)
    │   ├── file.svg
    │   ├── globe.svg
    │   ├── next.svg
    │   ├── vercel.svg
    │   └── window.svg
    ├── AGENTS.md            # Architecture specs for AI Agents and Tools
    ├── CLAUDE.md            # Tool guides & IDE integration settings (MCP/Claude)
    ├── README.md            # Frontend-specific development manual
    ├── eslint.config.mjs    # Static analysis rules for the frontend
    ├── next-env.d.ts        # Next.js TypeScript environment declarations
    ├── next.config.ts       # Next.js compiler and bundling configuration
    ├── package-lock.json    # Strict frontend dependency lockfile
    ├── package.json         # Frontend runtime & development dependencies
    ├── page.tsx             # Root frontend entry component
    ├── postcss.config.mjs   # PostCSS styling config
    └── tsconfig.json        # TypeScript compilation options
```

---

## 🛠️ Infrastructure & Setup

### 1. Vector Database & Storage Services (Docker)
The infrastructure uses Docker Compose to run local database engines, caching layers, or Vector Stores (such as Qdrant, Chroma, Redis, or pgvector):

```bash
# Start backend infrastructure in detached mode
docker compose up -d
```

### 2. Configure the Python Engine (Conda)
Initialize the Python environment containing all necessary numerical processing libraries, LangChain modules, and AI SDKs using the lockfile located in the `backend` directory:

```bash
# Create the environment from the lockfile
conda env create -f backend/environment.yml

# Activate the virtual environment
conda activate langchain-core
```

### 3. Run the Modular Backend API & Reasoning Loops
Initialize the modular backend service to expose endpoints to the web console, run data ingestion pipelines, or execute agent CLI runtimes:

```bash
# Launch the API service layer (FastAPI gateway)
python backend/main.py

# Ingest and embed document data sources
python backend/ingest.py
```

### 4. Configure the Web Console (Next.js)
Navigate to the frontend directory, install dependencies under npm, and run the development server:

```bash
# Navigate to workspace
cd frontend

# Install Node dependencies
npm install

# Run the development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) inside your browser to view the operational dashboard.

Navigate back to your LangChain project folder and run the Next.js initialization command again

npx create-next-app@latest frontend


Restart the FastAPI server

uvicorn main:app --reload

---

## 🤖 Strategy Pods & AI Agents

The platform uses specialized agents designed to accomplish task-specific actions. Comprehensive architecture rules, tooling definitions, and configurations are maintained in **`frontend/AGENTS.md`** and **`frontend/CLAUDE.md`**.

* **Document Ingestion Agent**: Analyzes metadata structures, validates chunk overlaps, and optimizes search queries for vector lookups.
* **Orchestration Agent**: Evaluates incoming user prompts, selects the best agentic toolpath, handles errors gracefully, and structures the final response.
* **Model Context Protocol (MCP) Integration**: Implements the Model Context Protocol (located under `frontend/node_modules/@modelcontextprotocol/sdk`) to expose context and tools dynamically to external developer environments (like Claude Desktop).

---

## 📊 Development Workflows

To ensure technical documentation matches structural realities, update scripts are provided:

* **Automated Updates**: Run `update_readme.py` to automatically analyze the folder architecture, identify newly added modules, and flag structural updates.
```bash
python update_readme.py


Git Commands

# 1. Stage the file movements
git add .

# 2. Commit the structural changes
git commit -m "Reorganize project structure: move Python files to backend directory"

# 3. Push to GitHub
git push