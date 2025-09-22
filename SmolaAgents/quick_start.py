from smolagents import CodeAgent, InferenceClientModel, DuckDuckGoSearchTool
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("HUGGING_FACE_TOKEN")
model = InferenceClientModel(token=token)

agent = CodeAgent(tools=[DuckDuckGoSearchTool()],model = model)

result = agent.run("What is the current weather in Paris?")

print(result)