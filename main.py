# main.py
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)
from handlers import register_handlers
from conversation import (
    start_conversation,
    handle_message,
    handle_followup_buttons,
    handle_callback_response,
)
from feedback import handle_feedback_rating, handle_feedback_comment
from pharmacist import pharmacist_reply_handler
from tnc import start_handler, tnc_response_handler
import os
from keep_alive import keep_alive

keep_alive()  # Starts the pingable Flask server


TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # ✅ Terms & Conditions flow
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CallbackQueryHandler(tnc_response_handler, pattern="^(agree|disagree)$"))

    # ✅ Screening question flow
    dispatcher.add_handler(CallbackQueryHandler(handle_callback_response, pattern="^screen_(yes|no)$"))

    # ✅ General conversation and flow
    dispatcher.add_handler(CallbackQueryHandler(start_conversation, pattern="^(avail|ailments|products|store)$"))
    dispatcher.add_handler(CallbackQueryHandler(handle_followup_buttons, pattern="^(pharmacist_request|return_main|end_chat)$"))

    # ✅ Handles user questions
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # ✅ Feedback handling
    dispatcher.add_handler(CallbackQueryHandler(handle_feedback_rating, pattern="^rate_[1-5]$"))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_feedback_comment))

    # ✅ Pharmacist reply command
    dispatcher.add_handler(CommandHandler("reply", pharmacist_reply_handler))

    updater.start_polling()
    print("✅ Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
