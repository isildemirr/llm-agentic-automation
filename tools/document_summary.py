def document_summary_tool(
    chat_id: int,
    user_input: str,
    llm
) -> str:

    system_instruction = """
Sen profesyonel bir doküman analiz uzmanısın.

Görevin:
- Dokümanları özetlemek.
- En önemli maddeleri çıkarmak.
- Riskleri belirtmek.

Kurallar:
- Türkçe yaz.
- Kısa ve anlaşılır özet oluştur.
- Gereksiz detay verme.
"""

    return llm.generate_response(
        chat_id=chat_id,
        user_input=user_input,
        system_instruction=system_instruction,
    )