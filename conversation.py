# conversation.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from config import STORE_LOCATOR_URL, ADMIN_CHAT_ID
from pharma_ai import generate_symptom_response
from utils import show_main_menu, ask_for_feedback
from rx_list import is_rx_medication
from datetime import datetime

conversation_state = {}
screening_progress = {}
user_answers = {}
user_symptom_message = {}
pharmacist_sessions = {}

SCREENING_QUESTIONS = [
    "Do you have any drug allergies?",
    "Are you taking any long-term medications or supplements?",
    "Do you have any medical conditions?"
]

def start_conversation(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    context.user_data.clear()

    # Remove main menu inline message
    try:
        query.delete_message()
    except:
        pass

    option = query.data
    conversation_state[user_id] = option
    screening_progress[user_id] = 0
    user_answers[user_id] = []
    user_symptom_message[user_id] = ""

    if option == "avail":
        context.bot.send_message(chat_id=user_id, text="🧾 What medication would you like to enquire about?")
        return

    elif option == "ailments" or option == "products":
        context.bot.send_message(chat_id=user_id, text="🩺 Before we proceed, kindly answer the following questions:")
        ask_next_screening_question(context, user_id)
        return

    elif option == "store":
        keyboard = [[InlineKeyboardButton("🔁 Return to Main Menu", callback_data="return_main")]]
        context.bot.send_message(
            chat_id=user_id,
            text=f"📍 Thank you for your enquiry! Please visit:\n{STORE_LOCATOR_URL}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

def ask_next_screening_question(context: CallbackContext, user_id: int):
    step = screening_progress.get(user_id, 0)
    if step < len(SCREENING_QUESTIONS):
        q = SCREENING_QUESTIONS[step]
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="screen_yes"), InlineKeyboardButton("No", callback_data="screen_no")]
        ]
        context.bot.send_message(chat_id=user_id, text=q, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        context.bot.send_message(chat_id=user_id, text="✅ Thank you! What would you like to ask about?")

def handle_callback_response(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    response = query.data
    query.answer()

    if user_id not in screening_progress:
        return

    current_step = screening_progress[user_id]
    user_answers[user_id].append("Yes" if response == "screen_yes" else "No")

    if current_step < len(SCREENING_QUESTIONS):
        answered_text = f"{SCREENING_QUESTIONS[current_step]} ✅ {'Yes' if response == 'screen_yes' else 'No'}"
        query.edit_message_text(text=answered_text)

    screening_progress[user_id] += 1
    ask_next_screening_question(context, user_id)

def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    msg = update.message.text.strip()

    # Pharmacist chat session handling
    if user_id in pharmacist_sessions:
        pharmacist_sessions[user_id]["messages"].append(msg)
        context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"📨 *User {user_id} replied:*\n{msg}",
            parse_mode='Markdown'
        )
        return

    user_symptom_message[user_id] = msg

    if conversation_state.get(user_id) == "avail":
        if is_rx_medication(msg):
            context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"💊 RX enquiry from user `{user_id}`:\n\n*{msg}*", parse_mode='Markdown')
            context.bot.send_message(chat_id=user_id, text="This medication requires a pharmacist. We'll attend to you shortly.")
            pharmacist_sessions[user_id] = {"messages": [msg]}

            keyboard = [[InlineKeyboardButton("❌ End Chat", callback_data="end_chat")]]
            context.bot.send_message(chat_id=user_id, text="If you're done, you may end the chat anytime.", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            keyboard = [[InlineKeyboardButton("🔁 Return to Main Menu", callback_data="return_main")]]
            context.bot.send_message(
                chat_id=user_id,
                text=f"📦 For non-RX meds, please contact your nearest DrJoji store:\n{STORE_LOCATOR_URL}",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    elif conversation_state.get(user_id) in ["ailments", "products"]:
        try:
            symptom_context = get_screening_summary(user_id)
            full_prompt = f"{symptom_context}\n\nUser's question: {msg}"
            ai_reply, response_type = generate_symptom_response(full_prompt)
            context.bot.send_message(chat_id=user_id, text=ai_reply, parse_mode='Markdown')

            log_type = "💊 Medication Advice" if response_type == "medication" else "🩺 Symptom Triage"
            context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"[LOG] User {user_id} triggered: {log_type}")
            print(f"[{datetime.now()}] User {user_id} asked: {msg} → Type: {log_type}")

        except Exception as e:
            context.bot.send_message(chat_id=user_id, text="❌ AI is currently unavailable. Please try again later or speak to a pharmacist.")
            print("AI error:", str(e))

        keyboard = [
            [InlineKeyboardButton("💬 Speak to Pharmacist", callback_data="pharmacist_request")],
            [InlineKeyboardButton("🔁 Return to Main Menu", callback_data="return_main")]
        ]
        context.bot.send_message(
            chat_id=user_id,
            text="Would you like to speak to a pharmacist or return to the main menu?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def get_screening_summary(user_id: int) -> str:
    answers = user_answers.get(user_id, ["-", "-", "-"])
    return (
        f"👤 *User Screening Summary:*\n"
        f"- Drug Allergies: {answers[0]}\n"
        f"- Long-term Meds/Supplements: {answers[1]}\n"
        f"- Medical Conditions: {answers[2]}"
    )

def forward_to_pharmacist(user_id, context):
    screening_info = get_screening_summary(user_id)
    user_message = user_symptom_message.get(user_id, "[No message submitted]")

    pharmacist_sessions[user_id] = {
        "messages": [user_message]
    }

    context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            f"📨 *Pharmacist Request Received!*\n\n"
            f"{screening_info}\n\n"
            f"💬 *User's Question:*\n{user_message}\n\n"
            f"Use `/reply {user_id} <your message>` to respond."
        ),
        parse_mode='Markdown'
    )
    context.bot.send_message(
        chat_id=user_id,
        text="💬 A pharmacist will respond to you shortly. Thank you for your patience.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ End Chat", callback_data="end_chat")]])
    )

def handle_followup_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query_data = query.data

    query.answer()

    if query_data == "pharmacist_request":
        forward_to_pharmacist(user_id, context)

    elif query_data == "return_main":
        clear_user_session(user_id)
        show_main_menu(user_id, context.bot)

    elif query_data == "end_chat":
        pharmacist_sessions.pop(user_id, None)
        context.bot.send_message(
            chat_id=user_id,
            text="🛑 Chat session ended. Thank you for speaking with us!"
        )
        ask_for_feedback(update, context)

def clear_user_session(user_id: int):
    conversation_state.pop(user_id, None)
    screening_progress.pop(user_id, None)
    user_answers.pop(user_id, None)
    user_symptom_message.pop(user_id, None)
