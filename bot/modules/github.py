from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_msg_string
from github import Github
from github.GithubException import UnknownObjectException, GithubException
import asyncio
import os


async def github(update: Update, context: ContextTypes.DEFAULT_TYPE):
    no_args = get_msg_string(update, "github.no_args")

    args = context.args
    if not args:
        await update.message.reply_text(no_args)
        return

    username = args[0]

    try:
        gh = Github()
        user = await asyncio.to_thread(gh.get_user, username)
    except UnknownObjectException:
        await update.message.reply_text(
            get_msg_string(update, "github.not_found", username=username)
        )
        return
    except GithubException:
        await update.d.reply_text(get_msg_string(update, "github.error"))
        return

    login = getattr(user, "login", "") or ""
    name = getattr(user, "name", "") or ""
    bio = getattr(user, "bio", "") or ""

    await update.message.reply_text(f"{login} — {name}\n{bio}")


def __init_module__(application):
    application.add_handler(CommandHandler("github", github))
