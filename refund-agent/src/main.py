from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

bot = init_chat_model(model="gpt-6-luna")

response = bot.invoke("Say hello in one word")
print(response)
