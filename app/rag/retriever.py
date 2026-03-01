from app.rag.vectorstore import get_vector_store

def retrieve_memories(user_id: str, query: str, k: int = 5) -> str:
    store = get_vector_store()
    docs = store.similarity_search(query, k=k)

    filtered = [
        d for d in docs
        if d.metadata.get("user_id") == user_id
           and not d.metadata.get("bootstrap")
    ]

    if not filtered:
        return "No prior user memory."

    return "\n".join(
        f"- ({d.metadata.get('type')}): {d.page_content}"
        for d in filtered
    )