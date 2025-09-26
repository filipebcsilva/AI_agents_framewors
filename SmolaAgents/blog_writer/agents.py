from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    LiteLLMModel,
    DuckDuckGoSearchTool,
)
from dotenv import load_dotenv
import os

load_dotenv()


model = LiteLLMModel(model_id="gemini/gemini-2.5-flash",
                     api_key=os.getenv("GEMINI_API_KEY"))


research_agent = ToolCallingAgent(
    model = model,
    tools=[DuckDuckGoSearchTool()],
    name="super_researcher",
    description="Pesquisa tópicos exaustivamente usando pesquisas na web e extração de conteúdo. Fornece o tópico da pesquisa como entrada.",
)

research_checker_agent = CodeAgent(
    model = model,
    tools=[],
    name="research_checker",
    description="Verifica a relevância da pesquisa para a tarefa original solicitada. Se a pesquisa não for relevante, serão solicitadas mais pesquisas.",
)

writer_agent = CodeAgent(
    model = model,
    tools=[],
    name="writer",
    description="Escreve posts de blog com base em pesquisas verificadas. Apresenta os resultados da pesquisa e o tom/estilo desejado.",
)

copy_editor = CodeAgent(
    model = model,
    tools=[],
    name="editor",
    description="Revisa e aprimora a publicação do blog com base na pesquisa e na solicitação da tarefa original. Organiza a publicação final do blog e quaisquer listas de forma que sejam mais envolventes para quem trabalha com IA. Fornece a versão final editada em markdown.",
)

blog_manager = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[research_agent,research_checker_agent, writer_agent,copy_editor],
    additional_authorized_imports=["re"],
    description = """Você é o gerente do blog. Você é responsavel por toda a organização.Escolha entre fazer os agentes de pesquisa, escrita e edição
    Siga estes passos:
    1. Use o research_agent para coletar informações
    2. Passe a pesquisa para o research_checker_agent para verificar a relevância
    3. Passe a pesquisa para o writer_agent para criar o rascunho inicial
    4. Envie o rascunho ao editor para o acabamento final
    4. Salve o arquivo markdown final
    """
)

result = blog_manager.run(f"""Crie um post de blog sobre Lionel Messi""")
print(result)