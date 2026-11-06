# Comparação de frameworks de agentes de IA

Estudo prático de seis frameworks para construir agentes e sistemas multiagentes com LLMs. Para cada um, implementei exemplos que vão do básico até equipes de agentes que dividem tarefas, usam ferramentas e trocam informação.

O objetivo foi entender as diferenças de abstração, controle do fluxo e facilidade de uso, para escolher o framework do meu projeto de iniciação científica ([longtail_recognation_system](https://github.com/filipebcsilva/longtail_recognation_system), que acabou usando o Agno). O relatório com as conclusões está em [`AI Agents Frameworks (1).pdf`](./AI%20Agents%20Frameworks%20(1).pdf).

## O que tem em cada pasta

| Framework | Pasta | Exemplos implementados |
| --- | --- | --- |
| [CrewAI](https://github.com/crewAIInc/crewAI) | `AIcrew/` | Equipe que escreve reportagens; equipe que projeta e programa jogos (Snake, Pac-Man) |
| [Agno](https://github.com/agno-agi/agno) | `Agno/` | Equipe de agentes de notícias; agente de recomendação de filmes |
| [Atomic Agents](https://github.com/BrainBlend-AI/atomic-agents) | `AtomicAgents/` | Chatbot; sistema multiagente com ferramentas de busca na web (SearXNG) e calculadora |
| [AutoGen](https://github.com/microsoft/autogen) | `AutoGen/` | Início rápido; equipe de agentes conversando entre si |
| [LangGraph](https://github.com/langchain-ai/langgraph) | `Long_graph/` | Arquiteturas multiagente em rede e com supervisor, com e sem ferramentas |
| [smolagents](https://github.com/huggingface/smolagents) | `SmolaAgents/` | Agente gerente com busca na web que encontra locais de filmagem, calcula tempos de voo e gera um mapa; equipe que pesquisa, revisa e escreve posts para blog |

## Principais pontos comparados

- **Nível de abstração:** frameworks baseados em papéis (CrewAI) contra grafos de estados explícitos (LangGraph).
- **Controle do fluxo:** quem decide o próximo passo, o desenvolvedor ou um agente gerente.
- **Ferramentas e saídas estruturadas:** como cada um integra funções externas e valida respostas.
- **Modelos:** suporte a APIs (Gemini, OpenAI) e a modelos locais.

## Como rodar

Cada pasta tem seu próprio `requirements.txt`:

```bash
cd Agno
pip install -r requirements.txt
python news_team.py
```

Os exemplos usam principalmente o Gemini 2.5 Flash. Crie um arquivo `.env` com a sua chave (`GEMINI_API_KEY` ou `GOOGLE_API_KEY`, conforme o framework).

## Tecnologias

Python · CrewAI · Agno · Atomic Agents · AutoGen · LangGraph · smolagents · Gemini · OpenAI
