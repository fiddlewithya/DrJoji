import pandas as pd

def load_rx_medications(filepath="RX medication list.xlsx", sheet_name="RX") -> list:
    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        rx_column = "Medication Name"
        if rx_column in df.columns:
            rx_list = df[rx_column].dropna().astype(str).str.upper().tolist()
            return rx_list
        else:
            print(f"⚠️ Column '{rx_column}' not found in {sheet_name}.")
            return []
    except Exception as e:
        print("❌ Error loading RX medications:", e)
        return []

# Load once at the start
RX_MEDICATIONS = load_rx_medications()

def is_rx_medication(user_input: str) -> bool:
    """Check if user_input matches any known RX med (case-insensitive, partial match)."""
    user_input_upper = user_input.strip().upper()
    return any(user_input_upper in med for med in RX_MEDICATIONS)
