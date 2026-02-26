from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from bot.utils.db import get_db


async def _save_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or user.is_bot:
        return

    db = get_db()
    db.execute(
        """
        INSERT INTO users (user_id, username, full_name)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            full_name = excluded.full_name
        """,
        (user.id, user.username, user.full_name),
    )
    db.commit()


def get_user_id(username: str) -> int | None:
    username = username.lstrip("@").lower()
    db = get_db()
    row = db.execute(
        "SELECT user_id FROM users WHERE LOWER(username) = ?", (username,)
    ).fetchone()
    return row[0] if row else None


def __init_module__(application):
    application.add_handler(MessageHandler(filters.ALL, _save_user), group=1)
