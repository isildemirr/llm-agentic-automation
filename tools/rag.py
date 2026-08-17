from rag import search_documents

def rag_tool(question: str):
    return search_documents(question)