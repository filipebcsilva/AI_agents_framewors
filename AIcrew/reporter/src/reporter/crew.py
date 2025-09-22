from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from reporter.tools.custom_tool import SearchTool
from crewai import LLM
from dotenv import load_dotenv
import os
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

load_dotenv()

llm = LLM(
    model='gemini/gemini-2.5-flash',
    api_key="AIzaSyDv_8QbuzZuPn_sXhrKW-4o5LAn0tJxltU"
)

@CrewBase
class Reporter():
    """Reporter crew"""
    
    agents: List[BaseAgent]
    tasks: List[Task]
   
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    
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
        """Creates the Reporter crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents[0:4], # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            manager_agent = self.agents[4],
            verbose=True,
            process=Process.hierarchical # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
