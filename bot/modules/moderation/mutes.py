from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes, CommandHandler
from telegram.error import TelegramError
from bot.utils.help import get_string_helper
from bot.utils.message import reply
from bot.modules.moderation.common import check_common, get_member, _parse_args


async def _mute_common(update, context, action, restrict=True):
    s, e = get_string_helper(update)

    user_id, display_name, ok = await check_common(update, context, s, action)
    if not ok:
        return

    if not restrict:
        member = await get_member(update.effective_chat, user_id)
        if not member or member.can_send_messages is not False:
            return await reply(update, s("moderation.unmute.not_muted"))

    arg_offset = 0 if update.message.reply_to_message else 1
    until_date, duration_str, arg_offset = _parse_args(context, arg_offset, restrict)
    reason = " ".join(context.args[arg_offset:]) if context.args else None

    try:
        allow = not restrict
        await update.effective_chat.restrict_member(
            user_id,
            ChatPermissions(
                can_send_messages=allow,
                can_send_polls=allow,
                can_send_other_messages=allow,
                can_add_web_page_previews=allow,
            ),
            until_date=until_date,
        )

        text = s(f"moderation.{action}.success", username=e(display_name))
        if duration_str:
            text += f"\n{s(f'moderation.{action}.duration', duration=e(duration_str))}"
        if reason:
            text += f"\n{s('moderation.common.restriction_reason', reason=e(reason))}"

        await reply(update, text)
    except TelegramError:
        await reply(update, s(f"moderation.{action}.error"))


async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _mute_common(update, context, "mute")


async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _mute_common(update, context, "unmute", restrict=False)


def __init_module__(application):
    application.add_handler(CommandHandler("mute", mute))
    application.add_handler(CommandHandler("unmute", unmute))
