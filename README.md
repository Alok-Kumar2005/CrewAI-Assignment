# CrewAI-Assignment

## Getting Started

### Create Environment
```
uv venv
```
- python version: 3.12.10
### Activate the environment
```
.venv\Scripts\activate
```

### Install Required Libraries
```
uv add -r requirements.txt
```

### run the server
```
python main.py
```

# Key Changes
### Tools
- Getting Serper tool and BaseTool from the correct package
- Created a Input schema for each tool ( BaseTool required the schema in pydantic structured format)
- Using correct PyPDF module to load and import the data
- Adding extraction data to extract the important data from the output of the Agent to import in database
- Some other changes to extract data correctly
- In NutritionAnalysisTool, created a custom function to get the values from the data and according to that suggest nutitious meal ( i don't have knowledge about the correct value so i took help of LLM to create a custom value for me)
- In ExercisePlanningTool, on the basis of extracted data try to suggest the best exercies. ( since i don't have knowledge about these so i took the help of LLM for that)

### Agents
- Improve the correct way to integrate the LLM from crewai library with gemini model
- some changes in role, goal and backstory of Agents
- since these is small file and most of the things are correct. so i need not to chage more in these 
- Just change some values of Agents

### Task
- changes the desciption and output schema as per my code
- addes medical_analysis_task inplace of ```help_patient``` 
- In these also no major changes, just normal correct agent and tools are replaced 

### Crew
- created a crew for all the Task and Agent 

### Database
- Created a multiple table in the database like 
    1. `User` for storing User info
    2. `BloodTestReport` to store the important data in the report
    3. `AnalysisResult` to store the user question and response
- Created some function to apply `CRUD` operation on the database

### Main.py
- Since i created a new database schema so as per the the that i have to make changes in the api endpoints
- created some of the enpoints like `create_user` to create a user 
- `get_user_by_email` to get the user info using email
- `analyze_report_endpoint` to use crewai and store the important data in database from the result of crew
- `get_report_analyses_endpoint` to add the user query and response