import re

def extract_blood_values(report_content: str) -> dict:
    """Extract blood test values from report content"""
    values = {}
    
    # Extract hemoglobin
    hb_match = re.search(r'Hemoglobin.*?(\d+\.?\d*)\s*g/dL', report_content, re.IGNORECASE)
    if hb_match:
        values['hemoglobin'] = float(hb_match.group(1))
    
    # Extract cholesterol values
    total_chol_match = re.search(r'Cholesterol, Total.*?(\d+\.?\d*)\s*mg/dL', report_content)
    if total_chol_match:
        values['total_cholesterol'] = float(total_chol_match.group(1))
        
    hdl_match = re.search(r'HDL Cholesterol.*?(\d+\.?\d*)\s*mg/dL', report_content)
    if hdl_match:
        values['hdl_cholesterol'] = float(hdl_match.group(1))
        
    ldl_match = re.search(r'LDL Cholesterol.*?(\d+\.?\d*)\s*mg/dL', report_content)
    if ldl_match:
        values['ldl_cholesterol'] = float(ldl_match.group(1))
    
    # Extract triglycerides
    trig_match = re.search(r'Triglycerides.*?(\d+\.?\d*)\s*mg/dL', report_content)
    if trig_match:
        values['triglycerides'] = float(trig_match.group(1))
    
    # Extract glucose
    glucose_match = re.search(r'Glucose Fasting.*?(\d+\.?\d*)\s*mg/dL', report_content)
    if glucose_match:
        values['fasting_glucose'] = float(glucose_match.group(1))
    
    # Extract HbA1c
    hba1c_match = re.search(r'HbA1c.*?(\d+\.?\d*)\s*%', report_content)
    if hba1c_match:
        values['hba1c'] = float(hba1c_match.group(1))
    
    # Extract Vitamin B12
    b12_match = re.search(r'VITAMIN B12.*?(\d+\.?\d*)\s*pg/mL', report_content)
    if b12_match:
        values['vitamin_b12'] = float(b12_match.group(1))
    
    # Extract Vitamin D
    vit_d_match = re.search(r'VITAMIN D.*?(\d+\.?\d*)\s*nmol/L', report_content)
    if vit_d_match:
        values['vitamin_d'] = float(vit_d_match.group(1))
    
    # Extract thyroid values
    tsh_match = re.search(r'TSH.*?(\d+\.?\d*)\s*μIU/mL', report_content)
    if tsh_match:
        values['tsh'] = float(tsh_match.group(1))
    
    return values