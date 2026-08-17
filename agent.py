import time
from database import save_message
from guardrail import mask_sensitive_data

from document_rag import (
    get_or_create_vectorstore,
    search_document,
)

from tools.document_summary import document_summary_tool
from tools.email import email_tool
from tools.financial_report import financial_report_tool

try:
    from tools.compliance_checker_tool import compliance_checker_tool
except Exception as e:
    import traceback

    print("\n" + "=" * 50)
    print("🔥 GERÇEK HATA YAKALANDI 🔥")
    print(traceback.format_exc())
    print("=" * 50 + "\n")
    raise e


class Agent:

    def __init__(self, llm):
        self.llm = llm

    def run(
        self,
        chat_id: int,
        user_input: str,
        file_path: str = None,
    ):

        start_time = time.time()

        # ======================================================
        # Guardrail
        # ======================================================

        safe_input, detected = mask_sensitive_data(user_input)

        if detected:
            print("🛡️ Maskelenen veriler:", ", ".join(detected))

        save_message(
            chat_id,
            "user",
            safe_input
        )

        # ======================================================
        # Tool Seçimi
        # ======================================================

        decision = self.llm.analyze(safe_input)

        tool_name = decision.get(
            "tool",
            "general_response"
        )

        print(f"Seçilen Tool: {tool_name}")

        # ======================================================
        # VectorStore
        # ======================================================

        vectorstore = None

        if (
            file_path
            and tool_name in [
                "financial_report_tool",
                "document_summary_tool",
                "finance_rag_tool",
                "compliance_checker_tool",
            ]
        ):

            vectorstore = get_or_create_vectorstore(
                file_path
            )

        source = file_path if file_path else "Yok"

        # ======================================================
        # Financial Report
        # ======================================================

        if tool_name == "financial_report_tool":

            if vectorstore:

                context = search_document(
                    vectorstore,
                    safe_input
                )[:2000]

                answer = financial_report_tool(
                    chat_id,
                    context,
                    self.llm
                )

            else:

                answer = financial_report_tool(
                    chat_id,
                    safe_input,
                    self.llm
                )

        # ======================================================
        # Document Summary
        # ======================================================

        elif tool_name == "document_summary_tool":

            if vectorstore:

                context = search_document(
                    vectorstore,
                    
                    safe_input
                )[:2000]

                answer = document_summary_tool(
                    chat_id,
                    context,
                    self.llm
                )

            else:

                answer = document_summary_tool(
                    chat_id,
                    safe_input,
                    self.llm
                )

        # ======================================================
        # Finance RAG
        # ======================================================

        elif tool_name == "finance_rag_tool":

            if not vectorstore:

                answer = "Lütfen önce bir doküman yükleyin."

            else:

                context = search_document(
                    vectorstore,
                    safe_input
                )[:2000]

                rag_instruction = f"""
Sen finans alanında çalışan bir yapay zekâ asistansın.

Soruları SADECE aşağıdaki dokümandaki bilgilere göre cevapla.

Doküman:

{context}

Eğer cevap dokümanda yoksa:

"Bu bilgi yüklenen dokümanda bulunmuyor."

cevabını ver.

Türkçe, kısa ve net cevap ver.
"""

                answer = self.llm.generate_response(
                    chat_id=chat_id,
                    user_input=safe_input,
                    system_instruction=rag_instruction,
                )

        # ======================================================
        # Compliance Checker
        # ======================================================

        elif tool_name == "compliance_checker_tool":

            answer = compliance_checker_tool(
                chat_id=chat_id,
                user_input=safe_input,
                llm=self.llm,
                document_path=file_path,
            )

        # ======================================================
        # Email
        # ======================================================

        elif tool_name == "finance_email_tool":

            answer = email_tool(
                chat_id,
                safe_input,
                self.llm
            )

        # ======================================================
        # General Chat
        # ======================================================

        else:

            # ✅ DÜZELTİLDİ: Parametre sıralaması ve keyword tanımı bütünüyle düzeltildi
            answer = self.llm.generate_response(
                chat_id=chat_id,
                user_input=safe_input
            )

        # ======================================================
        # DATABASE
        # ======================================================

        save_message(
            chat_id,
            "assistant",
            answer
        )

        # ======================================================
        # AUDIT LOG
        # ======================================================

        elapsed = round(
            time.time() - start_time,
            2
        )

        audit_log = {

            "tool": tool_name,

            "model": self.llm.model_name,

            "response_time": f"{elapsed} sn",

            "document": source,

            "security": [
                "PII Masking",
                "Prompt Guardrail",
            ],

            "status": "Başarılı",
        }

        return answer, audit_log