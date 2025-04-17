# pharma_ai.py
from openai import OpenAI
from config import OPENAI_API_KEY
from rx_list import is_rx_medication
import re

client = OpenAI(api_key=OPENAI_API_KEY)

def is_medication_query(text: str) -> bool:
    return is_rx_medication(text) or any(
        kw in text.lower() for kw in [
            "paracetamol", "ibuprofen", "dosage", "vitamin",
            "take", "how many", "how much", "tablet", "medicine", "pill", "mg",
            "cough syrup", "ointment", "nasal spray", "inhaler"
        ]
    )

def generate_symptom_response(user_combined_input: str):
    try:
        # Extract actual user question
        user_lines = user_combined_input.strip().split("User's question:")
        user_question = user_lines[-1].strip() if len(user_lines) > 1 else user_combined_input.strip()

        # Determine type of response
        is_med_query = is_medication_query(user_question)
        system_prompt = (
            "You are a professional pharmacy assistant. Respond in this format using emojis and Markdown:\n\n"
            "💊 **What It Is**\n"
            "📝 **How to Use**\n"
            "⚠️ **Precautions**\n"
            "🚨 **When to Stop / Side Effects**\n"
            "📌 **Disclaimer**"
            if is_med_query else
            "You are a helpful and professional pharmacy assistant. Respond to symptoms in this structured format with emojis and Markdown:\n\n"
            "🔍 **Possible Causes**\n"
            "💊 **Immediate Recommendations**\n"
            "🚨 **Red Flags**\n"
            "🩺 **When to See a Doctor**\n"
            "📌 **Disclaimer**"
        )

        # OpenAI API call
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_combined_input}
            ],
            temperature=0.6,
            max_tokens=600,
        )

        reply = response.choices[0].message.content
        log_type = "💊 Medication Advice" if is_med_query else "🩺 Symptom Triage"
        print(f"[LOG] Response Type: {log_type}")
        return reply, "medication" if is_med_query else "symptom"

    except Exception as e:
        print("❌ OpenAI error:", str(e))
        return "❌ AI is currently unavailable. Please try again later or speak to a pharmacist.", "error"
