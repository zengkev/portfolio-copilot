from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# LangChain & LangGraph Imports
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables (GOOGLE_API_KEY + Langchain Tracing)
load_dotenv()

# Write to chat history file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_DIR = os.path.join(BASE_DIR, "..", "history")
os.makedirs(HISTORY_DIR, exist_ok=True)

HISTORY_FILE = os.path.join(HISTORY_DIR, "chat_log.txt")


# Re-connect to the Vector Database
connection = "postgresql+psycopg://langchain:langchain@localhost:5432/portfolio_db"
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="property_leases",
    connection=connection,
    use_jsonb=True,
)

# Define the Tool for the Agent
@tool
def search_building_documents(query: str) -> str:
    """Searches the offering plan database"""
    results = vector_store.similarity_search(query, k=4)
    return "\n\n".join([doc.page_content for doc in results])

# Initialize the Agent
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
tools = [search_building_documents]


# Pass the system prompt to the agent via state_modifier
agent_executor = create_react_agent(llm, tools)

# FastAPI App Setup
app = FastAPI(title="Property Portfolio Copilot API")

# local host CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/api/health")
def health_check():
    return {"status": "Backend is online and ready for agents today."}



@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    system_prompt = """You are an expert Property Management Copilot. 
    Your primary job is to assist with building operations, lease reviews, and condo board regulations for Kensington Manor. 
    Always use the `search_building_documents` tool to look up exact building rules before answering questions about tenant alterations, maintenance limits, or board approvals. 
    Provide your answers in a highly professional, concise format suitable for property management operations and board-level communication."""

    inputs = {
        "messages": [
            SystemMessage(content=system_prompt),
            HumanMessage(content=request.message)
        ]
    }

    result = agent_executor.invoke(inputs)
    last_message = result["messages"][-1]
    raw_content = last_message.content

    # Robustly extract string text whether content is a string, list of blocks, or dict
    if isinstance(raw_content, list):
        final_message = "".join([
            chunk.get("text", "") if isinstance(chunk, dict) else str(chunk) 
            for chunk in raw_content
        ])
    elif isinstance(raw_content, dict):
        final_message = raw_content.get("text", str(raw_content))
    else:
        final_message = str(raw_content)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] USER: {request.message}\n")
        f.write(f"[{timestamp}] AI: {final_message}\n")
        f.write("-" * 50 + "\n")
    
    return {"response": final_message}