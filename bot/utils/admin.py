from telegram import Update, ChatMember
from telegram.error import TelegramError


async def is_user_admin(update: Update) -> bool:
    """Check if the command sender is an admin or creator."""
    member = await update.effective_chat.get_member(update.effective_user.id)
    return member.status in (ChatMember.ADMINISTRATOR, ChatMember.OWNER)


async def is_bot_admin(update: Update) -> bool:
    """Check if the bot is an admin in the chat."""
    bot_id = update.get_bot().id
    member = await update.effective_chat.get_member(bot_id)
    return member.status in (ChatMember.ADMINISTRATOR, ChatMember.OWNER)


async def bot_has_permission(update: Update, permission: str) -> bool:
    """
    Check if the bot has a specific admin permission.

    Permissions:
    - can_restrict_members  (kick, ban, mute)
    - can_delete_messages
    - can_pin_messages
    - can_promote_members
    - can_change_info
    - can_invite_users
    - can_manage_chat
    - can_manage_video_chats
    """
    try:
        bot_id = update.get_bot().id
        member = await update.effective_chat.get_member(bot_id)
        if member.status != ChatMember.ADMINISTRATOR:
            return False
        return bool(getattr(member, permission, False))
    except TelegramError:
        return False


async def user_has_permission(update: Update, permission: str) -> bool:
    """Check if the command sender has a specific admin permission."""
    try:
        member = await update.effective_chat.get_member(update.effective_user.id)
        if member.status == ChatMember.OWNER:
            return True
        if member.status != ChatMember.ADMINISTRATOR:
            return False
        return bool(getattr(member, permission, False))
    except TelegramError:
        return False
