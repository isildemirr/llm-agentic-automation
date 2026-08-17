import os
import streamlit as st

from llm import LLMClient
from agent import Agent
from export import create_pdf, create_excel

from database import (
    create_database,
    create_chat,
    get_all_chats,
    load_messages,
    clear_messages,
    delete_chat,
    update_chat_title,
)

# ======================================================
# DATABASE
# ======================================================

create_database()

# ======================================================
# PAGE
# ======================================================

st.set_page_config(
    page_title="Finance Copilot",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Finance Copilot AI")

# ======================================================
# SESSION
# ======================================================

if "chat_id" not in st.session_state:

    chats = get_all_chats()

    if chats:

        st.session_state.chat_id = chats[0][0]

    else:

        st.session_state.chat_id = create_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_file_path" not in st.session_state:
    st.session_state.uploaded_file_path = None

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

# ======================================================
# AGENT
# ======================================================

@st.cache_resource
def load_agent():

    llm = LLMClient()

    return Agent(llm)

agent = load_agent()

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.title("💰 Finance Copilot")

    if st.button(
        "➕ Yeni Sohbet",
        use_container_width=True,
    ):

        new_chat = create_chat()

        st.session_state.chat_id = new_chat
        st.session_state.messages = []

        st.session_state.uploaded_file_path = None
        st.session_state.uploaded_file_name = None

        st.rerun()

    st.divider()

    st.subheader("🕘 Sohbetler")
        # ======================================================
    # CHAT LIST
    # ======================================================

    chats = get_all_chats()

    for chat in chats:

        chat_id = chat[0]
        title = chat[1]

        col1, col2 = st.columns([5, 1])

        with col1:

            button_type = (
                "primary"
                if chat_id == st.session_state.chat_id
                else "secondary"
            )

            if st.button(
                title,
                key=f"chat_{chat_id}",
                use_container_width=True,
                type=button_type,
            ):

                st.session_state.chat_id = chat_id
                st.session_state.messages = []

                st.session_state.uploaded_file_path = None
                st.session_state.uploaded_file_name = None

                for role, message in load_messages(chat_id):

                    st.session_state.messages.append(
                        {
                            "role": role,
                            "content": message,
                        }
                    )

                st.rerun()

        with col2:

            if st.button(
                "🗑️",
                key=f"delete_{chat_id}",
            ):

                delete_chat(chat_id)

                chats = get_all_chats()

                if chats:

                    st.session_state.chat_id = chats[0][0]

                else:

                    st.session_state.chat_id = create_chat()

                st.session_state.messages = []
                st.session_state.uploaded_file_path = None
                st.session_state.uploaded_file_name = None

                st.rerun()

    st.divider()

    # ======================================================
    # FILE UPLOAD
    # ======================================================

    uploaded_file = st.file_uploader(
        "📁 Dosya Yükle",
        type=[
            "pdf",
            "txt",
            "csv",
            "xlsx",
            "docx",
        ],
    )

    if uploaded_file is not None:

        os.makedirs("uploads", exist_ok=True)

        file_path = os.path.join(
            "uploads",
            uploaded_file.name,
        )

        with open(file_path, "wb") as f:

            f.write(uploaded_file.getbuffer())

        st.session_state.uploaded_file_path = file_path
        st.session_state.uploaded_file_name = uploaded_file.name

        st.success(f"✅ {uploaded_file.name} yüklendi.")

    if st.session_state.uploaded_file_name:

        st.info(
            f"📄 Aktif Dosya\n\n{st.session_state.uploaded_file_name}"
        )

    st.divider()
        # ======================================================
    # SYSTEM TRACE
    # ======================================================

    with st.expander("🛡️ System Trace", expanded=False):

        if "audit_log" in st.session_state:

            audit = st.session_state.audit_log

            st.write("### 🛠 Tool")
            st.info(audit.get("tool", "-"))

            st.write("### 🤖 Model")
            st.info(audit.get("model", "-"))

            st.write("### 📄 Doküman")
            st.info(audit.get("document", "-"))

            st.write("### ⚡ Süre")
            st.success(audit.get("response_time", "-"))

            st.write("### 🔒 Güvenlik")

            for item in audit.get("security", []):

                st.success(item)

            st.write("### ✅ Durum")
            st.success(audit.get("status", "-"))

    st.divider()

    # ======================================================
    # CLEAR CHAT
    # ======================================================

    if st.button(
        "🗑️ Bu Sohbeti Temizle",
        use_container_width=True,
    ):

        clear_messages(st.session_state.chat_id)

        st.session_state.messages = []

        st.rerun()

# ======================================================
# LOAD CHAT
# ======================================================

if len(st.session_state.messages) == 0:

    for role, message in load_messages(
        st.session_state.chat_id
    ):

        st.session_state.messages.append(
            {
                "role": role,
                "content": message,
            }
        )

# ======================================================
# CHAT
# ======================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ======================================================
# USER INPUT
# ======================================================

if prompt := st.chat_input("Mesajınızı yazın..."):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.spinner("🤖 Finance Copilot düşünüyor..."):

        response, audit_log = agent.run(
            st.session_state.chat_id,
            prompt,
            st.session_state.get("uploaded_file_path"),
        )

        st.session_state.audit_log = audit_log
        # İlk mesajdan sohbet başlığını oluştur
    chats = get_all_chats()

    current_title = ""

    for chat in chats:

        if chat[0] == st.session_state.chat_id:

            current_title = chat[1]

            break

    if current_title == "Yeni Sohbet":

        title = prompt.strip()

        if len(title) > 40:

            title = title[:40] + "..."

        update_chat_title(
            st.session_state.chat_id,
            title,
        )

    with st.chat_message("assistant"):

        st.markdown(response)

        pdf = create_pdf(response)

        st.download_button(
            "📄 PDF İndir",
            data=pdf,
            file_name="analiz.pdf",
            mime="application/pdf",
            key=f"pdf_{len(st.session_state.messages)}",
        )

        excel = create_excel(response)

        st.download_button(
            "📊 Excel İndir",
            data=excel,
            file_name="analiz.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"excel_{len(st.session_state.messages)}",
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    st.rerun()

# ======================================================
# FOOTER
# ======================================================

st.divider()

st.caption(
    "💰 Finance Copilot AI | Financial Report Analysis • RAG • Compliance Checker • Audit Log"
)