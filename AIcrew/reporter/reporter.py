from crewai import Crew,Process
import os
from agents import web_researcher_agent,trend_analyst_agent,proofreader_agent,report_writer_agent,manager_agent
from tasks import web_research_task,trend_analysis_task,proofreading_task,report_writing_task


crew = Crew(
    agents=[web_researcher_agent, trend_analyst_agent, report_writer_agent, proofreader_agent],
    tasks=[web_research_task, trend_analysis_task, report_writing_task, proofreading_task],
    process=Process.hierarchical,
    manager_agent=manager_agent,
    verbose=True
)

crew_output = crew.kickoff(inputs={"topic": "AI Trends"})