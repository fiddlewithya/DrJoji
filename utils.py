import json
import os
from datetime import datetime
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext
from config import ADMIN_CHAT_ID, STORE_LOCATOR_URL

FEEDBACK_FILE = "feedback.json"

def save_feedback(user_id, rating=None, comment=None):
    data = {}
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

    if str(user_id) not in data:
        data[str(user_id)] = {}

    if rating is not None:
        data[str(user_id)]["rating"] = rating
    if comment is not None:
        data[str(user_id)]["comment"] = comment

    data[str(user_id)]["timestamp"] = datetime.now().isoformat()

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)

def ask_for_feedback(update: Update, context: CallbackContext):
    keyboard = [[
        InlineKeyboardButton("😡", callback_data="rate_1"),
        InlineKeyboardButton("😞", callback_data="rate_2"),
        InlineKeyboardButton("😐", callback_data="rate_3"),
        InlineKeyboardButton("🙂", callback_data="rate_4"),
        InlineKeyboardButton("😄", callback_data="rate_5")
    ]]
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text="📝 Thank you for using DrJoji! Please rate your overall satisfaction:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def handle_feedback_rating(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    rating = int(query.data.split("_")[1])
    user_id = query.from_user.id

    save_feedback(user_id, rating=rating)

    context.bot.send_message(
        chat_id=user_id,
        text="Would you like to leave additional feedback? If yes, please type your message now. If not, thank you!"
    )
    context.user_data["awaiting_feedback_comment"] = True

def handle_feedback_comment(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    comment = update.message.text

    if context.user_data.get("awaiting_feedback_comment"):
        save_feedback(user_id, comment=comment)
        context.bot.send_message(
            chat_id=user_id,
            text="🙏 Thank you for your valuable feedback! We look forward to serving you again."
        )
        context.user_data["awaiting_feedback_comment"] = False

        context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"📬 Feedback from {user_id}:\nRating: {get_feedback_rating_emoji(user_id)}\nComment: {comment}"
        )

def get_feedback_rating_emoji(user_id):
    if not os.path.exists(FEEDBACK_FILE):
        return "N/A"
    with open(FEEDBACK_FILE, "r") as f:
        data = json.load(f)
    rating = data.get(str(user_id), {}).get("rating", None)
    return {
        1: "😡",
        2: "😞",
        3: "😐",
        4: "🙂",
        5: "😄"
    }.get(rating, "N/A")

def show_main_menu(user_id, bot):
    keyboard = [
        [InlineKeyboardButton("🧾 Stock Availability", callback_data="avail")],
        [InlineKeyboardButton("🤒 Minor Ailments", callback_data="ailments")],
        [InlineKeyboardButton("💊 Meds, Supps & Devices", callback_data="products")],
        [InlineKeyboardButton("🕘 Store Hours / Location", callback_data="store")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(
        chat_id=user_id,
        text="How can DrJoji assist you today?",
        reply_markup=reply_markup
    )
