from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.help import get_string_helper, register_module_help
from bot.utils.message import reply, edit

import time


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s, e = get_string_helper(update)

    before = time.time()
    message = await reply(update, f"Pinging\\!")

    after = time.time()
    latency = int((after - before) * 1000)
    await edit(message, f"Pong\\! `{e(latency)}ms`")


def __init_module__(application):
    application.add_handler(CommandHandler("ping", ping))
    register_module_help("Misc", "misc.help")
