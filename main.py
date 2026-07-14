from agent import Agent
from llm import LLMClient
def main():
    llm = LLMClient()
    agent = Agent(llm)

    print("LLM Agent sistemine hoş geldiniz.")
    print("Çıkmak için 'çıkış' yazın.")

    while True:
        user_input = input("\nBir görev girin: ")

        if user_input.lower() == "çıkış":
            print("Program kapatıldı.")
            break

        try:
            result = agent.run(user_input)

            print("\nAgent Sonucu:")
            print(result)

        except Exception as error:
            print("\nBir hata oluştu:")
            print(error)

if __name__ == "__main__":
    main()
