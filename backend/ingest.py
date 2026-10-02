import os
from dotenv import load_dotenv

# 1. Load the variables from the .env file into the system environment
load_dotenv()

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document

# 2. Setup the connection string
connection = "postgresql+psycopg://langchain:langchain@localhost:5432/portfolio_db"
collection_name = "property_leases"

# 3. Initialize Gemini Embeddings (It will now automatically find the key)
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-3.5-flash")

# 4. Connect to the PGVectorStore
vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)

# 5. Create a mock document for our real estate copilot
mock_lease_doc = Document(
    page_content="Lease Agreement - Unit 4B: The tenant is permitted to sublet the apartment for a maximum of 3 months per calendar year, subject to a $500 sublet fee and written approval from the Kensington Manor condo board.",
    metadata={"source": "Unit_4B_Lease.pdf", "property": "Kensington Manor"}
)

# 6. Insert the document into PostgreSQL
print("Generating Gemini embeddings and inserting into PostgreSQL...")
vector_store.add_documents([mock_lease_doc])
print("Success! The document is now stored as vectors.")