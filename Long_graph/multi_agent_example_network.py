from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from langgraph.graph import StateGraph,END
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

class Router(BaseModel):
    next_agent: Literal["product_agent", "subscription_agent", "__end__"] = Field(
        description="The name of the next agent.If the question is about products, go to 'product_agent'.If the question is about finance and subscriptions, go to 'subscription_agent'. " 
        "If the question was answered use __end__ to end the conversation."
    )
    content: str = Field(
        description="Generate a confirmation message to the user, informing them of the specialist they're being forwarded to. "
        "For example: 'Sure, I'm transferring you to our financial specialist."
    )
    
structered_model = model.with_structured_output(Router)

class Router2(BaseModel):
    next_agent: Literal["decider","subscription_agent", "__end__"] = Field(
        description="""Your decision about the next step. RULES:
        - If you've fully answered the user's question about the product, choose '__end__'.
        - If the user asked a new question about pricing or subscriptions, choose 'subscription_agent'.
        - If you're unsure or the question is ambiguous, return control to the main router by choosing 'decider'.
        """

    )
    content: str = Field(
        description="The answer of the user's question about the product"
    )

structered_model2 = model.with_structured_output(Router2)


class Router3(BaseModel):
    next_agent: Literal["decider", "product_agent", "__end__"] = Field(
        description="""Your decision about the next step. RULES:
        - If you've fully answered the user's question about finances, choose '__end__'.
        - If the user asked a new question about product features, choose 'product_agent'.
        - If you're unsure or the question is ambiguous, return control to the main router by choosing 'decider'.
        """

    )
    content: str = Field(
        description="The answer of the user's question about finances"
    )

structered_model3 = model.with_structured_output(Router3)

def decider(state: AgentState) -> Command[Literal["product_agent", "subscription_agent", END]]:
    
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

def product_agent(state: AgentState) -> Command[Literal["decider", "subscription_agent", END]]:
    
    system_prompt = """
            You are product especialist. Your task is to answer questions about the products of our company and then
            decide what is the next step:
            - If you are highly confident that the user's question has been fully answered, **end the conversation** by choosing '__end__'.
            - If the user has asked a new question that belongs to another expert, forward it directly to them (e.g., 'product_agent' or 'subscription_agent').
            - If you are unsure or the question is ambiguous, return control to the primary router ('decider').
            ---PRODUCT INFORMATION---
            - Notebook: 500$ or 5x100$
            - TV: 200$ or 4x50$
            - Iphone 17:1000$ or 2x500$.
            --------------------------
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

def subscription_agent(state: AgentState) -> Command[Literal["decider", "product_agent", END]]:
    system_prompt = """
        You are finances and subscriptions especialist. Your task is to answer questions about the subscriptions of our sorftware and then
        return the control to the supervisor.
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
builder.add_node(decider)
builder.add_node(product_agent)
builder.add_node(subscription_agent)

builder.set_entry_point("decider")

network = builder.compile()


if __name__ == "__main__":
    initial_state = {
        "messages": [HumanMessage(content="Hi, I want to know the price of the subscription")],
        "next_agent": ""
    }
    for event in network.stream(initial_state):
        print(event)
        print("---")