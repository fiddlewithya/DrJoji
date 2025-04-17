# config.py
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", 0))

TNC_TEXT = """
*Welcome to DrJoji!*

*Terms & Conditions*

*Medical Disclaimer*  
This chatbot provides general health advice and product info. It is not a substitute for professional medical care.

*PDPA Disclaimer*  
By using this chatbot, you consent to data collection to improve our services. We do not share sensitive medical info or use data without your consent.
"""

MAIN_MENU_OPTIONS = [
    "🧾 Stock Availability",
    "🤒 Minor Ailments",
    "💊 Meds, Supps & Devices",
    "🕘 Store Hours / Location"
]

STORE_LOCATOR_URL = "Google.com"
