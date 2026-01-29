import os
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI


load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

llm = ChatMistralAI(
    api_key=MISTRAL_API_KEY,
    model_name='open-mistral-nemo-2407',
    temperature=0
)

if __name__ == "__main__":
    message = "hello"
    answer = llm.invoke(message)
    print(answer.content)