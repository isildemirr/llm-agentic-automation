import json
import os
import random
import re
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from database import load_last_messages

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)


class LLMClient:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY bulunamadı.")

        self.client = Groq(api_key=api_key)

        self.model_name = "llama-3.1-8b-instant"

        # Aynı soruda tekrar analiz yapmamak için
        self.router_cache = {}

    # ======================================================
    # GROQ
    # ======================================================

    def _generate(
        self,
        prompt: str,
        system_instruction: str = ""
    ) -> str:

        last_error = None

        for attempt in range(3):

            try:

                response = self.client.chat.completions.create(
                    model=self.model_name,
                    temperature=0,
                    messages=[
                        {
                            "role": "system",
                            "content": system_instruction
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                return response.choices[0].message.content.strip()

            except Exception as e:

                last_error = e

                print(f"Deneme {attempt+1}: {e}")

                if "429" in str(e):

                    wait = (2 ** (attempt + 1)) + random.uniform(0.5, 1.5)
                    time.sleep(wait)

                else:
                    raise

        raise last_error

    # ======================================================
    # TOOL ROUTER
    # ======================================================

    def analyze(self, user_input: str):

        cache_key = user_input.lower().strip()

        if cache_key in self.router_cache:
            return self.router_cache[cache_key]

        system_instruction = """
Sen yalnızca bir Tool Router'sın.

Tek görevin kullanıcının mesajını uygun tool'a yönlendirmektir.

SADECE JSON döndür.

Format:

{
  "tool":"tool_ismi"
}

Kullanılabilecek toollar

financial_report_tool
- bilanço
- finansal tablo
- gelir tablosu
- nakit akışı
- şirket analizi
- oran analizi

document_summary_tool
- özetle
- summarize
- uzun metni özetle

finance_rag_tool
- yüklenen dosyaya soru soruyorsa
- pdf içeriği
- raporda ne yazıyor
- bu dosyada ...

compliance_checker_tool
- BDDK
- SPK
- mevzuat
- yönetmelik
- prosedür
- politika
- sözleşme
- uygun mu
- compliance

finance_email_tool
- mail yaz
- e-posta hazırla

general_response
BUNLARIN TAMAMI:

- merhaba
- selam
- günaydın
- iyi akşamlar
- naber
- nasılsın
- teşekkür ederim
- benim adım neydi
- beni hatırlıyor musun
- sohbet
- genel bilgi
- yukarıdakilerin dışında kalan HER ŞEY

ÖRNEKLER

Kullanıcı:
"Naber"

Cevap
{
 "tool":"general_response"
}

Kullanıcı:
"Merhaba"

{
 "tool":"general_response"
}

Kullanıcı:
"Benim adım neydi"

{
 "tool":"general_response"
}

Kullanıcı:
"Bu bilançoyu analiz et"

{
 "tool":"financial_report_tool"
}

Kullanıcı:
"Bu sözleşme BDDK'ya uygun mu?"

{
 "tool":"compliance_checker_tool"
}

Kullanıcı:
"Bu PDF'i özetle"

{
 "tool":"document_summary_tool"
}

Kullanıcı:
"Yüklediğim dosyada faaliyet kârı kaç?"

{
 "tool":"finance_rag_tool"
}

SADECE JSON DÖNDÜR.
Başka hiçbir açıklama yazma.
"""

        try:

            raw = self._generate(
                user_input,
                system_instruction
            )

            match = re.search(r"\{.*\}", raw, re.DOTALL)

            if match:
                result = json.loads(match.group())
            else:
                raise ValueError

        except Exception:

            result = {
                "tool": "general_response"
            }

        self.router_cache[cache_key] = result

        return result
    # ======================================================
    # RESPONSE
    # ======================================================

    def generate_response(
        self,
        user_input: str,
        chat_id: int,
        system_instruction: str = None
    ) -> str:

        # Son konuşmaları getir
        history = load_last_messages(
            chat_id=chat_id,
            limit=12
        )

        default_system = """
Sen finans alanında çalışan profesyonel bir yapay zekâ asistanısın.

Kurallar:

- Her zaman Türkçe cevap ver.
- Önceki konuşmaları dikkate al.
- Kullanıcının adını veya önceki konuşmaları hatırlayabiliyorsan kullan.
- Bilmediğin bilgiyi uydurma.
- Gereksiz tekrar yapma.
- Gerektiğinde maddeler halinde cevap ver.
- Sohbet ediliyorsa doğal cevap ver.
- Finans sorularında uzman gibi davran.
"""

        messages = [
            {
                "role": "system",
                "content": system_instruction or default_system
            }
        ]

        # Geçmiş konuşmalar
        for role, message in history:

            if not message:
                continue

            role = role.lower().strip()

            if role not in ("user", "assistant"):
                continue

            messages.append(
                {
                    "role": role,
                    "content": message
                }
            )

        # Yeni kullanıcı mesajı
        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        last_error = None

        for attempt in range(3):

            try:

                response = self.client.chat.completions.create(

                    model=self.model_name,

                    temperature=0,

                    messages=messages

                )

                answer = response.choices[0].message.content.strip()

                return answer

            except Exception as e:

                last_error = e

                print(f"Deneme {attempt + 1}: {e}")

                if "429" in str(e):

                    wait = (2 ** (attempt + 1)) + random.uniform(0.5, 1.5)

                    print(f"{wait:.1f} sn bekleniyor...")

                    time.sleep(wait)

                else:
                    raise

        raise last_error