from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command
from IPython.display import Image, display
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
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

class SupervisorRouter(BaseModel):
    next_agent: Literal["product_agent", "subscription_agent", "__end__"] = Field(
        description="The name of the next agent.If the question is about products, go to 'product_agent'.If the question is about finance and subscriptions, go to 'subscription_agent'. " 
        "If the question was answered use __end__ to end the conversation."
    )
    content: str = Field(
        description="Generate a confirmation message to the user, informing them of the specialist they're being forwarded to. "
        "For example: 'Sure, I'm transferring you to our financial specialist."
    )
    
class WorkerRouter(BaseModel):
    next_agent: Literal["supervisor"] = Field( 
        description="Needs to be the supervisor always"
        )
    content: str = Field( 
        description="The complete answaer to the user's question"
    )

supervisor_model = model.with_structured_output(SupervisorRouter)
worker_model = model.with_structured_output(WorkerRouter)


def supervisor(state: AgentState) -> Command[Literal["product_agent", "subscription_agent", END]]:
    system_prompt = """
            Your task is to analyse the conversation and decide which one of the agents should
            be next: 'product_agent' or 'subscription_agent'.
            ROUTING RULES:
            1. FOCUS on the user's last message (HumanMessage). Ignore responses from other agents.
            2. If the user's last question is about features or product usage, choose 'product_agent'.
            3. If the user's last question is about pricing, subscriptions, or billing, choose 'subscription_agent'.

            ENDING RULES:
            4. If the last message in the history was a complete response from an expert (product_agent or subscription_agent) and the user did not ask a new question, the task is complete. Choose '__end__'.

            DO NOT attempt to answer the question. Your response in the 'content' field should ONLY be a short status message, reflecting the action taken.

    """
    messages = [SystemMessage(content = system_prompt)] + state["messages"]
    response = supervisor_model.invoke(messages)

    new_message = AIMessage(content=response.content)
    
    update_dict = {
        "messages": state["messages"] + [new_message],
        "next_agent": response.next_agent
    }
     
    return Command(
        goto=response.next_agent,
        update=update_dict,
    )

def product_agent(state: AgentState) -> Command[Literal["supervisor"]]:
    system_prompt = """
            You are product especialist. Your task is to answer questions about the products of our shop and then
            return the control to the supervisor.
            ---PRODUCT INFORMATION---
            - Notebook: 500$ or 5x100$
            - TV: 200$ or 4x50$
            - Iphone 17:1000$ or 2x500$.
            --------------------------
            """
            
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = worker_model.invoke(messages)
    
    new_message = AIMessage(content=response.content)
    
    update_dict = {
        "messages": state["messages"] + [new_message],
        "next_agent": response.next_agent
    }
     
    return Command(
        goto=response.next_agent,
        update=update_dict,
    )

def subscription_agent(state: AgentState) -> Command[Literal["supervisor"]]:
    system_prompt = """
            You are finances and subscriptions especialist. Your task is to answer questions about the subscriptions of our sorftware and then
            return the control to the supervisor.
            --- INTERNAL INFORMATION ---
            - Basic Plan: $10 per month or $100 per year. Includes features X, Y, and Z.
            - Premium Plan: $25 per month or $250 per year. Includes all Basic features plus A, B, and C.
            - Enterprise Plan: Contact us for a personalized quote.
            --------------------------
            """
            
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = worker_model.invoke(messages)
    
    new_message = AIMessage(content=response.content)
    
    update_dict = {
        "messages": state["messages"] + [new_message],
        "next_agent": response.next_agent
    }
     
    return Command(
        goto=response.next_agent,
        update=update_dict,
    )

builder = StateGraph(AgentState)
builder.add_node(supervisor)
builder.add_node(product_agent)
builder.add_node(subscription_agent)

builder.set_entry_point("supervisor")

graph = builder.compile()


png_data = graph.get_graph().draw_mermaid_png(max_retries=5,retry_delay=2.0)
display(Image(png_data))

if __name__ == "__main__":
    initial_state = {
        "messages": [HumanMessage(content="How much is the premium plan")],
        "next_agent": ""
    }
    for event in graph.stream(initial_state):
        for key, value in event.items():
            print(f"Node: '{key}'")
            print(f"State: {value}\n------------------")