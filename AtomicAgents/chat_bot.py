import os
import instructor
import openai
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import List 
from pydantic import Field
from atomic_agents.context import ChatHistory, SystemPromptGenerator
from atomic_agents import AtomicAgent, AgentConfig, BasicChatInputSchema, BasicChatOutputSchema,BaseIOSchema
from dotenv import load_dotenv

load_dotenv()

class CustomOutputSchema(BaseIOSchema):
    
    """A clear and concise description of what this schema is for."""
     
    chat_message: str = Field(
        description="The chat message exchanged between the user and the chat agent.",
    )
    suggested_user_questions: List[str] = Field(
        description="A list of suggested follow-up questions the user could ask the agent.",
    )



console = Console()

history = ChatHistory()

initial_message = CustomOutputSchema(
    chat_message="Hello! How can I assist you today?",
    suggested_user_questions=["What can you do?", "Tell me a joke", "Tell me about how you were made"],
)
history.add_message("assistant", initial_message)

client = instructor.from_openai(openai.OpenAI(api_key=os.getenv("GEMINI_API_KEY"),
                                            base_url=os.getenv("GEMINI_BASE_URL")))

system_prompt_generator = SystemPromptGenerator(
    background=[
        "This assistant is a knowledgeable AI designed to be helpful, friendly, and informative.",
        "It has a wide range of knowledge on various topics and can engage in diverse conversations.",
    ],
    steps=[
        "Analyze the user's input to understand the context and intent.",
        "Formulate a relevant and informative response based on the assistant's knowledge.",
        "Generate 3 suggested follow-up questions for the user to explore the topic further.",
        "When you get a simple number from the user, choose the corresponding question from the last list of "
        "suggested questions and answer it. Note that the first question is 1, the second is 2, and so on.",
    ],
    output_instructions=[
        "Provide clear, concise, and accurate information in response to user queries.",
        "Maintain a friendly and professional tone throughout the conversation.",
        "Conclude each response with 3 relevant suggested questions for the user.",
    ],
)

console.print(Panel(system_prompt_generator.generate_prompt(), width=console.width, style="bold cyan"), style="bold cyan")

agent = AtomicAgent[BasicChatInputSchema, CustomOutputSchema](
    config=AgentConfig(
        client=client,
        model="gemini-2.0-flash-exp",  # Using the latest model
        history=history,
        system_prompt_generator= system_prompt_generator,
        model_api_parameters={"max_tokens": 2048}
    )
)

console.print(Text("Agent:", style="bold green"), end=" ")
console.print(Text(initial_message.chat_message, style="bold green"))

console.print("\n[bold cyan]Suggested questions you could ask:[/bold cyan]")
for i, question in enumerate(initial_message.suggested_user_questions, 1):
    console.print(f"[cyan]{i}. {question}[/cyan]")
console.print() 

while True:
    user_input = console.input("[bold blue]You:[/bold blue] ")
    if user_input.lower() in ["/exit", "/quit"]:
        console.print("Exiting chat...")
        break

    input_schema = BasicChatInputSchema(chat_message=user_input)
    response = agent.run(input_schema)

    console.print("Agent: ", response.chat_message)
    
    console.print("\n[bold cyan]Suggested questions you could ask:[/bold cyan]")
    for i, question in enumerate(response.suggested_user_questions, 1):
        console.print(f"[cyan]{i}. {question}[/cyan]")
    console.print() 
