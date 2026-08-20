import os
from dotenv import load_dotenv

load_dotenv()
# Persistent volume test

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Не знайдено TOKEN у .env або змінних середовища!")

COOLDOWN = 3600  # 1 година

ADMIN_ID = 879144294