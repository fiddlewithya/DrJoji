# 🧠 DrJoji Telegram Bot

**DrJoji** is a lightweight AI-powered health advisory assistant built on Python and Telegram. It allows users to:
- Check stock availability of medications
- Ask about minor ailments or symptoms
- Enquire about usage of medications, supplements, devices
- Locate store opening hours
- Chat with a pharmacist for further consultation
- Submit feedback after the conversation

---

## 💡 Features

| Functionality                  | Description |
|-------------------------------|-------------|
| 🤖 **AI Assistant**           | Uses OpenAI to answer queries about symptoms and medications |
| 💬 **Pharmacist Handoff**     | Routes RX medication or flagged questions to a human pharmacist |
| 🗂️ **Screening Questions**   | Captures user history for better AI context |
| 📍 **Store Locator**          | Shares the URL to the store location page |
| 📝 **Feedback Capture**       | Captures emoji-based ratings and comments (saved as JSON) |
| 🕓 **Timeout Auto-feedback**  | (Planned) Feedback triggers if chat is inactive |
| 📦 **Stock Enquiry**          | Forwards RX queries to pharmacist, provides store URL for others |

---

## 🛠 Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/drjoji-telegram-bot.git
   cd drjoji-telegram-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup your environment**
   Create a `.env` or configure environment variables directly in your deployment:

   - `TELEGRAM_TOKEN=your_bot_token`
   - `OPENAI_API_KEY=your_openai_key`
   - `ADMIN_CHAT_ID=your_telegram_user_id`

4. **Run the bot**
   ```bash
   python main.py
   ```

---

## 🔧 Known Issues

- Feedback comment text triggers AI (workaround pending).
- If a user clicks incorrect options before completing the proper flow, it may route to a pharmacist instead of the AI.
- Timeout auto-feedback is planned but not yet implemented.

---

## 🚀 Future Enhancements

- Auto-timeout for feedback if user doesn’t respond
- Persistent conversation history for each user
- Admin panel to monitor all queries and usage
- Support for multiple language input
