from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
from typing import Literal

class AgentState(TypedDict):
    messages: List[BaseMessage]
    next_agent: str 
    
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key = "AIzaSyDv_8QbuzZuPn_sXhrKW-4o5LAn0tJxltU")

class Router(BaseModel):
    next_agent: Literal["agent_2", "agent_3", "__end__"] = Field(
        description="The name of the next agent.If the question is about products, go to 'agent_2'.If the question is about finance and subscriptions, go to 'agent_3'. " 
        "If the question was answered use __end__ to end the conversation."
    )
    content: str = Field(
        description="Generate a confirmation message to the user, informing them of the specialist they're being forwarded to. "
        "For example: 'Sure, I'm transferring you to our financial specialist."
    )
    
structered_model = model.with_structured_output(Router)

class Router2(BaseModel):
    next_agent: Literal["agent_1","agent_2" ,"agent_3", "__end__"] = Field(
        description="""Your decision about the next step. RULES:
        - If you've fully answered the user's question about the product, choose '__end__'.
        - If the user asked a new question about pricing or subscriptions, choose 'agent_3'.
        - If you're unsure or the question is ambiguous, return control to the main router by choosing 'agent_1'.
        """

    )
    content: str = Field(
        description="The answer of the user's question about the product"
    )

structered_model2 = model.with_structured_output(Router2)


class Router3(BaseModel):
    next_agent: Literal["agent_1", "agent_2", "__end__"] = Field(
        description="""Your decision about the next step. RULES:
        - If you've fully answered the user's question about finances, choose '__end__'.
        - If the user asked a new question about product features, choose 'agent_2'.
        - If you're unsure or the question is ambiguous, return control to the main router by choosing 'agent_1'.
        """

    )
    content: str = Field(
        description="The answer of the user's question about finances"
    )

structered_model3 = model.with_structured_output(Router3)

def agent_1(state: AgentState) -> Command[Literal["agent_2", "agent_3", END]]:
    
    system_prompt = """
            Your task is to analyse the conversation and decide which one of the agents should
            be next: 'agent_2' or 'agent_3'.
            ROUTING RULES:
            1. FOCUS on the user's last message (HumanMessage). Ignore responses from other agents.
            2. If the user's last question is about features or product usage, choose 'agent_2'.
            3. If the user's last question is about pricing, subscriptions, or billing, choose 'agent_3'.

            ENDING RULES:
            4. If the last message in the history was a complete response from an expert (agent_2 or agent_3) and the user did not ask a new question, the task is complete. Choose '__end__'.

            DO NOT attempt to answer the question. Your response in the 'content' field should ONLY be a short status message, reflecting the action taken.

    """
    
    messages = [SystemMessage(content = system_prompt)] + state["messages"]
    response = structered_model.invoke(messages)

    new_message = AIMessage(content=response.content)
    
    update_dict = {
        "messages": state["messages"] + [new_message],
        "next_agent": response.next_agent
    }
     
    return Command(
        goto=response.next_agent,
        update=update_dict,
    )

def agent_2(state: AgentState) -> Command[Literal["agent_1", "agent_3", END]]:
    
    system_prompt = """
            You are product especialist. Your task is to answer questions about the funcionality of our sorftware and then
            decide what is the next step:
            - If you are highly confident that the user's question has been fully answered, **end the conversation** by choosing '__end__'.
            - If the user has asked a new question that belongs to another expert, forward it directly to them (e.g., 'agent_2' or 'agent_3').
            - If you are unsure or the question is ambiguous, return control to the primary router ('agent_1').
            """
            
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = structered_model2.invoke(messages)
    
    new_message = AIMessage(content=response.content)
    
    update_dict = {
        "messages": state["messages"] + [new_message],
        "next_agent": response.next_agent
    }
     
    return Command(
        goto=response.next_agent,
        update=update_dict,
    )

def agent_3(state: AgentState) -> Command[Literal["agent_1", "agent_2", END]]:
    system_prompt = """
        --- INTERNAL INFORMATION ---
        - Basic Plan: $10 per month or $100 per year. Includes features X, Y, and Z.
        - Premium Plan: $25 per month or $250 per year. Includes all Basic features plus A, B, and C.
        - Enterprise Plan: Contact us for a personalized quote.
        --------------------------

        RULES:
        1. **Use Internal Information:** Always base your answer on the prices and plans listed above. Don't invent other plans.
        2. **Be Direct:** Answer the user's question directly. If the question is generic about "price," present the available plans. Don't ask for clarification unless absolutely necessary.
        3. **Decide the Next Step:** After answering fully, decide whether the conversation is over ('__end__') or needs to be forwarded to another agent.
        """
            
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = structered_model3.invoke(messages)
    
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
builder.add_node(agent_1)
builder.add_node(agent_2)
builder.add_node(agent_3)

builder.set_entry_point("agent_1")

def router_function(state: AgentState) -> str:
    return state["next_agent"]

builder.add_conditional_edges(
    "agent_1",
    router_function,
    {
        "agent_2": "agent_2",
        "agent_3": "agent_3",
        "__end__": END
    }
)
builder.add_conditional_edges(
    "agent_2",
    router_function,
    {
        "agent_1": "agent_1",
        "agent_3": "agent_3",
        "__end__": END
    }
)
builder.add_conditional_edges(
    "agent_3",
    router_function,
    {
        "agent_1": "agent_1",
        "agent_2": "agent_2",
        "__end__": END
    }
)

network = builder.compile()

if __name__ == "__main__":
    initial_state = {
        "messages": [HumanMessage(content="Hi, I want to know the price of the subscription")],
        "next_agent": ""
    }
    for event in network.stream(initial_state):
        print(event)
        print("---")