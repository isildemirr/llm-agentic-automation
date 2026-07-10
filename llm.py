# class LLMClient:
#     def generate(self, prompt: str) -> str:
#         prompt_lower = prompt.lower()

#         if "pdf" in prompt_lower or "özet" in prompt_lower:
#             return "Bu görev için önce dosya okunmalı, sonra içerik özetlenmelidir."
#         if "hatırlat" in prompt_lower or "yarın" in prompt_lower or "saat" in prompt_lower:
#             return "Bu görev için hatırlatma aracı kullanılmalıdır."
#         if "mail" in prompt_lower or "e-posta" in prompt_lower:
#             return "Bu görev için profesyonel bir e-posta taslağı oluşturulmalıdır."

#         if "hesap" in prompt_lower or "+" in prompt_lower or "*" in prompt_lower:
#             return "Bu görev için hesaplama aracı kullanılmalıdır."

#         return "Kullanıcı isteği analiz edildi. Uygun işlem planlanmalıdır."
class LLMClient:
    def generate(self, prompt: str) -> str:
        prompt_lower = prompt.lower()

        if "hatırlat" in prompt_lower:
            return "hatırlatma aracı"

        if any(operator in prompt for operator in ["+", "-", "*", "/"]):
            return "hesaplama aracı"
        if "mail" in prompt_lower or "e-posta" in prompt_lower:
            return "e-posta aracı"
        return "Uygun araç bulunamadı."