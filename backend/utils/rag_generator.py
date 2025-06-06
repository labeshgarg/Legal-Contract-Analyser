# utils/rag_generator.py

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from .rag import get_vector_retriever
from .rag import load_vector_store
# 🔧 Initialize retriever
retriever = get_vector_retriever()

# 🧠 Load LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 🧩 Prompt Template
template = """
You are a legal expert assistant.
Use the retrieved context to answer the user query. Be concise, but legally accurate.

Context:
{context}

Question:
{question}

Answer in simple legal language:
"""

prompt = PromptTemplate(input_variables=["context", "question"], template=template)

# 🔗 Chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True,
)

def answer_legal_query(question: str):
    """RAG pipeline entrypoint."""
    result = rag_chain({"query": question})
    return result["result"]

def answer_legal_query(question, session_id="default"):
    vectorstore = load_vector_store(persist_dir=f"chroma_store/{session_id}")
    results = vectorstore.similarity_search(question, k=3)
    return "\n\n".join([doc.page_content for doc in results])