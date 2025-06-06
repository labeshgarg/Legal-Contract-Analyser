# Legal Contract Analyzer 🧾📊

## 🚀 Overview

Legal contracts often contain complex clauses that are difficult to review manually. This project provides an **AI-powered Contract Analysis Tool** that:

- Extracts clauses from uploaded PDF/DOCX legal contracts
- Classifies each clause (e.g., Indemnity, Arbitration, Termination, etc)
- Assesses the **risk score** of each clause
- Provides a **summary** and a **redline suggestion** for improvement
- Allows users to ask **legal queries** using RAG (Retrieval-Augmented Generation)
- Generates a downloadable PDF report

## 🧠 Motivation

Lawyers and compliance officers spend hours reviewing long contracts. This project automates their workflow, highlights high-risk clauses, and offers a chat interface for clause-level understanding and risk mitigation.

## 🏗️ Tech Stack

### 🔙 Backend (FastAPI)

- **FastAPI** – API endpoints
- **LangChain** – RAG for legal Q&A
- **Chroma DB** – Vector store for clause-level retrieval
- **HuggingFace** – Sentence Transformers for embeddings
- **scikit-learn** – Clause classification
- **PyMuPDF / python-docx** – Text extraction from PDF/DOCX
- **Faker / ReportLab** – PDF generation

### 🌐 Frontend (Next.js + TailwindCSS)

- **Next.js** – Frontend framework
- **React Hooks** – State management
- **Tailwind CSS** – Styling
- **Fetch API** – Integration with FastAPI backend

## 🧩 Project Structure

### Backend (`/backend`)

```
backend/
├── main.py               # FastAPI app
├── routes/
│   ├── classify.py       # Endpoint for clause classification
│   └── rag.py            # Endpoint for RAG-based Q&A
├── utils/
│   ├── clause_chunker.py     # Splits raw text into clauses
│   ├── clause_classifier.py  # Classifier for clause types
│   ├── parser_pdf.py         # PDF text extraction
│   ├── parser_docx.py        # DOCX text extraction
│   ├── risk_scorer.py        # Simple heuristic risk score
│   ├── summarizer.py         # Summary generator (GPT or rule-based)
│   ├── redliner.py           # Clause rewriter (optional)
│   ├── pdf_generator.py      # Generates the final report
│   ├── rag.py                # Embedding, vector store
│   └── rag_generator.py      # RAG query answer logic
└── uploads/              # Uploaded contracts
```

### Frontend (`/frontend`)

```
frontend/
├── app/
│   └── page.tsx          # Main Upload + RAG UI page
├── utils/
│   └── api/
│       ├── askRag.ts     # Wrapper for /ask_rag API
│       └── classifyText.ts   # Wrapper for /classify API
├── public/
└── styles/
```

## 📥 Features Walkthrough

### 1. **Upload Contract (PDF/DOCX)**

- Endpoint: `POST /upload/`
- Extracts text
- Splits into clauses
- Classifies clause type using `predict_clause_type`
- Assigns a risk score using `risk_scorer`
- Summarizes using `summarizer`
- Suggests a rewrite for high-risk clauses

### 2. **Download Report**

- Endpoint: `POST /generate_report/`
- Creates a stylized PDF with all annotated clause data

### 3. **Raw Text Clause Classification**

- Endpoint: `POST /classify/`
- Sends freeform clause text for classification

### 4. **Clause-Aware Q&A (RAG)**

- Uploading vectorizes and stores clauses
- Then you ask:
  - Endpoint: `POST /ask_rag/`
  - Uses LangChain + Chroma vector DB to fetch relevant clauses
  - Uses GPT to answer based on context

## ⚙️ Workflow

1. User uploads a PDF or DOCX
2. Backend processes and returns annotated clauses
3. Frontend renders clauses with risk/summaries
4. User can download a PDF report
5. User can ask questions — RAG answers based on vectorized clause data

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload/` | Upload and analyze contract |
| POST | `/classify/` | Classify raw text clause |
| POST | `/ask_rag/` | Ask questions using RAG |
| POST | `/generate_report/` | Generate PDF report |

## 🧠 Why These Choices?

- **FastAPI**: Async, production-ready Python backend
- **LangChain + Chroma**: Simple and modular RAG setup
- **Next.js**: React-based modern frontend with SSR support
- **HuggingFace + sentence-transformers**: Lightweight yet powerful clause embeddings
- **Manual chunking**: We use custom clause-based splitting instead of raw chunking, improving relevance

## ⚠️ Limitations

- Clause classifier is heuristic (not fine-tuned transformer)
- Risk scoring is rule-based, not learned
- RAG model context is limited to extracted clauses
- No login/auth system (can be added easily)

## ✅ Future Enhancements

- 🔐 User auth (JWT or Clerk)
- 🧠 Fine-tuned LLM for clause classification and risk scoring
- 🗂️ User clause history dashboard
- 📚 PDF + clause memory with FAISS or Weaviate
- 🧾 Redlining via GPT-4 custom prompt

## 🧪 Example Use Case

Upload a contract with 10 clauses. The app will:

- Classify 7 as low risk (e.g., confidentiality, jurisdiction)
- Highlight 3 as high-risk indemnity or termination clauses
- Suggest redlines (e.g., add termination for convenience clause)
- Answer: "Does this contract bind me to arbitration in Singapore?" using RAG

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🧠 Authors & Contributors

- 💡 Idea & Architecture: Labesh Garg
- 👨‍💻 Backend & ML: ChatGPT + Labesh
- 🎨 Frontend & UI/UX: Labesh + Tailwind

## 📄 License

MIT License (custom clause data and classifier models excluded)

## 🏁 Conclusion

This is a real-world, production-ready Legal Contract Analyzer powered by AI + RAG. It saves time, flags issues, and offers explainability for non-legal users.

---

*Built with ❤️ for the legal tech community*