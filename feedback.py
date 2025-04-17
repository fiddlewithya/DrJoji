# feedback.py
import json
from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext
import os

FEEDBACK_FILE = "feedback_log.json"
pending_feedback = {}

def handle_feedback_rating(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.from_user.id
    rating = query.data.split("_")[1]
    query.answer()

    # Store the rating in pending state
    pending_feedback[chat_id] = {
        "rating": int(rating),
        "timestamp": datetime.utcnow().isoformat()
    }

    context.bot.send_message(
        chat_id=chat_id,
        text="📝 Got it! If you'd like to leave a comment as well, type it below:"
    )

def handle_feedback_comment(update: Update, context: CallbackContext):
    chat_id = update.effective_user.id
    comment = update.message.text

    feedback_data = pending_feedback.pop(chat_id, None)

    if feedback_data:
        feedback_data["comment"] = comment
    else:
        feedback_data = {
            "rating": None,
            "comment": comment,
            "timestamp": datetime.utcnow().isoformat()
        }

    feedback_data["user_id"] = chat_id

    # Load existing feedback if any
    all_feedback = []
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r") as f:
                all_feedback = json.load(f)
        except json.JSONDecodeError:
            all_feedback = []

    all_feedback.append(feedback_data)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(all_feedback, f, indent=2)

    context.bot.send_message(
        chat_id=chat_id,
        text="🙏 Thank you for your feedback! We really appreciate it."
    )
