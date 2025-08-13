import re
from typing import List, Dict

def create_addon(text: str) -> List[Dict[str, str]]:
    """
    Analyzes the PDF text to determine the status (Yes/No) of various addon covers.
    """
    # List of all possible addon covers to check
    all_covers = [
        "Ambulance Cover", "Convalescence Benefit", "Critical Illness Benefit",
        "Daily/Hospital Cash Benefit", "Anyone Illness", "Attendant Care", "Cancer Cover", 
        "Dental Cover", "Diabetic Cover", "Doctor Nurse Home Visit Cover", "Education Fund", 
        "Funeral", "Getwell Benefit", "Hardship Critical Illness Cover", "Health Check up", 
        "Hypertension Cover", "Intensive Care Benefit", "Loss Of Pay Cover", 
        "Medical Evacuation Cover", "Medical Second Opinion", "Non Medical Expense Cover", 
        "Out Patient Cover", "Optical Cover", "Organ Donor Medical Expense Cover", 
        "Personal Accident Cover", "Pre Existing Disease Benefit", "Psychiatric Cover", 
        "Recovery Benefit", "Referral Hospital Care", "Surgical Benefit", "Top Up Cover", 
        "Vaccination/Immunization Cover"
    ]

    # Initialize all covers to "No" by default
    status = {cover: "No" for cover in all_covers}

    # --- Precise "Yes" Logic for each endorsement ---

    if re.search(r'Endt\. No\.\s*16', text, re.IGNORECASE):
        status["Ambulance Cover"] = "Yes"

    if re.search(r'Endt\. No\.\s*15', text, re.IGNORECASE):
        status["Convalescence Benefit"] = "Yes"
        
    # NEW: Logic to detect Home Nursing Allowance
    if re.search(r'Endt\. No\.\s*17', text, re.IGNORECASE):
        status["Doctor Nurse Home Visit Cover"] = "Yes"

    return [status]
