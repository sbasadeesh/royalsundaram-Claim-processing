import re
from typing import Dict, Any

def extract_ambulance_cover_details(text: str, policy_sum_insured: float) -> Dict[str, Any]:
    """
    Extracts detailed information for Ambulance Cover from a specific text block.
    """
    details = {
        "Sum Insured": policy_sum_insured,
        "Number of Trips": "",
        "% Limit Applicable On": "Sum Insured",
        "Limit Amount": "",
        "Applicability": "lower",
        "Limit Percentage": ""
    }

    # This regex is now searching only within the Endorsement 16 text block.
    limit_match = re.search(r'limit of Rs\.?\s*([\d,]+)', text, re.IGNORECASE)
    
    if limit_match:
        limit_amount_str = limit_match.group(1).replace(',', '')
        limit_amount = float(limit_amount_str)
        details["Limit Amount"] = limit_amount
        if policy_sum_insured > 0 and limit_amount > 0:
            details["Limit Percentage"] = limit_amount / policy_sum_insured
            
    return details

def extract_convalescence_benefit_details(text: str, policy_sum_insured: float) -> Dict[str, Any]:
    """
    Extracts detailed information for Convalescence Benefit from a specific text block.
    """
    details = {
        "Sum Insured": policy_sum_insured,
        "Minimum LOS in days": "",
        "Applicable From": "",
        "Benefit Amount": ""
    }
    days_match = re.search(r'exceeds\s+(\d+)\s+days', text, re.IGNORECASE)
    if days_match:
        details["Minimum LOS in days"] = int(days_match.group(1))

    benefit_match = re.search(r'benefit of Rs\.?\s*([\d,]+)', text, re.IGNORECASE)
    if benefit_match:
        details["Benefit Amount"] = float(benefit_match.group(1).replace(',', ''))
    return details

def create_addon_coverages(text: str, addon_covers_status: Dict[str, str]) -> Dict[str, Any]:
    """
    Main function to orchestrate the extraction. It now isolates the text for each
    endorsement before processing to ensure accuracy.
    """
    DEFAULT_SUM_INSURED = 500000.0 
    coverages_data = {}

    # --- FINAL FIX: Isolate text for each endorsement before extracting values ---

    if addon_covers_status.get("Ambulance Cover") == "Yes":
        # Find the text block for Endorsement 16 and pass only that to the extractor
        match = re.search(r'Endt\. No\.\s*16(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        search_text = match.group(1) if match else ""
        coverages_data["Ambulance Cover"] = extract_ambulance_cover_details(search_text, DEFAULT_SUM_INSURED)
    else:
        # Create empty placeholder if "No"
        coverages_data["Ambulance Cover"] = {
            "Sum Insured": "", "Number of Trips": "", "% Limit Applicable On": "", "Limit Percentage": "", "Limit Amount": "", "Applicability": ""
        }

    if addon_covers_status.get("Convalescence Benefit") == "Yes":
        # Find the text block for Endorsement 15 and pass only that to the extractor
        match = re.search(r'Endt\. No\.\s*15(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        search_text = match.group(1) if match else ""
        coverages_data["Convalescence Benefit"] = extract_convalescence_benefit_details(search_text, DEFAULT_SUM_INSURED)
    else:
        # Create empty placeholder if "No"
        coverages_data["Convalescence Benefit"] = {
            "Sum Insured": "", "Minimum LOS in days": "", "Applicable From": "", "Benefit Amount": ""
        }
        
    return coverages_data







