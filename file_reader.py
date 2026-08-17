import os
import pandas as pd
from pypdf import PdfReader
from docx import Document

# Maksimum gönderilecek içerik
MAX_PDF_CHARS = 8000
MAX_TEXT_CHARS = 8000
MAX_ROWS = 100


def read_document(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    # ==========================
    # TXT
    # ==========================
    if extension == ".txt":

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        if len(text) > MAX_TEXT_CHARS:
            text = text[:MAX_TEXT_CHARS]
            text += "\n\n[Doküman kısaltıldı.]"

        return text

    # ==========================
    # PDF
    # ==========================
    elif extension == ".pdf":

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

            if len(text) >= MAX_PDF_CHARS:
                break

        if len(text) > MAX_PDF_CHARS:
            text = text[:MAX_PDF_CHARS]
            text += "\n\n[PDF kısaltıldı.]"

        return text

    # ==========================
    # Word
    # ==========================
    elif extension == ".docx":

        doc = Document(file_path)

        text = "\n".join(
            p.text for p in doc.paragraphs
        )

        if len(text) > MAX_TEXT_CHARS:
            text = text[:MAX_TEXT_CHARS]
            text += "\n\n[Word dokümanı kısaltıldı.]"

        return text

    # ==========================
    # CSV
    # ==========================
    elif extension == ".csv":

        df = pd.read_csv(file_path)

        info = f"""
Dosya Türü: CSV

Satır Sayısı: {len(df)}
Sütun Sayısı: {len(df.columns)}

Sütunlar:
{", ".join(df.columns)}

İlk {min(MAX_ROWS, len(df))} Satır:
"""

        preview = df.head(MAX_ROWS).to_string(index=False)

        return info + "\n" + preview

    # ==========================
    # Excel
    # ==========================
    elif extension == ".xlsx":

        df = pd.read_excel(file_path)

        info = f"""
Dosya Türü: Excel

Satır Sayısı: {len(df)}
Sütun Sayısı: {len(df.columns)}

Sütunlar:
{", ".join(df.columns)}

İlk {min(MAX_ROWS, len(df))} Satır:
"""

        preview = df.head(MAX_ROWS).to_string(index=False)

        return info + "\n" + preview

    else:

        return "Desteklenmeyen dosya formatı."