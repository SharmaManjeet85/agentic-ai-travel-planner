from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ✅ Start with NO vectorstore
vector_store: FAISS | None = None


def get_vector_store() -> FAISS:
    global vector_store

    if vector_store is None:
        # Create a dummy first index
        vector_store = FAISS.from_texts(
            texts=["initial memory bootstrap"],
            embedding=embedding,
            metadatas=[{"bootstrap": True}]
        )

    return vector_store