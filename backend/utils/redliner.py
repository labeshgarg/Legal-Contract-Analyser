from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

llm = ChatOpenAI(
    temperature=0.3,
    model_name="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

redline_prompt = PromptTemplate(
    input_variables=["clause"],
    template="""
You are a legal expert. Rewrite the following contract clause to reduce legal risk while preserving its original intent.
Make it more favorable to the receiving party.

Original Clause:
{clause}

Redlined Safer Clause:
""".strip()
)

redliner_chain = LLMChain(llm=llm, prompt=redline_prompt)

def rewrite_clause(clause_text: str) -> str:
    try:
        response = redliner_chain.run(clause=clause_text)
        return response.strip()
    except Exception as e:
        return f"Error: {str(e)}"
