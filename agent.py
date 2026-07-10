
from llm import LLMClient
from tools import reminder_tool, calculator_tool, email_tool


class Agent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, user_input: str) -> str:
        decision = self.llm.generate(user_input)

        print("\nLLM Kararı:")
        print(decision)

        if decision == "hatırlatma aracı":
            return reminder_tool(user_input)

        if decision == "hesaplama aracı":
            return calculator_tool(user_input)
        if decision == "e-posta aracı":
            return email_tool(user_input)
        return decision