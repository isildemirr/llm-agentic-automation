def calculator_tool(expression: str) -> str:
    try:
        result = eval(expression)
        return f"Hesaplama sonucu: {result}"
    except Exception:
        return "Hesaplama yapılırken bir hata oluştu."
def email_tool(subject: str) -> str:
        return f"""
Konu: {subject}

Merhaba,

İstediğiniz konuda bilgilendirme yapmak için bu e-posta hazırlanmıştır.

İyi çalışmalar.
"""
def reminder_tool(task: str) -> str:
    return f"""
Hatırlatma oluşturuldu.

Görev: {task}
Durum: Beklemede
"""