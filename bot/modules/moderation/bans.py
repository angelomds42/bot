from telegram import Update, ChatMember
from telegram.ext import ContextTypes, CommandHandler
from telegram.error import TelegramError
from bot.utils.help import get_string_helper, register_module_help
from bot.utils.message import reply
from bot.modules.moderation.common import check_common, get_member, _parse_args


async def _execute_ban(update, user_id, until_date, kick, unban, delete_message):
    if not unban:
        await update.effective_chat.ban_member(user_id, until_date=until_date)
    if kick or unban:
        await update.effective_chat.unban_member(user_id)
    if delete_message and update.message.reply_to_message:
        await update.message.reply_to_message.delete()


async def _ban_common(
    update,
    context,
    action,
    force_reply=False,
    delete_message=False,
    has_duration=True,
    kick=False,
    unban=False,
):
    s, e = get_string_helper(update)

    if force_reply and not update.message.reply_to_message:
        return await reply(update, s("moderation.common.reply_required"))

    user_id, display_name, ok = await check_common(
        update, context, s, action, check_admin_target=not unban
    )
    if not ok:
        return

    if unban:
        member = await get_member(update.effective_chat, user_id)
        if not member or member.status != ChatMember.BANNED:
            return await reply(update, s("moderation.ban.not_banned"))

    arg_offset = 0 if update.message.reply_to_message else 1
    until_date, duration_str, arg_offset = _parse_args(
        context, arg_offset, has_duration
    )
    reason = " ".join(context.args[arg_offset:]) if context.args else None

    try:
        await _execute_ban(update, user_id, until_date, kick, unban, delete_message)

        text = s(f"moderation.{action}.success", username=e(display_name))
        if duration_str:
            text += f"\n{s(f'moderation.{action}.duration', duration=e(duration_str))}"
        if reason:
            text += f"\n{s('moderation.common.restriction_reason', reason=e(reason))}"

        await reply(update, text)
    except TelegramError:
        await reply(update, s(f"moderation.{action}.error"))


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _ban_common(update, context, "ban")


async def dban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _ban_common(update, context, "ban", force_reply=True, delete_message=True)


async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _ban_common(update, context, "unban", unban=True, has_duration=False)


async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _ban_common(update, context, "kick", kick=True, has_duration=False)


def __init_module__(application):
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CommandHandler("dban", dban))
    application.add_handler(CommandHandler("unban", unban))
    application.add_handler(CommandHandler("kick", kick))
