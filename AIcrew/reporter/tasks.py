from crewai import Task


web_research_task = Task(
    description=(
        "Conduct web-based research to identify 5-7 of the {topic}. Focus on key use cases. "
    ),
    expected_output=(
        "A structured list of 5-7 {topic}."
    )
)
trend_analysis_task = Task(
    description=(
        "Analyze the research findings to rank {topic}. "
    ),
    expected_output=(
        "A table ranking trends by impact, with concise descriptions of each trend."
    )
)
 
report_writing_task = Task(
    description=(
        "Draft report summarizing the findings and analysis of {topic}. Include sections for "
        "Introduction, Trends Overview, Analysis, and Recommendations."
    ),
    expected_output=(
        "A structured, professional draft with a clear flow of information. Ensure logical organization and consistent tone."
    )
)
 
proofreading_task = Task(
    description=(
        "Refine the draft for grammatical accuracy, coherence, and formatting. Ensure the final document is polished "
        "and ready for publication."
    ),
    expected_output=(
        "A professional, polished report free of grammatical errors and inconsistencies. Format the document for "
        "easy readability."
    )
)
