from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from file_reader import read_document

_embeddings = None

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

_VECTORSTORE_CACHE = {}


def get_embeddings():
    global _embeddings

    if _embeddings is None:
        from langchain_huggingface import HuggingFaceEmbeddings

        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embeddings


def _build_pdf_documents(pdf_path: Path):

    documents = []

    reader = PdfReader(str(pdf_path))

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text() or ""

        if not page_text.strip():
            continue

        docs = splitter.create_documents(
            [page_text],
            metadatas=[
                {
                    "source": str(pdf_path),
                    "page": page_number
                }
            ]
        )

        documents.extend(docs)

    return documents


def build_document_index(path):

    path = Path(path)

    documents = []

    if path.is_dir():

        pdf_files = list(path.rglob("*.pdf"))

        for pdf in pdf_files:

            try:
                documents.extend(
                    _build_pdf_documents(pdf)
                )

            except Exception as e:
                print(f"{pdf} okunamadı: {e}")

    else:

        if path.suffix.lower() == ".pdf":

            documents = _build_pdf_documents(path)

        else:

            text = read_document(str(path))

            if text and text.strip():
                documents = splitter.create_documents(
                    [text],
                    metadatas=[
                        {
                            "source": str(path)
                        }
                    ]
                )

    if not documents:
        raise ValueError(
            f"Dokümandan geçerli bir metin çıkarılamadı veya dosya boş: {path}"
        )

    vectorstore = FAISS.from_documents(
        documents,
        get_embeddings()
    )

    return vectorstore


def get_or_create_vectorstore(path):

    if not path:
        return None

    path = str(path)

    if path in _VECTORSTORE_CACHE:
        return _VECTORSTORE_CACHE[path]

    vectorstore = build_document_index(path)

    _VECTORSTORE_CACHE[path] = vectorstore

    return vectorstore


def search_document(vectorstore, query):

    if not vectorstore:
        return ""

    # Doküman özetleme için daha fazla içerik getir
    if "özet" in query.lower():
        k = 10
    else:
        k = 3

    docs = vectorstore.similarity_search(
        query,
        k=k
    )

    context = ""

    for doc in docs:

        source = Path(
            doc.metadata.get("source", "")
        ).name

        page = doc.metadata.get("page")

        page_label = (
            f" | Sayfa: {page}"
            if page else ""
        )

        context += (
            f"Kaynak: {source}{page_label}\n"
            f"{doc.page_content}\n\n"
        )

    return context