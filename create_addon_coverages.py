import re
from typing import Dict, Any, List

def extract_ambulance_cover_details(text_block: str, policy_sum_insured: float) -> Dict[str, Any]:
    """
    Extracts detailed information for a single Ambulance Cover endorsement block.
    """
    details = {
        "Sum Insured": policy_sum_insured, "Number of Trips": "", "% Limit Applicable On": "Sum Insured",
        "Limit Amount": "", "Applicability": "lower", "Limit Percentage": ""
    }
    limit_match = re.search(r'limit of Rs\.?\s*([\d,]+)', text_block, re.IGNORECASE)
    if limit_match:
        limit_amount_str = limit_match.group(1).replace(',', '')
        limit_amount = float(limit_amount_str)
        details["Limit Amount"] = limit_amount
        if policy_sum_insured > 0 and limit_amount > 0:
            details["Limit Percentage"] = limit_amount / policy_sum_insured
    return details

def extract_convalescence_benefit_details(text_block: str, policy_sum_insured: float) -> Dict[str, Any]:
    """
    Extracts detailed information for a single Convalescence Benefit endorsement block.
    """
    details = {
        "Sum Insured": policy_sum_insured, "Minimum LOS in days": "", "Applicable From": "", "Benefit Amount": ""
    }
    days_match = re.search(r'exceeds\s+(\d+)\s+days', text_block, re.IGNORECASE)
    if days_match:
        details["Minimum LOS in days"] = int(days_match.group(1))
    benefit_match = re.search(r'benefit of Rs\.?\s*([\d,]+)', text_block, re.IGNORECASE)
    if benefit_match:
        details["Benefit Amount"] = float(benefit_match.group(1).replace(',', ''))
    return details

def create_addon_coverages(text: str, addon_covers_status: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Main function to orchestrate the extraction. This version ensures the data
    structure is ALWAYS a list of dictionaries, fixing the root cause of the error.
    """
    DEFAULT_SUM_INSURED = 500000.0
    coverages_data = {}

    # --- FINAL FIX: This logic now ensures a consistent return type for all cases ---

    # Process Ambulance Cover
    if addon_covers_status.get("Ambulance Cover") == "Yes":
        endorsement_blocks = re.findall(r'Endt\. No\.\s*16(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        ambulance_results = [extract_ambulance_cover_details(block, DEFAULT_SUM_INSURED) for block in endorsement_blocks]
        # If no results are found, return a list with one empty dict to maintain the data structure
        coverages_data["Ambulance Cover"] = ambulance_results if ambulance_results else [{}]
    else:
        # If "No", return a LIST containing ONE empty dictionary for the template
        coverages_data["Ambulance Cover"] = [{
            "Sum Insured": "", "Number of Trips": "", "% Limit Applicable On": "", "Limit Percentage": "", "Limit Amount": "", "Applicability": ""
        }]

    # Process Convalescence Benefit
    if addon_covers_status.get("Convalescence Benefit") == "Yes":
        endorsement_blocks = re.findall(r'Endt\. No\.\s*15(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        convalescence_results = [extract_convalescence_benefit_details(block, DEFAULT_SUM_INSURED) for block in endorsement_blocks]
        # If no results are found, return a list with one empty dict
        coverages_data["Convalescence Benefit"] = convalescence_results if convalescence_results else [{}]
    else:
        # If "No", return a LIST containing ONE empty dictionary for the template
        coverages_data["Convalescence Benefit"] = [{
            "Sum Insured": "", "Minimum LOS in days": "", "Applicable From": "", "Benefit Amount": ""
        }]
        
    return coverages_data
