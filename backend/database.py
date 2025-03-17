import os
from qdrant_client import QdrantClient #type: ignore
from dotenv import load_dotenv

load_dotenv()

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_API_ENDPOINT"),
    api_key= os.getenv("QDRANT_API_KEY")
)

print("Connected to Qdrant Cloud successfully!")