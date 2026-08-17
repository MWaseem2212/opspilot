import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_llm():
    """
    Returns a configured Groq LLM client.
    Model: openai/gpt-oss-20b — fast, capable open-weight model on Groq.
    """
    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.2,
        api_key=os.getenv("GROQ_API_KEY"),
    )