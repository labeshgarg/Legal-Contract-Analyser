import os
import pickle
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from langchain.text_splitter import RecursiveCharacterTextSplitter

# 🔧 Define embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 📄 Load clause text from extracted file (can modify to load from actual clause list)
def load_clauses(file_path: str):
    with open(file_path, "rb") as f:
        return pickle.load(f)  # List of dicts: [{'text': ..., 'type': ...}, ...]

# 🧩 Turn clause text into documents
def build_documents(clauses):
    return [Document(page_content=clause['text'], metadata={"type": clause["type"]}) for clause in clauses]


# 📚 Store vectors using Chroma
def build_vector_store(clauses, persist_dir="chroma_store"):
    documents = build_documents(clauses)
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    split_docs = splitter.split_documents(documents)
    
    vectordb = Chroma.from_documents(split_docs, embedding_model, persist_directory=persist_dir)
    vectordb.persist()
    return vectordb

# 🔍 Load stored vector db

def load_vector_store(persist_dir="chroma_store"):
    return Chroma(persist_directory=persist_dir, embedding_function=embedding_model)

# 🔁 Example retrieval
if __name__ == "__main__":
    clauses = load_clauses("extracted_clauses.pkl")
    db = build_vector_store(clauses)
    results = db.similarity_search("Is there a force majeure clause?", k=3)
    for doc in results:
        print("Clause Type:", doc.metadata["type"])
        print("Content:", doc.page_content)
        print("---")
        
def get_vector_retriever(persist_dir="chroma_store"):
    vectordb = load_vector_store(persist_dir)
    return vectordb.as_retriever()