import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.chains import RetrievalQA #type: ignore
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings #type: ignore
from langchain_community.vectorstores import FAISS #type: ignore
from langchain_core.prompts import PromptTemplate #type: ignore
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
HF_TOKEN = os.getenv("HF_TOKEN")
HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define request schema
class ChatRequest(BaseModel):
    query: str

# Load LLM
def load_llm():
    return HuggingFaceEndpoint(
        repo_id=HUGGINGFACE_REPO_ID,
        temperature=0.5,
        huggingfacehub_api_token=HF_TOKEN,
        model_kwargs={"token": HF_TOKEN, "max_length": 1024}
    )

# Custom Prompt Template
CUSTOM_PROMPT_TEMPLATE = """
You are a helpful assistant for history textbook that answers questions strictly based on the provided context. Follow these rules:
1. Use ONLY the information in the context to answer the question.
2. If the answer is not in the context, just say "Please ask questions about history".
3. Do not add any extra information or make up answers.
4. Start the answer directly. Do not include any introductory phrases.
5. Try to give at least 6 points of information in the answer.

Context: {context}
Question: {question}
"""

def set_custom_prompt():
    return PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context", "question"])

# Load FAISS Vector Store
DB_FAISS_PATH = "vectorstore/db_faiss"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

# Create Retrieval QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=load_llm(),
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": set_custom_prompt()},
)

# API Endpoint for Chatbot
@app.post("/chat/")
async def chat(request: ChatRequest):
    try:
        response = qa_chain.invoke(request.query)
        return {"answer": response["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
