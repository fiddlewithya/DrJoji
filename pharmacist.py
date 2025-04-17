# pharmacist.py
from telegram import Update
from telegram.ext import CallbackContext
import re
import os

ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", 0))

active_sessions = {}  # Stores user sessions to end with timeout or command

def pharmacist_reply_handler(update: Update, context: CallbackContext):
    message = update.message
    if message.chat_id != ADMIN_CHAT_ID:
        return  # Ignore if not from admin

    text = message.text.strip()
    match = re.match(r"^/reply (\d+)\s+(.+)", text, re.DOTALL)

    if match:
        user_id = int(match.group(1))
        reply_message = match.group(2)

        try:
            context.bot.send_message(
                chat_id=user_id,
                text=f"💬 *Pharmacist:* {reply_message}",
                parse_mode="Markdown"
            )
            context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"✅ Message sent to user {user_id}."
            )
        except Exception as e:
            context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"❌ Failed to send message to user {user_id}: {e}"
            )
    else:
        context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text="⚠️ Invalid format. Use: `/reply <user_id> <message>`"
        )
