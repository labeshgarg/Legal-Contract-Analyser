# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

llm = ChatOpenAI(
    temperature=0.2,
    model_name="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

prompt = PromptTemplate(
    input_variables=["clause"],
    template="""
You are a legal assistant. Summarize the following contract clause clearly and concisely in 1–2 sentences:

Clause:
{clause}

Summary:
""".strip()
)

summarizer_chain = LLMChain(llm=llm, prompt=prompt)

def summarize_clause(clause_text: str) -> str:
    try:
        response = summarizer_chain.run(clause=clause_text)
        return response.strip()
    except Exception as e:
        return f"Error: {str(e)}"
