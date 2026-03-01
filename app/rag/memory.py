from app.rag.vectorstore import get_vector_store
from app.rag.schemas import MemoryRecord


def save_memory(record: MemoryRecord):
    print("🔥 SAVE_MEMORY CALLED")
    print("Content:", record.content)
    print("Metadata:", record.metadata)

    get_vector_store().add_texts(
        texts=[record.content],
        metadatas=[record.metadata]
    )

