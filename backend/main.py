from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain & LangGraph Imports
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langgraph.prebuilt import create_react_agent

# 1. Load environment variables (GOOGLE_API_KEY)
load_dotenv()

# 2. Re-connect to the Vector Database
connection = "postgresql+psycopg://langchain:langchain@localhost:5432/portfolio_db"
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-3.5-flash")

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="property_leases",
    connection=connection,
    use_jsonb=True,
)

# 3. Define the Tool for the Agent
@tool
def lookup_lease_clauses(query: str) -> str:
    """Searches the property lease database for rules, restrictions, and clauses."""
    results = vector_store.similarity_search(query, k=2)
    return "\n\n".join([doc.page_content for doc in results])

# 4. Initialize the Agent
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
tools = [lookup_lease_clauses]

# This prebuilt function automatically creates the State, Nodes, and Edges for tool calling
agent_executor = create_react_agent(llm, tools) 

# 5. FastAPI App Setup
app = FastAPI(title="Portfolio Copilot API")

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
    return {"status": "Backend is online and ready for agents."}

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    # Run the agent with the user's message
    inputs = {"messages": [("user", request.message)]}
    
    # The agent returns a dictionary of the final state, where the last message is the AI's response
    result = agent_executor.invoke(inputs)
    final_message = result["messages"][-1].content
    
    return {"response": final_message}