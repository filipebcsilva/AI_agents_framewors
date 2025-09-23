from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from reporter.tools.custom_tool import SearchTool
from crewai import LLM
from dotenv import load_dotenv
import os
from typing import List


load_dotenv()

llm = LLM(
    model= 'gemini/gemini-2.5-flash',
    api_key=os.getenv("GEMINI_API_KEY")
)
print("gemini/" + os.getenv("MODEL"),)
@CrewBase
class Reporter():
    """Reporter crew"""
    
    agents: List[BaseAgent]
    tasks: List[Task]
   
    ##AGENTES##
    @agent
    def web_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['web_researcher_agent'], 
            verbose=True,
            llm = llm,
            tools = [SearchTool]
        )

    @agent
    def trend_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_analyst_agent'],
            llm = llm,
            verbose=True
        )
        
    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer_agent'],
            llm = llm,
            verbose=True
        )
        
           
    @agent
    def proofreader(self) -> Agent:
        return Agent(
            config=self.agents_config['proofreader_agent'],
            llm = llm,
            verbose=True
        )
        
    
    @agent
    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config['manager_agent'], 
            llm = llm,
            verbose=True
        )
        
    ##TASKS##
    @task
    def web_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['web_researcher_task'],
        )

    @task
    def trend_analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config['trend_analyst_task'], 
        )

    @task
    def report_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_writer_task'], 
        )
    
    
    @task
    def proofreader_task(self) -> Task:
        return Task(
            config=self.tasks_config['proofreader_task'], 
        )
    
    ##CREW##
    
    @crew
    def crew(self) -> Crew:
        
        return Crew(
            agents=self.agents[0:4],
            tasks=self.tasks, 
            manager_agent = self.agents[4],
            verbose=True,
            process=Process.hierarchical
        )
