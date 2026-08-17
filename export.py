from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

from openpyxl import Workbook


def create_pdf(text: str):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = [
        Paragraph(text.replace("\n", "<br/>"), styles["BodyText"])
    ]

    doc.build(story)

    buffer.seek(0)

    return buffer


def create_excel(text: str):

    wb = Workbook()

    ws = wb.active

    ws.title = "Analiz"

    for i, line in enumerate(text.split("\n"), start=1):
        ws.cell(row=i, column=1).value = line

    buffer = BytesIO()

    wb.save(buffer)

    buffer.seek(0)

    return buffer