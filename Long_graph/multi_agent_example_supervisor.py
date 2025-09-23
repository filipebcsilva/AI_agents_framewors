from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from langgraph.graph import StateGraph, START, END
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
    next_agent: Literal["agent_1", "agent_2", "__end__"] = Field(
        description="The name of the next agent.If the question is about products, go to 'agent_1'.If the question is about finance and subscriptions, go to 'agent_2'. " 
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


def supervisor(state: AgentState) -> Command[Literal["agent_1", "agent_2", END]]:
    system_prompt = """
            Your task is to analyse the conversation and decide which one of the agents should
            be next: 'agent_1' or 'agent_2'.
            ROUTING RULES:
            1. FOCUS on the user's last message (HumanMessage). Ignore responses from other agents.
            2. If the user's last question is about features or product usage, choose 'agent_1'.
            3. If the user's last question is about pricing, subscriptions, or billing, choose 'agent_2'.

            ENDING RULES:
            4. If the last message in the history was a complete response from an expert (agent_1 or agent_2) and the user did not ask a new question, the task is complete. Choose '__end__'.

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

def agent_1(state: AgentState) -> Command[Literal["supervisor"]]:
    system_prompt = """
            You are product especialist. Your task is to answer questions about the funcionality of our sorftware and then
            return the control to the supervisor.
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

def agent_2(state: AgentState) -> Command[Literal["supervisor"]]:
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
builder.add_node(agent_1)
builder.add_node(agent_2)

builder.set_entry_point("supervisor")


def router_function(state: AgentState) -> str:
    return state["next_agent"]

builder.add_conditional_edges(
    "supervisor",
    router_function,
    {
        "agent_1": "agent_1",
        "agent_2": "agent_2",
        "__end__": END
    }
)

builder.add_edge("agent_1", "supervisor")
builder.add_edge("agent_2", "supervisor")

graph = builder.compile()

if __name__ == "__main__":
    initial_state = {
        "messages": [HumanMessage(content="How much is the premium plan")],
        "next_agent": ""
    }
    for event in graph.stream(initial_state):
        for key, value in event.items():
            print(f"Node: '{key}'")
            print(f"State: {value}\n------------------")