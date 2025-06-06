from dotenv import load_dotenv
load_dotenv()
import pickle
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from routes.classify import router as classify_router
import os
from routes import rag
from utils.parser_pdf import extract_text_from_pdf
from utils.parser_docx import extract_text_from_docx
from utils.clause_chunker import split_into_clauses
from utils.risk_scorer import calculate_risk_score
from utils.summarizer import summarize_clause
from utils.redliner import rewrite_clause
from utils.clause_classifier import predict_clause_type
from utils.pdf_generator import generate_pdf_report

app = FastAPI()
app.include_router(rag.router) 
app.include_router(classify_router, prefix="/classify", tags=["Classification"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Legal Contract Analyzer API is live 🚀"}

@app.post("/upload/")
async def upload_contract(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ["pdf", "docx"]:
        return JSONResponse(status_code=400, content={"error": "Only PDF and DOCX files are supported."})

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    if file_ext == "pdf":
        full_text = extract_text_from_pdf(file_path)
    else:
        full_text = extract_text_from_docx(file_path)

    clauses = split_into_clauses(full_text)
    clauses = clauses[:20]  # limit for UI preview + API tokens

    tagged_clauses = []
    for clause in clauses:
        clause_types = predict_clause_type(clause)
        risk_score = calculate_risk_score(clause)
        summary = summarize_clause(clause)
        suggestion = rewrite_clause(clause) if risk_score >= 70 else ""

        tagged_clauses.append({
            "text": clause,
            "type": ", ".join(clause_types),
            "risk_score": risk_score,
            "summary": summary,
            "suggestion": suggestion
        })

    # ✅ Save clauses for RAG
    with open("extracted_clauses.pkl", "wb") as f:
        pickle.dump(tagged_clauses, f)

    return {
        "filename": file.filename,
        "num_clauses": len(tagged_clauses),
        "clauses": tagged_clauses
    }

@app.post("/generate_report/")
async def generate_report(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ["pdf", "docx"]:
        return JSONResponse(status_code=400, content={"error": "Only PDF and DOCX files are supported."})

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    if file_ext == "pdf":
        full_text = extract_text_from_pdf(file_path)
    else:
        full_text = extract_text_from_docx(file_path)

    clauses = split_into_clauses(full_text)
    clauses = clauses[:10]  # to avoid overflow in PDF

    tagged_clauses = []
    for clause in clauses:
        clause_types = predict_clause_type(clause)
        risk_score = calculate_risk_score(clause)
        summary = summarize_clause(clause)
        suggestion = rewrite_clause(clause) if risk_score >= 70 else ""

        tagged_clauses.append({
            "text": clause,
            "type": ", ".join(clause_types),
            "risk_score": risk_score,
            "summary": summary,
            "suggestion": suggestion
        })

    pdf_path = generate_pdf_report(file.filename, tagged_clauses)
    return FileResponse(pdf_path, media_type='application/pdf', filename=os.path.basename(pdf_path))
