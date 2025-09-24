from agno.agent import Agent  
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
import os
from dotenv import load_dotenv 

load_dotenv()

model = Gemini(id = "gemini-2.5-flash",provider= "gemini",api_key = os.getenv("GEMINI_API_KEY"))
searcher = DuckDuckGoTools()

agent = Agent(
    model = model,
    description = "Você é um excelente repórter e entusiasta de futebol",
    tools=[searcher],
    markdown= True
)

agent.print_response("Me fale quem é o ganhador mais recente do prêmio Ballon'dor",stream= True)