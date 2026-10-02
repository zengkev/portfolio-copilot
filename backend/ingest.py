import os
from time import sleep
from dotenv import load_dotenv
load_dotenv()

# Load langchain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# set up connection to the PostgreSQL database
connection = "postgresql+psycopg://langchain:langchain@localhost:5432/portfolio_db"
collection_name = "property_leases"


# Initalize the embeddings model
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

# Connect to the PGVectorStore
vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)


# Load some real documents

print("Loading PDF...")
loader = PyPDFLoader("Offering_Plan_Final.pdf")
pages = loader.load()
print(f"Loaded {len(pages)} pages from the PDF.")

# Split the pages into smaller chunks
print("Splitting the PDF into smaller chunks... can you wait???")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, # Number of characters per chunk
    chunk_overlap=200, # Overlap to prevent cutting sentences in half
    length_function=len
)

documents = text_splitter.split_documents(pages)
print(f"Split the PDF into {len(documents)} chunks.")

# need to batch this doc.. too big (that's what she said)
print(f"Total chunks created: {len(documents)}")
print("Embedding chunks into the database in batches...")

batch_size = 50  # Send 50 chunks at a time

for i in range(0, len(documents), batch_size):
    batch = documents[i : i + batch_size]
    print(f"Processing chunks {i} to {i + len(batch)}...")
    
    # Embed and insert the current batch
    vector_store.add_documents(batch)
    print(f"Successfully inserted the part {i} to {i + len(batch)} documents into PostgreSQL.")
    
    # Pause for 2 seconds to avoid hitting Google API rate limits
    time.sleep(2)

print("Success! Your offering plan is now searchable.")

