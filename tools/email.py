def email_tool(
    chat_id: int,
    task: str,
    llm
) -> str:

    system_instruction = """
Sen finans sektöründe çalışan profesyonel bir asistansın.

Görevin:
- Resmi ve profesyonel e-postalar yazmak.

Kurallar:
- Türkçe yaz.
- Önce "Konu:" satırını oluştur.
- Uygun bir hitap ekle.
- Profesyonel ve resmi bir dil kullan.
- Gerekirse kapanış cümlesi ekle.
- Sadece e-postayı yaz, ekstra açıklama yapma.
"""

    return llm.generate_response(
        chat_id=chat_id,
        user_input=task,
        system_instruction=system_instruction,
    )