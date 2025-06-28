from crewai import Crew, Process

from agents.medical_agents import doctor, verifier, nutritionist, exercise_specialist
from tasks.medical_tasks import (verification_task, medical_analysis_task, nutrition_analysis_task, exercise_planning_task)

## creating medical analysis crew
medical_crew = Crew(
    agents=[verifier, doctor, nutritionist, exercise_specialist],
    tasks=[verification_task, medical_analysis_task, nutrition_analysis_task, exercise_planning_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=False,
    verbose=2
)

def run_medical_analysis(query: str, file_path: str = 'data/sample.pdf'):
    """
    Run the medical analysis crew with the given query and file path.
    
    Args:
        query (str): User query about their blood test
        file_path (str): Path to the blood test PDF file
        
    Returns:
        dict: Results from the crew execution
    """
    try:
        # Update the file path in the tools if needed
        # This could be improved by making the file path dynamic
        
        result = medical_crew.kickoff(inputs={'query': query})
        return result
    except Exception as e:
        return f"Error running medical analysis: {str(e)}"

def get_crew_usage_metrics():
    """
    Get usage metrics for the crew.
    
    Returns:
        dict: Usage metrics
    """
    try:
        return medical_crew.usage_metrics
    except Exception as e:
        return f"Error getting usage metrics: {str(e)}"
    

if __name__ == "__main__":
    query = "Tell me detail about the report"
    print(run_medical_analysis(query))
