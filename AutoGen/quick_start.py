from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
)

async def get_weather(city: str) -> str:
    return f"The weather in {city} is 73 degrees and Sunny."

agent = AssistantAgent(
    name="weather_agent",
    model_client=model_client,
    tools=[get_weather],
    system_message="You are a helpful assistant.",
    reflect_on_tool_use=True,
    model_client_stream=True, 
)

async def main() -> None:
    await Console(agent.run_stream(task="What is the weather in New York?"))
    await model_client.close()


asyncio.run(main())