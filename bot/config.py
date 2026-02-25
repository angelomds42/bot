import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set in .env file")

    LANG_DIR = os.path.join(os.getcwd(), "bot", "languages")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
