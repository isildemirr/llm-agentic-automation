import re

def mask_sensitive_data(text):

    detected = []

    if re.search(r"\b\d{11}\b", text):
        detected.append("TC Kimlik No")
        text = re.sub(r"\b\d{11}\b", "[TC_MASKED]", text)

    if re.search(r"\bTR\d{24}\b", text):
        detected.append("IBAN")
        text = re.sub(r"\bTR\d{24}\b", "[IBAN_MASKED]", text)

    if re.search(r"\b\d{16}\b", text):
        detected.append("Kart Numarası")
        text = re.sub(r"\b\d{16}\b", "[CARD_MASKED]", text)

    if re.search(r"(\+90\s?)?(5\d{2}\s?\d{3}\s?\d{2}\s?\d{2})", text):
        detected.append("Telefon")
        text = re.sub(
            r"(\+90\s?)?(5\d{2}\s?\d{3}\s?\d{2}\s?\d{2})",
            "[PHONE_MASKED]",
            text,
        )

    if re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text):
        detected.append("E-posta")
        text = re.sub(
            r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "[EMAIL_MASKED]",
            text,
        )

    return text, detected

    