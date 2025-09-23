from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherResponse(BaseModel):
    conditions: str

checkpointer = InMemorySaver()

config={"configurable": {"user_name": "Filipe Barros","thread_id": "1"}}

def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:  
    user_name = config["configurable"].get("user_name")
    system_msg = f"You are a helpful assistant. Address the user as {user_name}."
    return [{"role": "system", "content": system_msg}] + state["messages"]


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key = os.getenv("GEMINI_API_KEY"))


agent = create_react_agent(
    model=model,
    tools=[get_weather],
    prompt="You are a helpful assistant",
    checkpointer = checkpointer,
    response_format = WeatherResponse
)

sf_response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    config=config
)

la_response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in la"}]},
    config=config
)

print(sf_response["structured_response"])
print(la_response["structured_response"])
