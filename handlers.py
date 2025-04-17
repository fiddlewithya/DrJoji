# handlers.py

from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from conversation import (
    start_conversation,
    handle_message,
    handle_followup_buttons,
    handle_callback_response,
)
from feedback import handle_feedback_rating, handle_feedback_comment
from pharmacist import pharmacist_reply_handler
from tnc import start_handler, tnc_response_handler

def register_handlers(dispatcher):
    # 🔹 Terms and Conditions flow
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CallbackQueryHandler(tnc_response_handler, pattern="^(agree|disagree)$"))

    # 🔹 Screening Questions
    dispatcher.add_handler(CallbackQueryHandler(handle_callback_response, pattern="^screen_(yes|no)$"))

    # 🔹 Main Menu Options
    dispatcher.add_handler(CallbackQueryHandler(start_conversation, pattern="^(avail|ailments|products|store)$"))
    dispatcher.add_handler(CallbackQueryHandler(handle_followup_buttons, pattern="^(pharmacist_request|return_main|end_chat)$"))

    # 🔹 User Messages (Symptoms or Medication Questions)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # 🔹 Feedback Buttons + Comments
    dispatcher.add_handler(CallbackQueryHandler(handle_feedback_rating, pattern="^rate_[1-5]$"))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_feedback_comment))

    # 🔹 Pharmacist response
    dispatcher.add_handler(CommandHandler("reply", pharmacist_reply_handler))
