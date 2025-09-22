import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


model_client = OpenAIChatCompletionClient(
    model="gemini-2.5-flash",
    api_key="AIzaSyDv_8QbuzZuPn_sXhrKW-4o5LAn0tJxltU",
)

primary_agent = AssistantAgent(
    "primary",
    model_client=model_client,
    system_message="You are a helpful AI assistant.",
)

critic_agent = AssistantAgent(
    "critic",
    model_client=model_client,
    system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed.",
)

text_termination = TextMentionTermination("APPROVE")

team = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=text_termination)

async def main():
    await Console(team.run_stream(task="Write a short poem about the fall season.")) 
    await Console(team.run_stream(task="将这首诗用中文唐诗风格写一遍。"))
asyncio.run(main())