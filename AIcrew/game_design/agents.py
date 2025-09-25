from crewai import Agent, LLM
import os
from crewai_tools import BraveSearchTool
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model = "gemini/gemini-2.5-flash",
    api_key= os.getenv("GEMINI_API_KEY")
)

game_dev_agent = Agent(
    llm = llm,
    role = "Desenvolvedor senior de jogos",
    goal = "Criar o sorftware necessário",
    backstory= "Você é um desenvolvedor de games senior de uma grande empresa mundial de jogos."
                "Você é um especialista na linguagem Python e sempre da o seu melhor nas suas criações",
    tools = [],
    verbose = True,
)

revisor_agent = Agent(
    llm = llm,
    role = "Revisor de códigos em python",
    goal =  "Revisar o código fornecido para garantir que não haja erros e esteja perfeito",
    backstory = "Você é um engenheiro de sorfware especialista em analíse de códigos em Python"
                "Seu trabalho é procurar erros e falhas em códigos para garantir o funcionamento perfeito" \
                " do mesmo. Você procura por erros de lógica,identação,técnicos e bugs e sempre se" \
                "preocupa em entregar o melhor trabalho.",
    tools = [],
    verbose = True, 
)   

chief_revisor_agent = Agent(
    llm = llm,
    role = "Você é o chefe da area de revisão da empresa",
    goal = "Seu objetivo é garantir que o código faça exatamente aquilo que se espera dele",
    backstory= "Você sempre procura por erros e garante em entregar códigos da melhor qualidade possível",
    tools = [],
    verbose = True,
)