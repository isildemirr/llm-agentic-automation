import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path)


class LLMClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY bulunamadı. "
                ".env dosyasını kontrol edin."
            )

        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-3.1-flash-lite"

    def analyze(self, user_input: str) -> dict:
        prompt = f"""
Sen bir agent yönlendiricisisin.

Kullanıcının mesajını analiz et ve yalnızca geçerli JSON döndür.

Kullanılabilecek araçlar:

1. weather_tool
   Kullanıcı hava durumu, sıcaklık, yağmur veya hava tahmini sorarsa kullanılır.

2. calculator_tool
   Kullanıcı matematiksel bir işlem yapmak isterse kullanılır.

3. reminder_tool
   Kullanıcı hatırlatma oluşturmak isterse kullanılır.

4. email_tool
   Kullanıcı e-posta veya mail yazmak isterse kullanılır.

5. general_response
   Hiçbir araç uygun değilse kullanılır.

JSON formatı:

{{
    "tool": "araç_adı",
    "city": null,
    "response": null
}}

Kurallar:

- Hava durumu sorulmuş ve şehir belirtilmişse city alanına şehri yaz.
- Hava durumu sorulmuş fakat şehir belirtilmemişse city null olsun.
- Araç gerekmiyorsa tool alanı general_response olsun.
- Açıklama yazma.
- Markdown kullanma.
- Sadece JSON döndür.

Kullanıcı mesajı:
{user_input}
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text.removeprefix("```json")
            response_text = response_text.removesuffix("```")

        elif response_text.startswith("```"):
            response_text = response_text.removeprefix("```")
            response_text = response_text.removesuffix("```")

        try:
            return json.loads(response_text.strip())

        except json.JSONDecodeError:
            return {
                "tool": "general_response",
                "city": None,
                "response": "Modelin cevabı işlenemedi.",
            }

    def generate_response(self, user_input: str) -> str:
        prompt = f"""
Kullanıcının mesajına Türkçe, anlaşılır ve kısa bir cevap ver.

Kullanıcı mesajı:
{user_input}
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        return response.text.strip()
