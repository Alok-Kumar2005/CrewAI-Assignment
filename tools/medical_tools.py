## Importing libraries and files
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader
from typing import Type
from pydantic import BaseModel, Field
import re


## Serper tool for internet search
search_tool = SerperDevTool(n=3)

## PDF reader tool to read the pdf data
class PDFReaderInput(BaseModel):
    """Input schema for PDF Reader tool."""
    path: str = Field(..., description="Path of the pdf file")

class BloodTestReportTool(BaseTool):
    name: str = "blood_test_reader"
    description: str = "Tool to read and extract the data from the blood test PDF report"
    args_schema: Type[BaseModel] = PDFReaderInput

    def _run(self, path: str = 'data/sample.pdf') -> str:
        """ Tool to read the data from the blood test PDF
        Args:
            path (str): path of the pdf file to read
        Returns:
            str: return the blood report content
        """
        try:
            # check if file exist or not
            if not os.path.exists(path):
                return f"Error: File does not exist at {path}"
            
            # load the pdf using pypdf loader using langchain
            loader = PyPDFLoader(file_path=path)
            docs = loader.load()
            
            ## checking for docs in pdf
            if not docs:
                return "Error: No content found in the PDF file"
            
            full_report = ""
            for page in docs:
                content = page.page_content
                
                # Clean and format the content
                content = content.strip()
                while "\n\n\n" in content:
                    content = content.replace("\n\n\n", "\n\n")
                    
                full_report += content + "\n\n"
            
            return full_report.strip()
            
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

## Creating Nutrition Analysis Tool
class NutritionAnalysisInput(BaseModel):
    """input schema for Nutrition analyst tool"""
    blood_report_data: str = Field(..., description="Blood report data to analyze for nutritional insights")

class NutritionAnalysisTool(BaseTool):
    name: str = "nutrition_analyzer"
    description: str = "Tool to analyze blood report data and provide evidence-based nutritional recommendations"
    args_schema: Type[BaseModel] = NutritionAnalysisInput

    def _extract_test_values(self, blood_report_data: str) -> dict:
        """Extract specific test values from blood report"""
        values = {}
        
        # Extract hemoglobin
        hb_match = re.search(r'Hemoglobin.*?(\d+\.?\d*)\s*g/dL', blood_report_data, re.IGNORECASE)
        if hb_match:
            values['hemoglobin'] = float(hb_match.group(1))
        
        # Extract cholesterol values
        total_chol_match = re.search(r'Cholesterol, Total.*?(\d+\.?\d*)\s*mg/dL', blood_report_data)
        if total_chol_match:
            values['total_cholesterol'] = float(total_chol_match.group(1))
            
        hdl_match = re.search(r'HDL Cholesterol.*?(\d+\.?\d*)\s*mg/dL', blood_report_data)
        if hdl_match:
            values['hdl_cholesterol'] = float(hdl_match.group(1))
            
        ldl_match = re.search(r'LDL Cholesterol.*?(\d+\.?\d*)\s*mg/dL', blood_report_data)
        if ldl_match:
            values['ldl_cholesterol'] = float(ldl_match.group(1))
        
        # Extract triglycerides
        trig_match = re.search(r'Triglycerides.*?(\d+\.?\d*)\s*mg/dL', blood_report_data)
        if trig_match:
            values['triglycerides'] = float(trig_match.group(1))
        
        # Extract glucose
        glucose_match = re.search(r'Glucose Fasting.*?(\d+\.?\d*)\s*mg/dL', blood_report_data)
        if glucose_match:
            values['fasting_glucose'] = float(glucose_match.group(1))
        
        # Extract HbA1c
        hba1c_match = re.search(r'HbA1c.*?(\d+\.?\d*)\s*%', blood_report_data)
        if hba1c_match:
            values['hba1c'] = float(hba1c_match.group(1))
        
        # Extract Vitamin B12
        b12_match = re.search(r'VITAMIN B12.*?(\d+\.?\d*)\s*pg/mL', blood_report_data)
        if b12_match:
            values['vitamin_b12'] = float(b12_match.group(1))
        
        # Extract Vitamin D
        vit_d_match = re.search(r'VITAMIN D.*?(\d+\.?\d*)\s*nmol/L', blood_report_data)
        if vit_d_match:
            values['vitamin_d'] = float(vit_d_match.group(1))
        
        # Extract thyroid values
        tsh_match = re.search(r'TSH.*?(\d+\.?\d*)\s*μIU/mL', blood_report_data)
        if tsh_match:
            values['tsh'] = float(tsh_match.group(1))
        
        return values

    def _run(self, blood_report_data: str) -> str:
        """analyze blood report for nutritional insights
        Args:
            blood_report_data (str): Blood report content
        Returns:
            str: Nutrition analysis and recommendations
        """
        try:
            if not blood_report_data:
                return "Error: No blood report data provided for analysis"
            
            values = self._extract_test_values(blood_report_data)
            recommendations = []
            
            # Hemoglobin analysis (Normal: 13.0-17.0 g/dL for males)
            ## since i don't have idea about these recommendations. so, these below function is generated by LLM
            if 'hemoglobin' in values:
                hb = values['hemoglobin']
                if hb < 13.0:
                    recommendations.append("Low hemoglobin detected. Include iron-rich foods: lean red meat, spinach, lentils, and vitamin C-rich foods to enhance iron absorption.")
                elif hb > 17.0:
                    recommendations.append("Elevated hemoglobin. Ensure adequate hydration and consider consulting healthcare provider.")
                else:
                    recommendations.append("Hemoglobin levels are normal. Maintain balanced iron intake through lean meats, legumes, and leafy greens.")
            
            # Cholesterol analysis
            if 'total_cholesterol' in values:
                total_chol = values['total_cholesterol']
                if total_chol >= 200:
                    recommendations.append("Elevated total cholesterol. Increase soluble fiber intake (oats, beans, apples), omega-3 fatty acids (fatty fish, walnuts), and limit saturated fats.")
                else:
                    recommendations.append("Total cholesterol is within healthy range. Continue heart-healthy diet with fruits, vegetables, and whole grains.")
            
            if 'hdl_cholesterol' in values:
                hdl = values['hdl_cholesterol']
                if hdl < 40:
                    recommendations.append("Low HDL cholesterol. Increase physical activity, include healthy fats (olive oil, avocados), and omega-3 rich foods.")
                else:
                    recommendations.append("HDL cholesterol is adequate. Maintain current healthy fat intake and regular exercise.")
            
            if 'ldl_cholesterol' in values:
                ldl = values['ldl_cholesterol']
                if ldl >= 100:
                    recommendations.append("LDL cholesterol is elevated. Focus on plant-based foods, reduce saturated fat, and increase soluble fiber.")
                else:
                    recommendations.append("LDL cholesterol is optimal. Continue current dietary patterns.")
            
            # Triglycerides analysis
            if 'triglycerides' in values:
                trig = values['triglycerides']
                if trig >= 150:
                    recommendations.append("Elevated triglycerides. Reduce refined carbohydrates, limit alcohol, increase omega-3 intake, and maintain healthy weight.")
                else:
                    recommendations.append("Triglyceride levels are normal. Continue balanced carbohydrate intake and healthy fats.")
            
            # Glucose analysis
            if 'fasting_glucose' in values:
                glucose = values['fasting_glucose']
                if glucose >= 100:
                    recommendations.append("Elevated fasting glucose. Focus on complex carbohydrates, increase fiber intake, limit simple sugars, and maintain portion control.")
                else:
                    recommendations.append("Fasting glucose is normal. Continue balanced carbohydrate intake with whole grains and vegetables.")
            
            # HbA1c analysis
            if 'hba1c' in values:
                hba1c = values['hba1c']
                if hba1c >= 5.7:
                    recommendations.append("HbA1c indicates prediabetes risk. Focus on low glycemic index foods, regular meal timing, and weight management.")
                else:
                    recommendations.append("HbA1c is normal, indicating good glucose control over past 2-3 months.")
            
            # Vitamin B12 analysis
            if 'vitamin_b12' in values:
                b12 = values['vitamin_b12']
                if b12 < 300:
                    recommendations.append("Vitamin B12 is on the lower side. Include B12-rich foods: fish, meat, dairy, or consider supplementation if vegetarian.")
                else:
                    recommendations.append("Vitamin B12 levels are adequate. Continue current intake of animal products or fortified foods.")
            
            # Vitamin D analysis
            if 'vitamin_d' in values:
                vit_d = values['vitamin_d']
                if vit_d < 75:
                    recommendations.append("Vitamin D deficiency detected. Increase sun exposure, include fatty fish, fortified dairy, and consider supplementation.")
                else:
                    recommendations.append("Vitamin D levels are sufficient. Continue current sun exposure and dietary sources.")
            
            # Thyroid analysis
            if 'tsh' in values:
                tsh = values['tsh']
                if tsh > 4.78:
                    recommendations.append("Elevated TSH may indicate thyroid dysfunction. Ensure adequate iodine intake through iodized salt and seafood.")
                elif tsh < 0.55:
                    recommendations.append("Low TSH detected. Monitor thyroid function and avoid excessive iodine intake.")
                else:
                    recommendations.append("TSH levels are normal, indicating healthy thyroid function.")
            
            if not recommendations:
                recommendations.append("All measured parameters appear normal. Maintain a balanced diet with variety of nutrients.")
            
            # Add general recommendations
            recommendations.append("\nGeneral Recommendations:")
            recommendations.append("• Stay hydrated with 8-10 glasses of water daily")
            recommendations.append("• Include 5 servings of fruits and vegetables daily")
            recommendations.append("• Choose whole grains over refined grains")
            recommendations.append("• Limit processed foods and added sugars")
            recommendations.append("• Include lean proteins in each meal")
            
            return "NUTRITIONAL ANALYSIS BASED ON BLOOD REPORT:\n\n" + "\n\n".join(recommendations)
            
        except Exception as e:
            return f"Error in nutrition analysis: {str(e)}"

## Creating Exercise Planning Tool
class ExercisePlanningInput(BaseModel):
    """inout schema for exercise plainning tool."""
    blood_report_data: str = Field(..., description="blood report data to analyze and recomment exercise")

class ExercisePlanningTool(BaseTool):
    name: str = "exercise_planner"
    description: str = "tool to create the exercise planning on the basis of the report data"
    args_schema: Type[BaseModel] = ExercisePlanningInput

    def _extract_test_values(self, blood_report_data: str) -> dict:
        """Extract test values from the report to recommend exercise"""
        values = {}
        
        # Extract key values for exercise planning
        hb_match = re.search(r'Hemoglobin.*?(\d+\.?\d*)\s*g/dL', blood_report_data, re.IGNORECASE)
        if hb_match:
            values['hemoglobin'] = float(hb_match.group(1))
        
        glucose_match = re.search(r'Glucose Fasting.*?(\d+\.?\d*)\s*mg/dL', blood_report_data)
        if glucose_match:
            values['fasting_glucose'] = float(glucose_match.group(1))
        
        hba1c_match = re.search(r'HbA1c.*?(\d+\.?\d*)\s*%', blood_report_data)
        if hba1c_match:
            values['hba1c'] = float(hba1c_match.group(1))
        
        total_chol_match = re.search(r'Cholesterol, Total.*?(\d+\.?\d*)\s*mg/dL', blood_report_data)
        if total_chol_match:
            values['total_cholesterol'] = float(total_chol_match.group(1))
        
        trig_match = re.search(r'Triglycerides.*?(\d+\.?\d*)\s*mg/dL', blood_report_data)
        if trig_match:
            values['triglycerides'] = float(trig_match.group(1))
        
        tsh_match = re.search(r'TSH.*?(\d+\.?\d*)\s*μIU/mL', blood_report_data)
        if tsh_match:
            values['tsh'] = float(tsh_match.group(1))
        
        return values

    def _run(self, blood_report_data: str) -> str:
        """Create exercise plan based on blood report
        
        Args:
            blood_report_data (str): Blood report content
            
        Returns:
            str: Exercise recommendations
        """
        try:
            if not blood_report_data:
                return "Error: No blood report data provided for exercise planning"
            
            values = self._extract_test_values(blood_report_data)
            recommendations = []
            
            # Base exercise recommendations for 30-year-old male
            recommendations.append("PERSONALIZED EXERCISE PLAN BASED ON BLOOD REPORT:")
            recommendations.append("\nBased on your blood test results, here are tailored exercise recommendations:")
            
            # Cardiovascular health recommendations
            if 'total_cholesterol' in values or 'triglycerides' in values:
                total_chol = values.get('total_cholesterol', 0)
                triglycerides = values.get('triglycerides', 0)
                
                if total_chol >= 200 or triglycerides >= 150:
                    recommendations.append("\n• CARDIOVASCULAR FOCUS (Elevated Cholesterol/Triglycerides):")
                    recommendations.append("  - Moderate-intensity cardio: 150 minutes/week (brisk walking, cycling)")
                    recommendations.append("  - High-intensity interval training (HIIT): 2-3 sessions/week, 20-30 minutes")
                    recommendations.append("  - Swimming or elliptical: 3-4 times/week, 30-45 minutes")
                else:
                    recommendations.append("\n• CARDIOVASCULAR MAINTENANCE:")
                    recommendations.append("  - Regular cardio: 120-150 minutes/week (running, cycling, swimming)")
                    recommendations.append("  - Mix of moderate and vigorous intensity exercises")
            
            # Glucose management recommendations
            if 'fasting_glucose' in values or 'hba1c' in values:
                glucose = values.get('fasting_glucose', 0)
                hba1c = values.get('hba1c', 0)
                
                if glucose >= 100 or hba1c >= 5.7:
                    recommendations.append("\n• GLUCOSE MANAGEMENT (Elevated Blood Sugar):")
                    recommendations.append("  - Post-meal walks: 10-15 minutes after each meal")
                    recommendations.append("  - Resistance training: 3 times/week, focusing on major muscle groups")
                    recommendations.append("  - Avoid prolonged sitting; take movement breaks every hour")
                    recommendations.append("  - Monitor blood sugar before and after exercise initially")
                else:
                    recommendations.append("\n• METABOLIC HEALTH MAINTENANCE:")
                    recommendations.append("  - Regular strength training: 2-3 times/week")
                    recommendations.append("  - Compound exercises: squats, deadlifts, push-ups")
            
            # Energy and endurance recommendations based on hemoglobin
            if 'hemoglobin' in values:
                hb = values['hemoglobin']
                if hb < 13.0:
                    recommendations.append("\n• ENERGY MANAGEMENT (Lower Hemoglobin):")
                    recommendations.append("  - Start with low-intensity exercises")
                    recommendations.append("  - Gradually increase intensity as iron levels improve")
                    recommendations.append("  - Focus on breathing exercises and yoga")
                    recommendations.append("  - Avoid overexertion; listen to your body")
                else:
                    recommendations.append("\n• PERFORMANCE OPTIMIZATION:")
                    recommendations.append("  - High-intensity workouts are well-tolerated")
                    recommendations.append("  - Include both aerobic and anaerobic training")
            
            # Thyroid-related exercise modifications
            if 'tsh' in values:
                tsh = values['tsh']
                if tsh > 4.78:
                    recommendations.append("\n• THYROID CONSIDERATIONS (Elevated TSH):")
                    recommendations.append("  - Start slowly and build exercise tolerance gradually")
                    recommendations.append("  - Focus on consistent, moderate-intensity exercise")
                    recommendations.append("  - Include stress-reducing activities like yoga or tai chi")
                elif tsh < 0.55:
                    recommendations.append("\n• THYROID CONSIDERATIONS (Low TSH):")
                    recommendations.append("  - Monitor heart rate during exercise")
                    recommendations.append("  - Avoid excessive high-intensity training")
                    recommendations.append("  - Include calming exercises like stretching or meditation")
            
            # Weekly exercise schedule
            recommendations.append("\n• SUGGESTED WEEKLY SCHEDULE:")
            recommendations.append("  Monday: Full-body strength training (45-60 minutes)")
            recommendations.append("  Tuesday: Cardio workout (30-45 minutes)")
            recommendations.append("  Wednesday: Yoga or flexibility training (30-45 minutes)")
            recommendations.append("  Thursday: Upper body strength + core (45-60 minutes)")
            recommendations.append("  Friday: HIIT or circuit training (30-40 minutes)")
            recommendations.append("  Saturday: Outdoor activity (hiking, sports, cycling)")
            recommendations.append("  Sunday: Active recovery (light walk, stretching)")
            
            # Important safety notes
            recommendations.append("\n• IMPORTANT SAFETY NOTES:")
            recommendations.append("  - Warm up for 5-10 minutes before exercising")
            recommendations.append("  - Cool down and stretch after workouts")
            recommendations.append("  - Stay hydrated throughout exercise")
            recommendations.append("  - Progress gradually; avoid sudden intensity increases")
            recommendations.append("  - Consult healthcare provider before starting intense exercise program")
            
            # Monitoring recommendations
            recommendations.append("\n• MONITORING & FOLLOW-UP:")
            recommendations.append("  - Track energy levels and exercise tolerance")
            recommendations.append("  - Retest blood parameters in 3-6 months")
            recommendations.append("  - Adjust exercise intensity based on how you feel")
            recommendations.append("  - Keep a workout log to track progress")
            
            return "\n".join(recommendations)
            
        except Exception as e:
            return f"Error in exercise planning: {str(e)}"

# Create instances of tools
blood_test_tool = BloodTestReportTool()
nutrition_tool = NutritionAnalysisTool()
exercise_tool = ExercisePlanningTool()