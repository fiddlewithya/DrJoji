# tnc.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils import show_main_menu

TNC_MESSAGE = """*Welcome to DrJoji!*

*Terms & Conditions*

*Medical Disclaimer*  
This chatbot aims to promote a healthy lifestyle as well as provide general health advice and product information only. It is not a substitute for professional medical advice. If you have an urgent and/or serious medical concern, please visit a medical facility.

*PDPA Disclaimer*  
By using this chatbot, you consent to the collection and processing of your data to improve our services. We do not store sensitive medical data or share it without consent, except as required by law."""

AGREE_TEXT = "✅ I agree with the Terms & Conditions and would like to proceed to consult DrJoji"
DISAGREE_TEXT = "❌ I do not agree with the Terms & Conditions"

def start_handler(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("✅ Agree", callback_data="agree"),
            InlineKeyboardButton("❌ Disagree", callback_data="disagree"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        TNC_MESSAGE, reply_markup=reply_markup, parse_mode="Markdown"
    )

def tnc_response_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    if query.data == "agree":
        query.edit_message_text("✅ Thank you! How can DrJoji assist you today?")
        show_main_menu(user_id, context.bot)
    else:
        query.edit_message_text(
            "⚠️ You need to agree to the terms before using this bot.\n\nPlease visit https://www.google.com./ for more info."
        )
