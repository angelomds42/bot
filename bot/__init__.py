import logging
from telegram.ext import Application
from bot.config import Config
from bot.utils.language import lang_manager, get_string, get_msg_string

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_application() -> Application:
    if not Config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set in config!")
    return Application.builder().token(Config.BOT_TOKEN).build()
