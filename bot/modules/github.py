from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_msg_string
from github import Github
from github.GithubException import UnknownObjectException, GithubException
import asyncio
import os


async def github(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # strings
    no_args_string = get_msg_string(update, "github.no_args")
    user_info_string = get_msg_string(update, "github.user_info")
    name_string = get_msg_string(update, "github.name")
    username_string = get_msg_string(update, "github.username")
    location_string = get_msg_string(update, "github.location")
    followers_string = get_msg_string(update, "github.followers")
    repos_string = get_msg_string(update, "github.public_repos")

    args = context.args
    if not args:
        await update.message.reply_text(no_args_string, parse_mode="Markdown")
        return

    username = args[0]

    try:
        gh = Github()
        user = await asyncio.to_thread(gh.get_user, username)
    except UnknownObjectException:
        await update.message.reply_text(
            get_msg_string(update, "github.not_found", username=username),
            parse_mode="Markdown",
        )
        return
    except GithubException:
        await update.message.reply_text(
            get_msg_string(update, "github.error"), parse_mode="Markdown"
        )
        return

    login = getattr(user, "login", "") or ""
    name = getattr(user, "name", "") or ""
    bio = getattr(user, "bio", "") or ""
    location = getattr(user, "location", "") or ""
    profile_url = getattr(user, "html_url", "") or ""
    followers = getattr(user, "followers", "") or ""
    public_repos = getattr(user, "public_repos", "") or ""

    await update.message.reply_text(
        f"*{user_info_string}*:\n"
        f"*{name_string}*: {name}\n"
        f"*{username_string}*: {login}\n"
        f"*Bio*: {bio}\n"
        f"*{location_string}*: {location}\n"
        f"*{repos_string}*: {public_repos}\n"
        f"*{followers_string}*: {followers}\n"
        f"*URL:* {profile_url}",
        parse_mode="Markdown",
    )


def __init_module__(application):
    application.add_handler(CommandHandler("github", github))
