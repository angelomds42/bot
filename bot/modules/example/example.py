from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.help import get_string_helper, register_module_help
from bot.utils.message import reply


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Example: reply with a localized string."""
    s, _ = get_string_helper(update)
    await reply(update, s("common.start"))


async def user_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Example: access user metadata and format with MarkdownV2."""
    user = update.effective_user
    if not user:
        return

    s, e = get_string_helper(update)
    await reply(
        update,
        f"*User Profile*\n"
        f"───\n"
        f"*Name:* {e(user.full_name)}\n"
        f"*ID:* `{e(user.id)}`\n"
        f"*Locale:* `{e(user.language_code or 'N/A')}`\n"
        f"*Premium:* {'Yes' if user.is_premium else 'No'}\n"
        f"───",
    )


async def chat_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Example: access chat metadata."""
    chat = update.effective_chat
    if not chat:
        return

    _, e = get_string_helper(update)
    await reply(
        update,
        f"*Chat Info*\n"
        f"───\n"
        f"*ID:* `{e(chat.id)}`\n"
        f"*Type:* `{e(chat.type)}`\n"
        f"*Title:* {e(chat.title or chat.first_name or 'N/A')}\n"
        f"───",
    )


async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Example: echo user input back, escaped for MarkdownV2."""
    s, e = get_string_helper(update)

    if not context.args:
        return await reply(update, s("errors.unknown"))

    await reply(update, e(" ".join(context.args)))


async def args_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Example: handle and display command arguments."""
    _, e = get_string_helper(update)

    if not context.args:
        return await reply(update, "Usage\\: `/args <arg1> [arg2] \\.\\.\\.`")

    lines = "\n".join(f"`{i + 1}`\\. {e(arg)}" for i, arg in enumerate(context.args))
    await reply(update, f"*{e(len(context.args))} argument\\(s\\):*\n{lines}")


# This module is an example of how to structure a new module.
# To activate it, implement __init_module__ and move it to bot/modules/.
#
# def __init_module__(application) -> None:
#     application.add_handler(CommandHandler("start", start_handler))
#     application.add_handler(CommandHandler("me", user_info_handler))
#     application.add_handler(CommandHandler("chat", chat_info_handler))
#     application.add_handler(CommandHandler("echo", echo_handler))
#     application.add_handler(CommandHandler("args", args_handler))
#     register_module_help("Example", "example.help")
