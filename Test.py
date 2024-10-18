import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print(f"Токен: {TELEGRAM_TOKEN}")
print(f"CHAT_ID: {CHAT_ID}")
