from app.agents.travel_agent import agent_executor
from app.rag.retriever import retrieve_memories
# result = agent_executor.invoke({
#     "messages": [
#         ("human", "Plan a budget trip under $700 from Delhi to Dubai in April")
#     ]
# })

# print(result["messages"][-1].content)
from app.rag.vectorstore import get_vector_store

get_vector_store().add_texts(
    texts=[
        "User prefers budget international trips from Delhi under $700",
        "User likes travel in April and avoids luxury hotels"
    ],
    metadatas=[
        {"user_id": "test_user"},
        {"user_id": "test_user"}
    ]
)

docs = get_vector_store().similarity_search(
    "budget trip from Delhi",
    k=5
)

print("Docs found:", len(docs))

for doc in docs:
    print("----")
    print("Text:", doc.page_content)
    print("Metadata:", doc.metadata)

result =retrieve_memories("user_001","Travel Plan from Delhi to Dubai",5)

print(result)
print("✅ Memory stored")