from telegram import Update, constants, helpers
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_msg_string

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_msg_string(update, "common.start")
    safe_text = helpers.escape_markdown(text, version=2)
    await update.message.reply_text(safe_text, parse_mode=constants.ParseMode.MARKDOWN_V2)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_msg_string(update, "common.help")
    safe_text = helpers.escape_markdown(text, version=2)
    await update.message.reply_text(safe_text, parse_mode=constants.ParseMode.MARKDOWN_V2)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = helpers.escape_markdown(user.first_name, version=2)
    uid = helpers.escape_markdown(str(user.id), version=2)
    lang = helpers.escape_markdown(user.language_code or "N/A", version=2)
    
    message = (
        f"*User:* {name}\n"
        f"*ID:* `{uid}`\n"
        f"*Lang:* `{lang}`"
    )
    await update.message.reply_text(message, parse_mode=constants.ParseMode.MARKDOWN_V2)

def __init_module__(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
