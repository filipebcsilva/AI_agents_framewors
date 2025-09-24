from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from langgraph.graph import StateGraph, START, END
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
    next_agent: str 
    
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key = os.getenv("GEMINI_API_KEY"))


def agent_1(state: Annotated[dict, InjectedState]):
    system_prompt = """
            You are product especialist. Your task is to answer questions about the funcionality of our sorftware and then
            return the control to the supervisor.
            """
            
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = model.invoke(messages)
    
    new_message = AIMessage(content=response.content)
    
    update_dict = {
        "messages": state["messages"] + [new_message],
        "next_agent": response.next_agent
    }
     
    return Command(
        goto=response.next_agent,
        update=update_dict,
    )

def agent_2(state: Annotated[dict, InjectedState]):
    system_prompt = """
            You are finances and subscriptions especialist. Your task is to answer questions about the funcionality of our sorftware and then
            return the control to the supervisor.
            --- INTERNAL INFORMATION ---
            - Basic Plan: $10 per month or $100 per year. Includes features X, Y, and Z.
            - Premium Plan: $25 per month or $250 per year. Includes all Basic features plus A, B, and C.
            - Enterprise Plan: Contact us for a personalized quote.
            --------------------------
            """
            
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = model.invoke(messages)
    
    new_message = AIMessage(content=response.content)
    
    update_dict = {
        "messages": state["messages"] + [new_message],
        "next_agent": response.next_agent
    }
     
    return Command(
        goto=response.next_agent,
        update=update_dict,
    )

tools = [agent_1,agent_2]
supervisor = create_react_agent(
    model = model,
    tools = tools,
    prompt="""
            Your task is to analyse the conversation and decide which one of the agents should
            be next: 'agent_1' or 'agent_2'.
            ROUTING RULES:
            1. FOCUS on the user's last message (HumanMessage). Ignore responses from other agents.
            2. If the user's last question is about features or product usage, choose 'agent_1'.
            3. If the user's last question is about pricing, subscriptions, or billing, choose 'agent_2'.

            ENDING RULES:
            4. If the last message in the history was a complete response from an expert (agent_1 or agent_2) and the user did not ask a new question, the task is complete. Choose '__end__'.

            DO NOT attempt to answer the question. Your response in the 'content' field should ONLY be a short status message, reflecting the action taken. """
        )