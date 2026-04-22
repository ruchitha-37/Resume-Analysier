import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="google/gemma-3-4b-it:free",
    temperature=0.3
)

messages = [HumanMessage(content="Hello")]
try:
    response = llm.invoke(messages)
    print("SUCCESS:", response.content)
except Exception as e:
    print("ERROR:", str(e))
