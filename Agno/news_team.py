from agno.agent import Agent  
from agno.team import Team
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
import os
from dotenv import load_dotenv 

load_dotenv()

model = Gemini(id = "gemini-2.5-flash",provider= "gemini",api_key = os.getenv("GEMINI_API_KEY"))

search_tool = DuckDuckGoTools()

searcher = Agent(
    name = "Searcher Agent",
    model = model,
    role = "Procura pelas principais urls de um tópico",
    instructions= """
        Dado um certo tópico, crie uma lista de 3 termos relacionados a o tópico
        Para cada termo, procure na web e analise os resultados.
        Retorne as 10 Urls mais relevantes do tópico
    """
)

writer = Agent(
    name = "Writer Agent",
    model = model,
    description= """Você é um grande escritor do New York Times. Dado um tópico, seu objetivo é escrever um 
    ótimo artigo baseado em uma lista de Urls
    """,
    instructions= """
        1. Leia todas as urls usando read_article
        2. Escreva o artigo baseado nas Urls
        3. O artigo deve ser bem escrito, informativo e atraente
        4. Foque em fatos reais e não invente informações
        Você é um escritor do New York, logo a qualidade do artigo é muito importante
    """,
    tools= [Newspaper4kTools],
    add_datetime_to_context=True,
)

editor = Team(
    name = "Editor",
    model = model,
    description= """
    Você é um grande editor do New York Times. Dado um tópico, seu objetivo é escrever um 
    ótimo artigo.
    """,
    members = [searcher,writer],
    instructions="""
    1. Primeiro peça para o searcher journalist para procurar na web uma lista dos Urls mais relevantes do tópico
    2. Após isso, peça para o writer escrever um artigo baseado no tópico e na lista de urls
    3. Edite, revise e refina o arigo para ter a qualidade no nível do New York times
    Lembre que vocẽ é a ultima pessoa a mexer no artigo antes do lançamento. Garante que esteja perfeito
    """,
    add_datetime_to_context=True,
    markdown=True,
    debug_mode=True,
    show_members_responses=True,
)

editor.print_response("Escreva um artigo sobre câncer de pele")