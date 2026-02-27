from app.agents.travel_agent import agent_executor

result = agent_executor.invoke({
    "messages": [
        ("human", "Plan a budget trip under $700 from Delhi to Dubai in April")
    ]
})

print(result["messages"][-1].content)