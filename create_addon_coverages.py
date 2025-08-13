# import re
# from typing import Dict, Any, List

# def extract_ambulance_cover_details(text_block: str, policy_sum_insured: float) -> Dict[str, Any]:
#     """
#     Extracts detailed information for a single Ambulance Cover endorsement block.
#     """
#     details = {
#         "Sum Insured": policy_sum_insured,
#         "Number of Trips": 0,  # FINAL CHANGE: Default value is now 0.
#         "% Limit Applicable On": "Sum Insured",
#         "Limit Amount": "",
#         "Applicability": "lower",
#         "Limit Percentage": ""
#     }
    
#     # Logic to find a specific number of trips, if mentioned.
#     trips_match = re.search(r'number of trips[:\s]+(\d+)', text_block, re.IGNORECASE)
#     if trips_match:
#         details["Number of Trips"] = int(trips_match.group(1))

#     # Existing logic for limit amount.
#     limit_match = re.search(r'limit of Rs\.?\s*([\d,]+)', text_block, re.IGNORECASE)
#     if limit_match:
#         limit_amount_str = limit_match.group(1).replace(',', '')
#         limit_amount = float(limit_amount_str)
#         details["Limit Amount"] = limit_amount
#         if policy_sum_insured > 0 and limit_amount > 0:
#             details["Limit Percentage"] = limit_amount / policy_sum_insured
#     return details

# def extract_convalescence_benefit_details(text_block: str, policy_sum_insured: float) -> Dict[str, Any]:
#     """
#     Extracts detailed information for a single Convalescence Benefit endorsement block.
#     """
#     details = {
#         "Sum Insured": policy_sum_insured, "Minimum LOS in days": "", "Applicable From": "", "Benefit Amount": ""
#     }
#     days_match = re.search(r'exceeds\s+(\d+)\s+days', text_block, re.IGNORECASE)
#     if days_match:
#         details["Minimum LOS in days"] = int(days_match.group(1))
#     benefit_match = re.search(r'benefit of Rs\.?\s*([\d,]+)', text_block, re.IGNORECASE)
#     if benefit_match:
#         details["Benefit Amount"] = float(benefit_match.group(1).replace(',', ''))
#     return details

# def create_addon_coverages(text: str, addon_covers_status: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
#     """
#     Main function to orchestrate the extraction. This version ensures the data
#     structure is ALWAYS a list of dictionaries.
#     """
#     DEFAULT_SUM_INSURED = 500000.0
#     coverages_data = {}

#     # Process Ambulance Cover
#     if addon_covers_status.get("Ambulance Cover") == "Yes":
#         endorsement_blocks = re.findall(r'Endt\. No\.\s*16(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
#         ambulance_results = [extract_ambulance_cover_details(block, DEFAULT_SUM_INSURED) for block in endorsement_blocks]
#         coverages_data["Ambulance Cover"] = ambulance_results if ambulance_results else [{}]
#     else:
#         coverages_data["Ambulance Cover"] = [{
#             "Sum Insured": "", "Number of Trips": "", "% Limit Applicable On": "", "Limit Percentage": "", "Limit Amount": "", "Applicability": ""
#         }]

#     # Process Convalescence Benefit
#     if addon_covers_status.get("Convalescence Benefit") == "Yes":
#         endorsement_blocks = re.findall(r'Endt\. No\.\s*15(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
#         convalescence_results = [extract_convalescence_benefit_details(block, DEFAULT_SUM_INSURED) for block in endorsement_blocks]
#         coverages_data["Convalescence Benefit"] = convalescence_results if convalescence_results else [{}]
#     else:
#         coverages_data["Convalescence Benefit"] = [{
#             "Sum Insured": "", "Minimum LOS in days": "", "Applicable From": "", "Benefit Amount": ""
#         }]
        
#     return coverages_data

import re
from typing import Dict, Any, List

def extract_ambulance_cover_details(text_block: str, policy_sum_insured: float) -> Dict[str, Any]:
    """
    Extracts detailed information for a single Ambulance Cover endorsement block.
    """
    details = {
        "Sum Insured": policy_sum_insured, "Number of Trips": 0, "% Limit Applicable On": "Sum Insured",
        "Limit Amount": "", "Applicability": "lower", "Limit Percentage": ""
    }
    trips_match = re.search(r'number of trips[:\s]+(\d+)', text_block, re.IGNORECASE)
    if trips_match:
        details["Number of Trips"] = int(trips_match.group(1))
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

def extract_home_nursing_allowance_details(text_block: str, policy_sum_insured: float) -> Dict[str, Any]:
    """
    FINAL CORRECTED VERSION: Extracts detailed information for Home Nursing Allowance (Endt. 17)
    using the correct logic for "daily allowance" and "maximum days".
    """
    details = {
        "Applicable On?": "",
        "Is Doctor & Nursing Charges Combined ?": "No",
        "% Limit Applicable On": policy_sum_insured,
        "Limit Percentage": "",
        "Limit amount": "",
        "Applicability": "lower",
        "No of days Allowed": ""
    }

    if re.search(r'following discharge', text_block, re.IGNORECASE):
        details["Applicable On?"] = "Post Hospitalization"

    # FIX: Correctly extract the maximum number of days.
    days_match = re.search(r'maximum\s+(\d+)\s+days', text_block, re.IGNORECASE)
    if days_match:
        details["No of days Allowed"] = int(days_match.group(1))

    # FIX: Correctly extract the "daily allowance" as the limit amount.
    limit_match = re.search(r'daily allowance of Rs\.?\s*([\d,]+)', text_block, re.IGNORECASE)
    if limit_match:
        limit_amount_str = limit_match.group(1).replace(',', '')
        limit_amount = float(limit_amount_str)
        details["Limit amount"] = limit_amount
        # Calculate percentage using the extracted limit and the provided sum insured.
        if policy_sum_insured > 0 and limit_amount > 0:
            details["Limit Percentage"] = limit_amount / policy_sum_insured
            
    return details

def create_addon_coverages(text: str, addon_covers_status: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Main function to orchestrate the extraction for all three addon covers.
    """
    DEFAULT_SUM_INSURED = 500000.0
    coverages_data = {}

    # --- Ambulance Cover ---
    if addon_covers_status.get("Ambulance Cover") == "Yes":
        blocks = re.findall(r'Endt\. No\.\s*16(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        results = [extract_ambulance_cover_details(block, DEFAULT_SUM_INSURED) for block in blocks]
        coverages_data["Ambulance Cover"] = results if results else [{}]
    else:
        coverages_data["Ambulance Cover"] = [{"Sum Insured": "", "Number of Trips": "", "% Limit Applicable On": "", "Limit Percentage": "", "Limit Amount": "", "Applicability": ""}]

    # --- Convalescence Benefit ---
    if addon_covers_status.get("Convalescence Benefit") == "Yes":
        blocks = re.findall(r'Endt\. No\.\s*15(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        results = [extract_convalescence_benefit_details(block, DEFAULT_SUM_INSURED) for block in blocks]
        coverages_data["Convalescence Benefit"] = results if results else [{}]
    else:
        coverages_data["Convalescence Benefit"] = [{"Sum Insured": "", "Minimum LOS in days": "", "Applicable From": "", "Benefit Amount": ""}]
        
    # --- Home Nursing Allowance ---
    if addon_covers_status.get("Doctor Nurse Home Visit Cover") == "Yes":
        blocks = re.findall(r'Endt\. No\.\s*17(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        results = [extract_home_nursing_allowance_details(block, DEFAULT_SUM_INSURED) for block in blocks]
        coverages_data["Doctor Nurse Home Visit Cover"] = results if results else [{}]
    else:
        coverages_data["Doctor Nurse Home Visit Cover"] = [{"Applicable On?": "", "Is Doctor & Nursing Charges Combined ?": "", "% Limit Applicable On": "", "Limit Percentage": "", "Limit amount": "", "Applicability": "", "No of days Allowed": ""}]

    return coverages_data




