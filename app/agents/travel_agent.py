from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent

from app.tools.weather import get_weather
from app.tools.flights import search_flights
from app.tools.hotels import search_hotels

# Claude model (tool calling is native)
llm = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    temperature=0.3
)

tools = [
    get_weather,
    search_flights,
    search_hotels
]

# Claude understands tool calls without ReAct helpers
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a travel planning assistant. Use tools when needed."),
    ("human", "{input}")
])

# Bind tools directly to model (THIS IS THE KEY)
agent = prompt | llm.bind_tools(tools)

agent_executor = create_agent(
    model=llm,
    tools=tools
)