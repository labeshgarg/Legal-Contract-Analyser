# backend/routes/rag.py
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from utils.rag_generator import answer_legal_query
from utils.rag import build_vector_store
import os

router = APIRouter()

class Query(BaseModel):
    question: str

class ClauseBatch(BaseModel):
    clauses: list[dict]  # Each should be {'text': ..., 'type': ...}
    session_id: str  # use file name or UUID per upload session

@router.post("/ask_rag/")
def ask_rag(query: Query, request: Request):
    session_id = request.headers.get("X-Session-ID", "default")
    try:
        answer = answer_legal_query(query.question, session_id=session_id)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/build_vectors/")
def build_vectors(payload: ClauseBatch):
    try:
        persist_dir = f"chroma_store/{payload.session_id}"
        build_vector_store(payload.clauses, persist_dir=persist_dir)
        return {"message": "Vector store built successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
