from app.rag.vectorstore import vectorstore

def save_search(text: str, metadata: dict):
    vectorstore.add_texts([text], metadatas=[metadata])

def search_similar(query: str, k: int = 3):
    return vectorstore.similarity_search(query, k=k)