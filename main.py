# from llm import LLMClient
# from tools import calculator_tool, reminder_tool, email_tool


# def main():
#     llm = LLMClient()

#     user_input = input("Bir görev girin: ")

#     response = llm.generate(user_input)

#     print("\nLLM Kararı:")
#     print(response)

#     if "hesaplama aracı" in response:
#         tool_result = calculator_tool(user_input)

#         print("\nTool Sonucu:")
#         print(tool_result)
#     else:
#         print("\nCevap:")
#         print(response)
#     # elif "hatırlatma aracı" in response:
#     #     tool_result = reminder_tool(user_input)

#     #     print("\nTool Sonucu:")
#     #     print(tool_result)
#     if "e-posta" in response:
#         tool_result = email_tool(user_input)

#         print("\nTool Sonucu:")
#         print(tool_result)
# if __name__ == "__main__":
#     main()
from agent import Agent


def main():
    agent = Agent()

    user_input = input("Bir görev girin: ")
    result = agent.run(user_input)

    print("\nSonuç:")
    print(result)


if __name__ == "__main__":
    main()