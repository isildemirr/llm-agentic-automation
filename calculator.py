def calculator_tool(task: str) -> str:
    try:
        result = eval(task)
        return f"Hesaplama sonucu: {result}"
    except Exception:
        return "Hesaplama yapılamadı."