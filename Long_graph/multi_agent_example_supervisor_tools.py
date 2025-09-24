from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from langchain_core.tools import tool
from typing_extensions import TypedDict, List,Annotated
from langgraph.prebuilt import InjectedState, create_react_agent
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
from typing import Literal
import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[BaseMessage]
    
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key = os.getenv("GEMINI_API_KEY"))

@tool
def agent_1(query:str) -> str:
    """ Use this tool to answer question about the funcionality of our sorftware"""
    system_prompt = """
            You are product especialist. Your task is to answer questions about the funcionality of our sorftware and then.
            """
            
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]
    response = model.invoke(messages)
    return response.content
    

@tool
def agent_2(query:str) -> str:
    """ Use this tool to answer question about our subscriptions and products"""
    system_prompt = """
            You are finances and subscriptions especialist. Your task is to answer questions about the our products and subscriptions.
            --- INTERNAL INFORMATION ---
            - Basic Plan: $10 per month or $100 per year. Includes features X, Y, and Z.
            - Premium Plan: $25 per month or $250 per year. Includes all Basic features plus A, B, and C.
            - Enterprise Plan: Contact us for a personalized quote.
            --------------------------
            """
            
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]
    response = model.invoke(messages)
    return response.content

tools = [agent_1,agent_2]
supervisor = create_react_agent(
    model = model,
    tools = tools,
    prompt="""
            Your task is to analyse the conversation and decide which one of the tools you should use
            ROUTING RULES:
            1. FOCUS on the user's last message (HumanMessage). Ignore responses from other agents.
            2. If the user's last question is about features or product usage, choose tool 'agent_1'.
            3. If the user's last question is about pricing, subscriptions, or billing, choose tool 'agent_2'.

            ENDING RULES:
            4. If you think the conversation is over,choose __end__

        """
)

graph = StateGraph(AgentState)

graph.add_node("agent", supervisor)

graph.set_entry_point("agent")

graph.add_edge("agent", END)

graph = graph.compile()

final_result = graph.invoke(
    {"messages": "What your sorftware does?"}
)

response = final_result['messages'][-1].content

print(response)