from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from connectMemory import qa_chain #type: ignore

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/chat/")
async def chat(query: QueryRequest):
    try:
        response = qa_chain.invoke(query.question)
        return {"answer": response["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Chatbot API is running!"}
