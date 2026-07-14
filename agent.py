from tools.calculator import calculator_tool
from tools.email import email_tool
from tools.reminder import reminder_tool
from tools.weather_tool import weather_tool


class Agent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, user_input: str) -> str:
        decision = self.llm.analyze(user_input)

        print("\nLLM Kararı:")
        print(decision)

        tool_name = decision.get("tool")
        city = decision.get("city")

        if tool_name == "weather_tool":
            if not city:
                return "Hangi şehrin hava durumunu öğrenmek istiyorsunuz?"

            return weather_tool(city)

        if tool_name == "calculator_tool":
            return calculator_tool(user_input)

        if tool_name == "reminder_tool":
            return reminder_tool(user_input)

        if tool_name == "email_tool":
            return email_tool(user_input)

        return self.llm.generate_response(user_input)
