from crewai import Task
from agents import game_dev_agent,revisor_agent,chief_revisor_agent

game_dev_task = Task(
    description= """ Você ira criar um jogo em python baseado em instruções" 
    Instrucões: {game}
    """,
    expected_output= "Seu output será um código em python capaz de executar o jogo",
    agent = game_dev_agent
)

revisor_task = Task(
    description= """
    Você ira criar um jogo em python dado as instruções 
    Instrucões: {game}"
    Usando o código que você tem,procure por erros.Revise erros de lógica,erros de sintaxe
    imports que estão faltando,erros de identação e vulnerabilidades de segurança""",
    expected_output= "Um código em Python revisado",
    agent= revisor_agent
    )

chief_revisor_task = Task(
    description = """Você está criando um jogo em python dado as instruções
    Instrucões: {game}"
    Você ira ler e revisar o código que recebeu e garantir sua funcionalidade completa e que está perfeito
    """,
    expected_output= "Seu output será um código em python revisado e funcional",
    agent= chief_revisor_agent
)