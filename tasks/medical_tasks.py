## Importing libraries and files
from crewai import Task

from agents.medical_agents import doctor, verifier, nutritionist, exercise_specialist
from tools.medical_tools import blood_test_tool, nutrition_tool, exercise_tool, search_tool

## Creating a task to verify blood test report
verification_task = Task(
    description=(
        "Verify that the uploaded document is a legitimate blood test report. "
        "Extract and validate key information including:\n"
        "- Patient information (if present and relevant)\n"
        "- Test dates and laboratory information\n"
        "- Blood test parameters and their values\n"
        "- Reference ranges for each parameter\n"
        "- Any abnormal values or flags\n"
        "Ensure the document format is consistent with standard laboratory reports."
    ),
    expected_output=(
        "A verification report that includes:\n"
        "- Confirmation that the document is a valid blood test report\n"
        "- Summary of key blood parameters found\n"
        "- List of any abnormal values with their reference ranges\n"
        "- Assessment of report completeness and quality\n"
        "- Any concerns or limitations identified in the report"
    ),
    agent=verifier,
    tools=[blood_test_tool],
    async_execution=False,
)

## Creating a task to analyze blood test results
medical_analysis_task = Task(
    description=(
        "Provide a comprehensive medical analysis of the blood test report to address the user's query: {query}\n"
        "Analyze the blood test parameters and provide:\n"
        "- Clinical interpretation of abnormal values\n"
        "- Potential medical significance of findings\n"
        "- Recommendations for follow-up testing if needed\n"
        "- General health insights based on the results\n"
        "Use evidence-based medical knowledge and current clinical guidelines."
    ),
    expected_output=(
        "A detailed medical analysis report including:\n"
        "- Summary of key findings from the blood test\n"
        "- Clinical interpretation of abnormal or concerning values\n"
        "- Potential health implications and risk factors\n"
        "- Recommendations for further evaluation or monitoring\n"
        "- Important disclaimers about the need for professional medical consultation\n"
        "- References to relevant medical literature or guidelines when appropriate"
    ),
    agent=doctor,
    tools=[blood_test_tool, search_tool],
    async_execution=False,
)

## Creating a nutrition analysis task
nutrition_analysis_task = Task(
    description=(
        "Based on the blood test results, provide evidence-based nutritional recommendations.\n"
        "Analyze relevant nutritional biomarkers and provide:\n"
        "- Assessment of nutritional status based on blood parameters\n"
        "- Specific dietary recommendations to address any deficiencies or imbalances\n"
        "- Food sources rich in needed nutrients\n"
        "- Dietary modifications that may help optimize the identified parameters\n"
        "User query context: {query}"
    ),
    expected_output=(
        "A comprehensive nutrition analysis including:\n"
        "- Assessment of nutritional biomarkers from the blood test\n"
        "- Specific nutrient recommendations based on the results\n"
        "- Detailed dietary suggestions including food sources\n"
        "- Meal planning tips and dietary modifications\n"
        "- Timeline for reassessment and monitoring\n"
        "- Emphasis on working with healthcare providers for personalized nutrition therapy"
    ),
    agent=nutritionist,
    tools=[nutrition_tool, search_tool],
    async_execution=False,
)

## Creating an exercise planning task
exercise_planning_task = Task(
    description=(
        "Develop a safe and effective exercise plan based on the blood test results and overall health status.\n"
        "Consider relevant biomarkers that affect exercise capacity and safety:\n"
        "- Cardiovascular risk factors\n"
        "- Metabolic parameters\n"
        "- Any contraindications to specific types of exercise\n"
        "- Individual fitness level and health goals\n"
        "User query context: {query}"
    ),
    expected_output=(
        "A personalized exercise plan including:\n"
        "- Assessment of exercise readiness based on blood test results\n"
        "- Specific exercise recommendations (type, intensity, duration, frequency)\n"
        "- Safety considerations and contraindications\n"
        "- Progression guidelines and monitoring parameters\n"
        "- Recommendations for medical clearance if needed\n"
        "- Integration with nutritional and medical recommendations"
    ),
    agent=exercise_specialist,
    tools=[exercise_tool, search_tool],
    async_execution=False,
)