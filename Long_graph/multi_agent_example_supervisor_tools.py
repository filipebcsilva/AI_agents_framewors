from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from typing_extensions import TypedDict, List
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import BaseMessage

import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[BaseMessage]
    
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key = os.getenv("GEMINI_API_KEY"))

@tool
def product_agent(query:str) -> str:
    """ Use this tool to answer question about the funcionality of our sorftware"""
    system_prompt = """
            You are product especialist. Your task is to answer questions about the products of our shop.
            ---PRODUCT INFORMATION---
            - Notebook: 500$ or 5x100$
            - TV: 200$ or 4x50$
            - Iphone 17:1000$ or 2x500$.
            --------------------------
            """
            
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]
    response = model.invoke(messages)
    return response.content
    

@tool
def subscription_agent(query:str) -> str:
    """ Use this tool to answer question about our subscriptions and products"""
    system_prompt = """
            You are finances and subscriptions especialist. Your task is to answer questions about the our subscriptions.
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

tools = [product_agent,subscription_agent]
supervisor = create_react_agent(
    model = model,
    tools = tools,
    prompt="""
            Your task is to analyse the conversation and decide which one of the tools you should use
            ROUTING RULES:
            1. FOCUS on the user's last message (HumanMessage). Ignore responses from other agents.
            2. If the user's last question is about features or product usage, choose tool 'product_agent'.
            3. If the user's last question is about pricing, subscriptions, or billing, choose tool 'subscription_agent'.

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