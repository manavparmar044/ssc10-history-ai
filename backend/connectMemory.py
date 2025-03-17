import os

from langchain_huggingface import HuggingFaceEndpoint #type: ignore
from langchain_core.prompts import PromptTemplate #type: ignore
from langchain.chains import RetrievalQA #type: ignore
from langchain_huggingface import HuggingFaceEmbeddings #type: ignore
from langchain_community.vectorstores import FAISS #type: ignore
from huggingface_hub import InferenceClient #type: ignore

HF_TOKEN = os.environ.get("HF_TOKEN")
HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"

def load_llm(HUGGINGFACE_REPO_ID):
    llm = HuggingFaceEndpoint(
        repo_id=HUGGINGFACE_REPO_ID,
        temperature=0.5, #Abstraction between robustness and creativity,
        huggingfacehub_api_token=HF_TOKEN,
        model_kwargs={
            "token":HF_TOKEN,"max_length":1024
        }
    )
    return llm

#Connect LLM with FAISS
    
CUSTOM_PROMPT_TEMPLATE = """
You are a helpful assistant for history textbook that answers questions strictly based on the provided context. Follow these rules:
1. Use ONLY the information in the context to answer the question.
2. If the answer is not in the context, say "I don't know".
3. Do not add any extra information or make up answers.
4. Start the answer directly. Do not include any introductory phrases.
5. Try to give at least 6 points of information in the answer.

Context: {context}
Question: {question}

"""

def set_custom_prompt(CUSTOM_PROMPT_TEMPLATE):
    prompt = PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE,input_variables=["context","question"])
    return prompt

#Load database

DB_FAISS_PATH = "vectorstore/db_faiss"

embedding_model = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(DB_FAISS_PATH,embedding_model,allow_dangerous_deserialization=True)

#Create retrieval QA chain

qa_chain = RetrievalQA.from_chain_type(
    llm = load_llm(HUGGINGFACE_REPO_ID),
    chain_type = "stuff",
    retriever = db.as_retriever(search_kwargs = {"k":10}),
    return_source_documents = True,
    chain_type_kwargs = {"prompt": set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)},
)

#Invoke with the user query

user_query = input("Write the Query here: ")
response = qa_chain.invoke(user_query)
print(response["result"])
# print("Source Documents: ", response["source_documents"])

#Trial prompt: What is press trust of India?