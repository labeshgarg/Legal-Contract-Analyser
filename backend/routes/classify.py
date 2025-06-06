# backend/routes/classify.py

from fastapi import APIRouter
from pydantic import BaseModel
from utils.clause_classifier import predict_clause_type

router = APIRouter()

class ClauseInput(BaseModel):
    text: str

@router.post("/")
def classify_clause(input: ClauseInput):
    """
    Classify the given clause text into predefined legal categories.
    """
    predicted_labels = predict_clause_type(input.text)
    return {"predicted_labels": predicted_labels}
