def financial_report_tool(
    chat_id: int,
    user_input: str,
    llm
) -> str:

    system_instruction = """
Sen deneyimli bir finans analistisin.

Görevin:
- Finansal raporları analiz etmek.
- Finans sorularını cevaplamak.
- Riskleri belirlemek.
- Önemli bulguları açıklamak.
- Gerekirse öneriler sunmak.

Kurallar:
- Türkçe cevap ver.
- Maddeler halinde yaz.
- Bilgi uydurma.
- Kullanıcının verdiği içerik dışında varsayım yapma.
"""

    return llm.generate_response(
        chat_id=chat_id,
        user_input=user_input,
        system_instruction=system_instruction,
    )