
import re
from typing import Dict, Any, List

def extract_ambulance_cover_details(text_block: str, policy_sum_insured: float) -> Dict[str, Any]:
    """
    Extracts detailed information for a single Ambulance Cover endorsement block.
    """
    details = {
        "Sum Insured": policy_sum_insured,
        "Number of Trips": 0,  # FINAL CHANGE: Default value is now 0.
        "% Limit Applicable On": "Sum Insured",
        "Limit Amount": "",
        "Applicability": "lower",
        "Limit Percentage": ""
    }
    
    # Logic to find a specific number of trips, if mentioned.
    trips_match = re.search(r'number of trips[:\s]+(\d+)', text_block, re.IGNORECASE)
    if trips_match:
        details["Number of Trips"] = int(trips_match.group(1))

    # Existing logic for limit amount.
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

def extract_critical_illness_field_identifiers(text_block: str) -> Dict[str, Any]:
    """
    Extracts individual field identifiers for Critical Illness from endorsement number 20.
    Checks for specific fields: "Over And Above Policy Sum Insured?", "Survival Period Applicable?", and "Applicable Limit".
    """
    field_identifiers = {
        "Over And Above Policy Sum Insured?": "No",
        "Survival Period Applicable?": "No", 
        "Applicable Limit": "",
        "Sum Insured Per Person": "",
        "Maximum Limit": "",
        "Survival Period": "",
        "Maximum Limit Percentage": ""  # New field for calculation: Maximum Limit/500000*100
    }
    
    # Check if it's over and above policy sum insured
    over_above_patterns = [
        r'over and above.*?sum insured',
        r'over and above.*?individual sum insured',
        r'over and above.*?policy sum insured',
        r'over and above.*?individual',
        r'over and above.*?insured'
    ]
    
    for pattern in over_above_patterns:
        if re.search(pattern, text_block, re.IGNORECASE | re.DOTALL):
            field_identifiers["Over And Above Policy Sum Insured?"] = "Yes"
            break
    
    # Extract sum insured per person
    sum_insured_match = re.search(r'sum insured of Rs\.?\s*([\d,]+)', text_block, re.IGNORECASE)
    if sum_insured_match:
        field_identifiers["Sum Insured Per Person"] = float(sum_insured_match.group(1).replace(',', ''))
    
    # Extract maximum limit
    max_limit_match = re.search(r'maximum limit of Rs\.?\s*([\d,]+)', text_block, re.IGNORECASE)
    if max_limit_match:
        max_limit_value = float(max_limit_match.group(1).replace(',', ''))
        field_identifiers["Maximum Limit"] = max_limit_value
        field_identifiers["Applicable Limit"] = f"Rs. {max_limit_match.group(1)}"
        
        # Calculate Maximum Limit Percentage: Maximum Limit/500000*100
        DEFAULT_SUM_INSURED = 500000.0
        if max_limit_value > 0 and DEFAULT_SUM_INSURED > 0:
            percentage = (max_limit_value / DEFAULT_SUM_INSURED) * 100
            field_identifiers["Maximum Limit Percentage"] = round(percentage, 2)
        else:
            field_identifiers["Maximum Limit Percentage"] = 0.0
    
    # Check for survival period
    survival_patterns = [
        r'survival period',
        r'waiting period',
        r'minimum survival'
    ]
    
    for pattern in survival_patterns:
        if re.search(pattern, text_block, re.IGNORECASE):
            field_identifiers["Survival Period Applicable?"] = "Yes"
            # Try to extract specific survival period duration
            survival_duration_match = re.search(r'(\d+)\s*(?:days?|months?|years?)\s*(?:survival|waiting)', text_block, re.IGNORECASE)
            if survival_duration_match:
                field_identifiers["Survival Period"] = survival_duration_match.group(1)
            break
    
    return field_identifiers

def extract_daily_cash_cover_details(text_block: str) -> Dict[str, Any]:
    """
    Extracts detailed information for Daily Cash Cover from endorsement number 14.
    """
    field_identifiers = {
        "DailyCash_Over_And_Above_Policy_Sum_Insured": "No",
        "DailyCash_Max_Days_Per_Policy_year": "",
        "DailyCash_Max_Days_Per_Illness": "",
        "DailyCash_Fixed_limit": "No",
        "DailyCash_Sum_Insured": "",
        "DailyCash_Threshold": "",
        "DailyCash_Limit_Amount": "",
        "DailyCash_Daily_Cash_Amount": "",
        "DailyCash_Daily_cash_percentage": "",  # New field for percentage calculation
        "DailyCash_Minimum_Hospitalization_Days": "",
        "DailyCash_Minimum_LOS_in_days": "",  # New field for Minimum LOS in days
        "DailyCash_Maximum_Days_Per_Person": "",
        "DailyCash_Waiting_Period_Days": "",
        "DailyCash_Maternity_Exclusion": "No",
        "DailyCash_First_Days_Exclusion": "",
        "DailyCash_Open_range": "No",  # New field for Open range (yes/no)
        "DailyCash_Daily_Limit_Range_From": "",  # New field for Daily Limit Range From
        "DailyCash_Daily_Limit_Range_To": ""  # New field for Daily Limit Range To
    }
    
    # Check if it's over and above policy sum insured
    over_above_patterns = [
        r'over and above.*?sum insured',
        r'over and above.*?individual sum insured',
        r'over and above.*?policy sum insured'
    ]
    
    for pattern in over_above_patterns:
        if re.search(pattern, text_block, re.IGNORECASE):
            field_identifiers["DailyCash_Over_And_Above_Policy_Sum_Insured"] = "Yes"
            break
    
    # Extract Max Days Per Policy year
    max_days_policy_match = re.search(r'maximum days of\s*(\d+)\s*per.*?policy', text_block, re.IGNORECASE)
    if max_days_policy_match:
        field_identifiers["DailyCash_Max_Days_Per_Policy_year"] = int(max_days_policy_match.group(1))
    
    # Extract Max Days Per Illness
    max_days_illness_match = re.search(r'maximum days of\s*(\d+)\s*per.*?event', text_block, re.IGNORECASE)
    if max_days_illness_match:
        field_identifiers["DailyCash_Max_Days_Per_Illness"] = int(max_days_illness_match.group(1))
    
    # Check for Fixed limit - detect when amount is fixed/definite vs variable/range
    fixed_limit_patterns = [
        r'fixed limit',
        r'fixed amount',
        r'lump sum',
        r'definite amount',
        r'specific amount',
        r'exact amount',
        r'predefined amount'
    ]
    
    # Check if any fixed limit patterns match
    for pattern in fixed_limit_patterns:
        if re.search(pattern, text_block, re.IGNORECASE):
            field_identifiers["DailyCash_Fixed_limit"] = "Yes"
            break
    
    # If amount range is detected, it's NOT fixed
    if field_identifiers["DailyCash_Open_range"] == "Yes":
        field_identifiers["DailyCash_Fixed_limit"] = "No"
    
    # Extract Sum Insured (if mentioned)
    sum_insured_match = re.search(r'sum insured.*?Rs\.?\s*([\d,]+)', text_block, re.IGNORECASE)
    if sum_insured_match:
        field_identifiers["DailyCash_Sum_Insured"] = float(sum_insured_match.group(1).replace(',', ''))
    
    # Extract Threshold (minimum days requirement)
    threshold_match = re.search(r'more than\s*(\d+)\s*days', text_block, re.IGNORECASE)
    if threshold_match:
        field_identifiers["DailyCash_Threshold"] = int(threshold_match.group(1))
    
    # Extract Limit Amount (daily cash amount) - handle both "per day" and "from X to Y days" formats
    daily_amount_match = re.search(r'Rs\.?\s*([\d,]+)\s*per day', text_block, re.IGNORECASE)
    if daily_amount_match:
        daily_amount = float(daily_amount_match.group(1).replace(',', ''))
        field_identifiers["DailyCash_Daily_Cash_Amount"] = daily_amount
        field_identifiers["DailyCash_Limit_Amount"] = daily_amount
        
        # Calculate Daily Cash Percentage: Daily Cash Amount/500000*100
        DEFAULT_SUM_INSURED = 500000.0
        if daily_amount > 0 and DEFAULT_SUM_INSURED > 0:
            percentage = (daily_amount / DEFAULT_SUM_INSURED) * 100
            field_identifiers["DailyCash_Daily_cash_percentage"] = round(percentage, 2)
        else:
            field_identifiers["DailyCash_Daily_cash_percentage"] = 0.0
    
    # Handle "from X to Y days" format for Limit Amount
    from_to_days_match = re.search(r'Rs\.?\s*([\d,]+)\s*from\s*\d+\s*to\s*\d+\s*days', text_block, re.IGNORECASE)
    if from_to_days_match:
        daily_amount = float(from_to_days_match.group(1).replace(',', ''))
        field_identifiers["DailyCash_Daily_Cash_Amount"] = daily_amount
        field_identifiers["DailyCash_Limit_Amount"] = daily_amount
        
        # Calculate Daily Cash Percentage: Daily Cash Amount/500000*100
        DEFAULT_SUM_INSURED = 500000.0
        if daily_amount > 0 and DEFAULT_SUM_INSURED > 0:
            percentage = (daily_amount / DEFAULT_SUM_INSURED) * 100
            field_identifiers["DailyCash_Daily_cash_percentage"] = round(percentage, 2)
        else:
            field_identifiers["DailyCash_Daily_cash_percentage"] = 0.0
    
    # Handle amount range format like "ranging from Rs 1000 - 2000"
    range_match = re.search(r'ranging from\s*rs\.?\s*([\d,]+)\s*-\s*([\d,]+)', text_block, re.IGNORECASE)
    if range_match:
        min_amount = float(range_match.group(1).replace(',', ''))
        max_amount = float(range_match.group(2).replace(',', ''))
        
        # Store the range values
        field_identifiers["DailyCash_Daily_Limit_Range_From"] = min_amount
        field_identifiers["DailyCash_Daily_Limit_Range_To"] = max_amount
        
        # Use the maximum amount as the limit amount
        field_identifiers["DailyCash_Daily_Cash_Amount"] = max_amount
        field_identifiers["DailyCash_Limit_Amount"] = max_amount
        
        # Calculate Daily Cash Percentage: Daily Cash Amount/500000*100
        DEFAULT_SUM_INSURED = 500000.0
        if max_amount > 0 and DEFAULT_SUM_INSURED > 0:
            percentage = (max_amount / DEFAULT_SUM_INSURED) * 100
            field_identifiers["DailyCash_Daily_cash_percentage"] = round(percentage, 2)
        else:
            field_identifiers["DailyCash_Daily_cash_percentage"] = 0.0
    
    # Extract minimum hospitalization days
    min_days_match = re.search(r'more than\s*(\d+)\s*days', text_block, re.IGNORECASE)
    if min_days_match:
        field_identifiers["DailyCash_Minimum_Hospitalization_Days"] = int(min_days_match.group(1))
        field_identifiers["DailyCash_Minimum_LOS_in_days"] = int(min_days_match.group(1))  # Same value for Minimum LOS in days
    
    # Extract maximum days per person
    max_days_match = re.search(r'maximum days of\s*(\d+)', text_block, re.IGNORECASE)
    if max_days_match:
        field_identifiers["DailyCash_Maximum_Days_Per_Person"] = int(max_days_match.group(1))
    
    # Extract waiting period (first days exclusion)
    waiting_period_match = re.search(r'first\s*(\d+)\s*days', text_block, re.IGNORECASE)
    if waiting_period_match:
        field_identifiers["DailyCash_Waiting_Period_Days"] = int(waiting_period_match.group(1))
        field_identifiers["DailyCash_First_Days_Exclusion"] = int(waiting_period_match.group(1))
    
    # Check for maternity exclusion
    if re.search(r'maternity', text_block, re.IGNORECASE):
        field_identifiers["DailyCash_Maternity_Exclusion"] = "Yes"
    
    # Check for Open range (yes/no) - amount ranges like "ranging from Rs 1000 - 2000"
    open_range_patterns = [
        r'ranging from',
        r'range from',
        r'from.*?to.*?rs',
        r'rs.*?to.*?rs',
        r'between.*?rs',
        r'rs.*?-\s*rs',
        r'rs.*?and.*?rs'
    ]
    
    for pattern in open_range_patterns:
        if re.search(pattern, text_block, re.IGNORECASE):
            field_identifiers["DailyCash_Open_range"] = "Yes"
            break
    
    return field_identifiers

def create_addon_coverages(text: str, addon_covers_status: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Main function to orchestrate the extraction. This version ensures the data
    structure is ALWAYS a list of dictionaries.
    """
    DEFAULT_SUM_INSURED = 500000.0
    coverages_data = {}

    # Process Ambulance Cover
    if addon_covers_status.get("Ambulance Cover") == "Yes":
        endorsement_blocks = re.findall(r'Endt\. No\.\s*16(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        ambulance_results = [extract_ambulance_cover_details(block, DEFAULT_SUM_INSURED) for block in endorsement_blocks]
        coverages_data["Ambulance Cover"] = ambulance_results if ambulance_results else [{}]
    else:
        coverages_data["Ambulance Cover"] = [{
            "Sum Insured": "", "Number of Trips": "", "% Limit Applicable On": "", "Limit Percentage": "", "Limit Amount": "", "Applicability": ""
        }]

    # Process Convalescence Benefit
    if addon_covers_status.get("Convalescence Benefit") == "Yes":
        endorsement_blocks = re.findall(r'Endt\. No\.\s*15(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        convalescence_results = [extract_convalescence_benefit_details(block, DEFAULT_SUM_INSURED) for block in endorsement_blocks]
        coverages_data["Convalescence Benefit"] = convalescence_results if convalescence_results else [{}]
    else:
        coverages_data["Convalescence Benefit"] = [{
            "Sum Insured": "", "Minimum LOS in days": "", "Applicable From": "", "Benefit Amount": ""
        }]

    # Process Critical Illness
    if addon_covers_status.get("Critical Illness") == "Yes":
        endorsement_blocks = re.findall(r'Endt\. No\.\s*20(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        critical_illness_results = [extract_critical_illness_field_identifiers(block) for block in endorsement_blocks]
        coverages_data["Critical Illness"] = critical_illness_results if critical_illness_results else [{}]
    else:
        coverages_data["Critical Illness"] = [{
            "Over And Above Policy Sum Insured?": "", "Survival Period Applicable?": "", "Applicable Limit": "", 
            "Sum Insured Per Person": "", "Maximum Limit": "", "Survival Period": "", "Maximum Limit Percentage": ""
        }]

    # Process Daily Cash Cover
    if addon_covers_status.get("Daily Cash Cover") == "Yes":
        endorsement_blocks = re.findall(r'Endt\. No\.\s*14(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        daily_cash_results = [extract_daily_cash_cover_details(block) for block in endorsement_blocks]
        coverages_data["Daily Cash Cover"] = daily_cash_results if daily_cash_results else [{}]
    else:
        coverages_data["Daily Cash Cover"] = [{
            "DailyCash_Over_And_Above_Policy_Sum_Insured": "", "DailyCash_Max_Days_Per_Policy_year": "", "DailyCash_Max_Days_Per_Illness": "", 
            "DailyCash_Fixed_limit": "", "DailyCash_Sum_Insured": "", "DailyCash_Threshold": "", "DailyCash_Limit_Amount": "",
            "DailyCash_Daily_Cash_Amount": "", "DailyCash_Daily_cash_percentage": "", "DailyCash_Minimum_Hospitalization_Days": "", "DailyCash_Minimum_LOS_in_days": "", "DailyCash_Maximum_Days_Per_Person": "", 
            "DailyCash_Waiting_Period_Days": "", "DailyCash_Maternity_Exclusion": "", "DailyCash_First_Days_Exclusion": "", "DailyCash_Open_range": "",
            "DailyCash_Daily_Limit_Range_From": "", "DailyCash_Daily_Limit_Range_To": ""
        }]
        
    return coverages_data

def create_AddonCoverages(text: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Wrapper function to match the import in Main.py.
    Creates a default addon_covers_status dictionary and calls create_addon_coverages.
    """
    # Default addon covers status - you can modify this based on your needs
    default_addon_covers_status = {
        "Ambulance Cover": "Yes",
        "Convalescence Benefit": "Yes", 
        "Critical Illness": "Yes",
        "Daily Cash Cover": "Yes"
    }
    
    return create_addon_coverages(text, default_addon_covers_status)
