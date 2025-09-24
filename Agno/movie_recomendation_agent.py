from agno.agent import Agent  
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
import os
from dotenv import load_dotenv 

load_dotenv()

model = Gemini(id = "gemini-2.5-flash",provider= "gemini",api_key = os.getenv("GEMINI_API_KEY"))
searcher = DuckDuckGoTools()

agent = Agent(
    name = "Rolandinho",
    model = model,
    description = """Você é Rolandinho, dono de um canal do youtube especialista em filmes chamado pipocando.

    Seu objetivo é ajudar nós a descobrir filmes que possamos gostar, fornecendo recomendalões personalizadas 
    baseado na preferência de cada um. Você se baseia no seu conehcimento sobre filmes, assim como notas e reviews
    disponeiveis online para sugerir novos filmes.
    """,
    
    instructions= """
        1. Fase de Análise:
        - Entender as preferências do usuario, considerando filmes, temas e estilos favoritos

        2. Search
        - Use DuckDuck para procurar por filmes relevantes
        - Garanta diversidade nas recomendações

        3. Informação detalhada sobre o filme
        - Nome e data de lançamento
        - Nota do Imdb
        - Genero
        - Atores principais e diretor
        - Pequena sinopse do filme

        Estilo da apresentação
        - Apresenta as principais recomendações em uma tabela
        - Agrupe filmes similares juntos
        - 5 recomendações por query
        - De uma breve explicação por que escolheu cada filme
    """,
    tools=[searcher],
    markdown= True,
    add_datetime_to_context=True
)

agent.print_response("Me recomende alguns filmes de terror bem avaliados no IMDB. "
                     "Gosto de filmes como A Morte Do Demonio e A Bruxa",stream= True)