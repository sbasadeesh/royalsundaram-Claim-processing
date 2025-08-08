
import re
from typing import List, Dict


def extract_age_ranges(text: str) -> Dict[str, Dict]:
    """
    Extract age ranges dynamically from policy text,
    with proper defaults if no match is found.
    """
    age_ranges = {
        "employee": {"min_years": 18, "min_months": 0, "max_years": 65, "max_months": 0},
        "spouse": {"min_years": 18, "min_months": 0, "max_years": 65, "max_months": 0},
        "children": {"min_years": 0, "min_months": 3, "max_years": 25, "max_months": 0},
        "parents": {"min_years": 40, "min_months": 0, "max_years": 100, "max_months": 0}
    }

    # Employee / Spouse
    employee_age_match = re.search(
        r'employee.*?(?:age|years?)\s*(?:between|from|range)?\s*(\d+)\s*(?:to|-)\s*(\d+)',
        text,
        re.IGNORECASE
    )
    if employee_age_match:
        min_age = int(employee_age_match.group(1))
        max_age = int(employee_age_match.group(2))
        age_ranges["employee"]["min_years"] = min_age
        age_ranges["employee"]["max_years"] = max_age
        age_ranges["spouse"]["min_years"] = min_age
        age_ranges["spouse"]["max_years"] = max_age

    # Children
    children_age_match = re.search(
        r'(?:children|dependent).*?(?:age|years?)\s*(?:between|from|range)?\s*(\d+)\s*(?:to|-)\s*(\d+)',
        text,
        re.IGNORECASE
    )
    if children_age_match:
        min_age = int(children_age_match.group(1))
        max_age = int(children_age_match.group(2))
        age_ranges["children"]["min_years"] = min_age
        age_ranges["children"]["max_years"] = max_age

    # over X days pattern for children minimum
    children_days_match = re.search(r'over\s+(\d+)\s+days?', text, re.IGNORECASE)
    if children_days_match:
        days = int(children_days_match.group(1))
        months = days // 30
        age_ranges["children"]["min_months"] = months

    # Parents
    parents_age_match = re.search(
        r'(?:parents?|father|mother).*?(?:age|years?)\s*(?:between|from|range)?\s*(\d+)\s*(?:to|-)\s*(\d+)',
        text,
        re.IGNORECASE
    )
    if parents_age_match:
        min_age = int(parents_age_match.group(1))
        max_age = int(parents_age_match.group(2))
        age_ranges["parents"]["min_years"] = min_age
        age_ranges["parents"]["max_years"] = max_age

    return age_ranges

def extract_sublimit_info(text: str) -> Dict:
    """Extract sublimit information from PDF text"""
    sublimit_info = {
        "applicable": "No",
        "type": "",
        "limit": 0
    }
    
    # Look for sublimit patterns
    if re.search(r'sublimit', text, re.IGNORECASE):
        sublimit_info["applicable"] = "Yes"
        
        # Extract sublimit type
        type_match = re.search(r'sublimit\s+(?:type|category)?\s*:?\s*([A-Za-z\s]+?)(?:\s+of\s+rs|\s+rs|$)', text, re.IGNORECASE)
        if type_match:
            extracted_type = type_match.group(1).strip()
            # Remove "of" if it appears at the end
            if extracted_type.endswith(" of"):
                extracted_type = extracted_type[:-3].strip()
            # If the extracted type is just "of", leave it blank
            if extracted_type.lower() == "of":
                sublimit_info["type"] = ""
            else:
                sublimit_info["type"] = extracted_type
        # If no type found, leave blank (don't set default)
        
        # Extract sublimit amount
        limit_match = re.search(r'sublimit.*?Rs[\.:]?\s?([\d,]+)', text, re.IGNORECASE)
        if limit_match:
            sublimit_info["limit"] = int(limit_match.group(1).replace(',', ''))
    
    # Look for Endt. No. 5(ii) patterns for specific conditions like Cataract
    endorsement_5ii_match = re.search(r'Endt\.\s*No\.\s*5\(ii\).*?(?=Endt\.\s*No\.|Endorsement\s*No\.|$)', text, re.IGNORECASE | re.DOTALL)
    if endorsement_5ii_match:
        endorsement_5ii_text = endorsement_5ii_match.group(0)
        
        # Look for specific conditions in the table
        conditions = [
            "Cataract",
            "Treatment of mental illness, stress or psychological disorders and neurodegenerative disorders",
            "Balloon Sinuplasty",
            "Stem Cell therapy",
            "Oral Chemotherapy, Immunotherapy",
            "Bronchial Thermoplasty",
            "vaporization of prostate",
            "Intra Operative Neuro Monitoring",
            "Intra vitreal injections"
        ]
        
        for condition in conditions:
            # Look for the condition in the table - more flexible pattern
            condition_match = re.search(
                rf'{re.escape(condition)}.*?(?:10%|25%|5%|%)\s+of\s+the\s+(?:sum\s+)?insured.*?(?:maximum\s+of\s+)?(?:INR\.?|Rs\.?)\s*([\d,]+)',
                endorsement_5ii_text,
                re.IGNORECASE | re.DOTALL
            )
            
            if condition_match:
                sublimit_info["applicable"] = "Yes"
                sublimit_info["type"] = condition
                
                # Extract the percentage and maximum amount
                percentage_match = re.search(
                    rf'{re.escape(condition)}.*?((?:10%|25%|5%|%))\s+of\s+the\s+(?:sum\s+)?insured',
                    endorsement_5ii_text,
                    re.IGNORECASE | re.DOTALL
                )
                
                max_amount_match = re.search(
                    rf'{re.escape(condition)}.*?(?:maximum\s+of\s+)?(?:INR\.?|Rs\.?)\s*([\d,]+)',
                    endorsement_5ii_text,
                    re.IGNORECASE | re.DOTALL
                )
                
                if percentage_match and max_amount_match:
                    percentage = percentage_match.group(1)
                    max_amount = int(max_amount_match.group(1).replace(',', ''))
                    
                    # Handle the case where just "%" is found (default to 10%)
                    if percentage == "%":
                        percentage = "10%"
                    
                    # Store the percentage and max amount for calculation later
                    sublimit_info["percentage"] = percentage
                    sublimit_info["max_amount"] = max_amount
                    
                    # For now, set the limit to the max amount (will be calculated based on sum insured later)
                    sublimit_info["limit"] = max_amount
                break
    
    return sublimit_info



def determine_member_type(min_age_years: int, max_age_years: int) -> str:
    """Determine member type based on age range"""
    # If the age range is primarily for children (max age <= 18)
    if max_age_years <= 18:
        return "Child"
    # If the age range is for adults (min age >= 18)
    elif min_age_years >= 18:
        return "Adult"
    # If the range spans both child and adult ages, determine based on the majority
    else:
        # Calculate the midpoint of the age range
        mid_age = (min_age_years + max_age_years) / 2
        if mid_age < 18:
            return "Child"
        else:
            return "Adult"

def extract_corporate_buffer_applicability(text: str) -> str:
    """
    Checks if Endt. No. 10 or Endorsement No. 10 exists in the text.
    Returns 'Yes' if applicable, else 'No'.
    """
    if re.search(r'(Endt\.|Endorsement)\s*No\.?\s*10\b', text, re.IGNORECASE):
        return "Yes"
    return "No"


def calculate_sublimit(sum_insured: int, percentage: str = "10%", max_amount: int = 200000) -> int:
    """Calculate sublimit based on sum insured, percentage, and maximum amount"""
    if percentage == "10%" or percentage == "%":
        calculated_limit = int(sum_insured * 0.10)
    elif percentage == "25%":
        calculated_limit = int(sum_insured * 0.25)
    elif percentage == "5%":
        calculated_limit = int(sum_insured * 0.05)
    else:
        calculated_limit = int(sum_insured * 0.10)  # Default to 10%
    
    return min(calculated_limit, max_amount)


def extract_Eligibility(text: str) -> List[Dict]:
    # Extract Endorsement No. 1 section
    endorsement_1_match = re.search(r'Endt\.\s*No\.\s*1.*?(?=Endt\.\s*No\.|Endorsement\s*No\.|$)', text, re.IGNORECASE | re.DOTALL)
    
    if not endorsement_1_match:
        # Try alternative patterns for Endt. No. 1
        endorsement_1_match = re.search(r'Endorsement\s*No\.\s*1.*?(?=Endt\.\s*No\.|Endorsement\s*No\.|$)', text, re.IGNORECASE | re.DOTALL)
        
    if not endorsement_1_match:
        # Try to find any section that mentions eligibility or member definitions
        endorsement_1_match = re.search(r'(?:Eligibility|Member|Insured Person).*?(?=Endt\.\s*No\.|Endorsement\s*No\.|$)', text, re.IGNORECASE | re.DOTALL)
    
    if not endorsement_1_match:
        print("[WARNING] Endt. No. 1 section not found, using entire text for extraction")
        endorsement_1_text = text
    else:
        endorsement_1_text = endorsement_1_match.group(0)
    
    # Extract age ranges dynamically from Endorsement No. 1 only
    age_ranges = extract_age_ranges(endorsement_1_text)
    
    # Extract member counts from Endorsement No. 1 only
    # More robust employee detection - look for various patterns that indicate employee coverage
    employee = 0
    if re.search(r'Insured Person covers employees of the Insured', endorsement_1_text, re.IGNORECASE):
        employee = 1
    elif re.search(r'employee', endorsement_1_text, re.IGNORECASE):
        employee = 1
    elif re.search(r'insured person', endorsement_1_text, re.IGNORECASE):
        employee = 1
    # If we have spouse or children but no explicit employee detection, assume employee is covered
    elif re.search(r'spouse', endorsement_1_text, re.IGNORECASE) or re.search(r'children', endorsement_1_text, re.IGNORECASE):
        employee = 1
    # More robust spouse detection
    spouse = 0
    spouse_patterns = [
        r'Spouse\s*-\s*Spouse means the employee[\u2019\'s]{0,2}\s+legally married partner',
        r'spouse',
        r'Dependent Spouse',
        r'Dependant Spouse',
        r'Spouse\s*-\s*(\d+)',
        r'Spouse\s*:\s*(\d+)'
    ]
    
    for pattern in spouse_patterns:
        if re.search(pattern, endorsement_1_text, re.IGNORECASE):
            spouse = 1
            break
    
    # Extract children count dynamically from Endorsement No. 1 only
    children = 0
    
    # Multiple patterns to catch different formats of dependent children mentions
    children_patterns = [
        r'Maximum of (?:the )?first\s*(\d+)\s*dependent children',
        r'Maximum of (?:the )?first\s*(\d+)\s*dependant children',
        r'(\d+)\s*dependent children',
        r'(\d+)\s*dependant children',
        r'Maximum of (?:the )?first\s*(\d+)\s*children',
        r'(\d+)\s*children',
        r'Dependent Children\s*-\s*(\d+)',
        r'Dependant Children\s*-\s*(\d+)',
        r'Children\s*-\s*(\d+)',
        r'Maximum of (?:the )?first\s*(\d+)\s*dependent',
        r'(\d+)\s*dependent',
        r'Children\s*:\s*(\d+)',
        r'Dependent Children\s*:\s*(\d+)',
        r'Dependant Children\s*:\s*(\d+)',
        r'Maximum\s*(\d+)\s*children',
        r'Maximum\s*(\d+)\s*dependent',
        r'Maximum\s*(\d+)\s*dependant',
        r'Up to\s*(\d+)\s*children',
        r'Up to\s*(\d+)\s*dependent',
        r'Up to\s*(\d+)\s*dependant'
    ]
    
    for pattern in children_patterns:
        children_match = re.search(pattern, endorsement_1_text, re.IGNORECASE)
        if children_match:
            children = int(children_match.group(1))
            break
    
    # If no specific count found, check if dependent children are mentioned at all
    if children == 0:
        if re.search(r'dependent children', endorsement_1_text, re.IGNORECASE) or re.search(r'dependant children', endorsement_1_text, re.IGNORECASE):
            # Default to 2 children if mentioned but no count specified
            children = 2
    
    # If we have children but no employee detected, assume employee is covered
    if children > 0 and employee == 0:
        employee = 1
        print(f"[INFO] Employee coverage assumed due to {children} dependent children found")
    
    # Extract parents count from Endorsement No. 1 only
    # Check for various parent patterns
    dependent_parents = 0
    parents_in_law = 0
    
    # Patterns for dependent parents
    dependent_parents_patterns = [
        r'Dependent Parents',
        r'Dependant Parents',
        r'Dependent Parent',
        r'Dependant Parent',
        r'Parents\s*-\s*(\d+)',
        r'Parent\s*-\s*(\d+)'
    ]
    
    for pattern in dependent_parents_patterns:
        if re.search(pattern, endorsement_1_text, re.IGNORECASE):
            dependent_parents = 2  # Default to 2 (father + mother)
            break
    
    # Patterns for parents in law
    parents_in_law_patterns = [
        r'Dependant Parents in law',
        r'Dependent Parents in law',
        r'Dependant Parents-in-law',
        r'Dependent Parents-in-law',
        r'Parents in law',
        r'Parents-in-law'
    ]
    
    for pattern in parents_in_law_patterns:
        if re.search(pattern, endorsement_1_text, re.IGNORECASE):
            parents_in_law = 2  # Default to 2 (father-in-law + mother-in-law)
            break
    
    parents = dependent_parents + parents_in_law
    
    # Calculate total members covered
    total_covered = employee + spouse + children + parents
    
    # Debug information
    print(f"[DEBUG] Endt. No. 1 extraction results:")
    print(f"[DEBUG] - Employee: {employee}")
    print(f"[DEBUG] - Spouse: {spouse}")
    print(f"[DEBUG] - Children: {children}")
    print(f"[DEBUG] - Parents: {parents}")
    print(f"[DEBUG] - Total covered: {total_covered}")
    
    # Extract buffer information from Endorsement No. 1 only
    buffer_match = re.search(r'limit of Rs[\.:]?\s?([\d,]+)', endorsement_1_text, re.IGNORECASE)
    buffer_limit = int(buffer_match.group(1).replace(',', '')) if buffer_match else 0

    # Extract Sum Insured from the policy text
    sum_insured = 0
    sum_insured_match = re.search(r'limit of Rs\.([\d,]+)/- as Corporate floater', text, re.IGNORECASE)
    if sum_insured_match:
        sum_insured = int(sum_insured_match.group(1).replace(",", ""))
    else:
        # Try alternative patterns for sum insured
        sum_insured_match = re.search(r'sum insured.*?Rs\.([\d,]+)', text, re.IGNORECASE)
        if sum_insured_match:
            sum_insured = int(sum_insured_match.group(1).replace(",", ""))
        else:
            # Default sum insured if not found
            sum_insured = 200000  # Default value

    # Extract Corporate Buffer values from Endorsement No: 10
    corporate_buffer_applicable = extract_corporate_buffer_applicability(text)
    corporate_buffer_limit_family = 0
    corporate_buffer_limit_parent = 0
    reload_of_si = "No limit for the reload of SI"
    buffer_opd_limit = 0
    
    # Look for Endorsement No: 10
    endorsement_10_match = re.search(r'Endt\.\s*No\.\s*10.*?(?=Endt\.\s*No\.|Endorsement\s*No\.|$)', text, re.IGNORECASE | re.DOTALL)
    if endorsement_10_match:
        endorsement_10_text = endorsement_10_match.group(0)
        
        # Check if Corporate Buffer/Floater is applicable
        if re.search(r'corporate\s+(?:buffer|floater)', endorsement_10_text, re.IGNORECASE):
            corporate_buffer_applicable = "Yes"
            
            # Extract Corporate Buffer/Floater Limit
            floater_limit_match = re.search(r'limit\s+of\s+Rs[\.:]?\s?([\d,]+).*?corporate\s+(?:buffer|floater)', endorsement_10_text, re.IGNORECASE)
            if floater_limit_match:
                corporate_buffer_limit_family = int(floater_limit_match.group(1).replace(',', ''))
            
            # Extract Corporate Buffer Limit Per Family (if different from floater limit)
            family_limit_match = re.search(r'corporate\s+buffer\s+limit\s+per\s+family.*?Rs[\.:]?\s?([\d,]+)', endorsement_10_text, re.IGNORECASE)
            if family_limit_match:
                corporate_buffer_limit_family = int(family_limit_match.group(1).replace(',', ''))
            
            # Extract Corporate Buffer Limit Per Parent
            parent_limit_match = re.search(r'corporate\s+buffer\s+limit\s+per\s+parent.*?Rs[\.:]?\s?([\d,]+)', endorsement_10_text, re.IGNORECASE)
            if parent_limit_match:
                corporate_buffer_limit_parent = int(parent_limit_match.group(1).replace(',', ''))
            
            # Extract Reload of SI options
            if re.search(r'reload.*?up\s+to\s+double', endorsement_10_text, re.IGNORECASE):
                reload_of_si = "Reload of SI is up to Double"
            elif re.search(r'reload.*?up\s+to\s+thrice', endorsement_10_text, re.IGNORECASE):
                reload_of_si = "Reload of SI is up to the Thr"
            elif re.search(r'reload.*?up\s+to\s+existing', endorsement_10_text, re.IGNORECASE):
                reload_of_si = "Reload of SI is up to the Exis"
            elif re.search(r'no\s+limit.*?reload', endorsement_10_text, re.IGNORECASE):
                reload_of_si = "No limit for the reload of SI"
            
            # Extract Buffer OPD Limit
            opd_limit_match = re.search(r'buffer\s+opd\s+limit.*?Rs[\.:]?\s?([\d,]+)', endorsement_10_text, re.IGNORECASE)
            if opd_limit_match:
                buffer_opd_limit = int(opd_limit_match.group(1).replace(',', ''))

    # Extract Critical Illness values
    critical_illness_applicable = "No"
    critical_illness_limit_family = 0.0
    
    # Look for Critical Illness in the policy text
    if re.search(r'critical\s+illness', text, re.IGNORECASE):
        critical_illness_applicable = "Yes"
        
        # Extract Critical Illness limit per family
        critical_limit_match = re.search(r'critical\s+illness\s+limit\s+per\s+family.*?Rs[\.:]?\s?([\d,]+)', text, re.IGNORECASE)
        if critical_limit_match:
            critical_illness_limit_family = float(critical_limit_match.group(1).replace(',', ''))
        else:
            # Look for general critical illness limit
            general_critical_match = re.search(r'critical\s+illness.*?limit.*?Rs[\.:]?\s?([\d,]+)', text, re.IGNORECASE)
            if general_critical_match:
                critical_illness_limit_family = float(general_critical_match.group(1).replace(',', ''))

    # Extract sublimit information from the entire text (including Endt. No. 5(ii))
    sublimit_info = extract_sublimit_info(text)
    
    # Calculate actual sublimit based on sum insured and percentage from Endt. No. 5(ii)
    if sublimit_info["applicable"] == "Yes" and "percentage" in sublimit_info:
        percentage_str = sublimit_info["percentage"]
        if percentage_str == "10%" or percentage_str == "%":
            calculated_limit = int(sum_insured * 0.10)
        elif percentage_str == "25%":
            calculated_limit = int(sum_insured * 0.25)
        elif percentage_str == "5%":
            calculated_limit = int(sum_insured * 0.05)
        else:
            calculated_limit = sublimit_info["limit"]
        
        # Apply the maximum limit constraint
        if "max_amount" in sublimit_info:
            sublimit_info["limit"] = min(calculated_limit, sublimit_info["max_amount"])
        else:
            sublimit_info["limit"] = calculated_limit

    covers = []

    # Add Employee as first row with ALL FIELDS
    if employee > 0:
        age_data = age_ranges["employee"]
        member_type = determine_member_type(age_data["min_years"], age_data["max_years"])
        
        covers.append({
            "Max No Of Members Covered": total_covered,
            "Relationship Covered (Member Count)": total_covered,
            "Relationship Covered": "Employee",
            "Min_Age(In Years)": age_data["min_years"],
            "Min_Age(In Months)": age_data["min_months"],
            "Max_Age(In Years)": age_data["max_years"],
            "Max_Age(In Months)": age_data["max_months"],
            "Member": 1,
            "Member_Count": employee,
            "Member_Type": member_type,
            "Sublimit_Applicable": sublimit_info["applicable"],
            "Sublimit_Type": sublimit_info["type"],
            "Sub_Limit": sublimit_info["limit"],
            "Family Buffer Applicable": "Yes" if buffer_limit > 0 else "No",
            "Family Buffer Amount": buffer_limit,
            "Is Network Applicable": "No",
            "Black listed hospitals are applicable?": "Yes",

            # Corporate Buffer & Additional Fields
            "Corporate Buffer applicable": corporate_buffer_applicable,
            "Buffer Type": "Both" if corporate_buffer_applicable == "Yes" else "",
            "Applicable for": "Normal Illness and Critical Illness" if corporate_buffer_applicable == "Yes" else "",
            "Total Corporate Buffer": corporate_buffer_limit_family,
            "Corporate Buffer Limit Per Family": corporate_buffer_limit_family,
            "Corporate Buffer Limit Per Parent": corporate_buffer_limit_parent,
            "Reload of SI": reload_of_si,
            "Total Corporate Buffer.1": corporate_buffer_limit_family,
            "Corporate Buffer Limit Per Family.1": corporate_buffer_limit_family,
            "Corporate Buffer Limit Per Parent.1": corporate_buffer_limit_parent,
            "Reload of SI.1": reload_of_si,
            "Approving Authority": "" if corporate_buffer_applicable == "No" else "Corporate HR",
            "Buffer OPD Limit": buffer_opd_limit,
            "Whether increase in sum insured permissible at renewal": "No",
            "Total Plan Buffer": corporate_buffer_limit_family,
            "Corporate Bufferr Limit for Employee/Family": corporate_buffer_limit_family,
            "Corporate Buffer Limit Per Parent.2": corporate_buffer_limit_parent,
            "Reload of SI.2": reload_of_si,
            "Approving Authority.1": "" if corporate_buffer_applicable == "No" else "Corporate HR",
            "Buffer OPD Limit.1": buffer_opd_limit,
            "Whether increase in sum insured permissible at renewal.1": "No",

            # Critical Illness Fields
            "Critical Illness applicable": critical_illness_applicable,
            "Critical Illness limit per family": critical_illness_limit_family,
            "Critical Illness Approving Authority": "" if critical_illness_applicable == "No" else "Corporate HR",
            "Critical Illness Whether increase in sum insured permissible at renewal": "No"
        })

    # Add Spouse as separate row with ONLY BASIC FIELDS
    if spouse > 0:
        age_data = age_ranges["spouse"]
        member_type = determine_member_type(age_data["min_years"], age_data["max_years"])
        
        covers.append({
            "Relationship Covered": "Spouse",
            "Min_Age(In Years)": age_data["min_years"],
            "Min_Age(In Months)": age_data["min_months"],
            "Max_Age(In Years)": age_data["max_years"],
            "Max_Age(In Months)": age_data["max_months"],
            "Member": 1,
            "Member_Type": member_type
        })

    # Add Son as separate row with ONLY BASIC FIELDS
    if children > 0:
        age_data = age_ranges["children"]
        member_type = determine_member_type(age_data["min_years"], age_data["max_years"])
        
        covers.append({
            "Relationship Covered": "Son",
            "Min_Age(In Years)": age_data["min_years"],
            "Min_Age(In Months)": age_data["min_months"],
            "Max_Age(In Years)": age_data["max_years"],
            "Max_Age(In Months)": age_data["max_months"],
            "Member": 1,
            "Member_Type": member_type
        })

    # Add Daughter as separate row with ONLY BASIC FIELDS
    if children > 0:
        age_data = age_ranges["children"]
        member_type = determine_member_type(age_data["min_years"], age_data["max_years"])
        
        covers.append({
            "Relationship Covered": "Daughter",
            "Min_Age(In Years)": age_data["min_years"],
            "Min_Age(In Months)": age_data["min_months"],
            "Max_Age(In Years)": age_data["max_years"],
            "Max_Age(In Months)": age_data["max_months"],
            "Member": 1,
            "Member_Type": member_type
        })

    # Add Parents as separate rows with ONLY BASIC FIELDS (Father, Mother, Father-in-law, Mother-in-law) if applicable
    if dependent_parents > 0:
        age_data = age_ranges["parents"]
        member_type = determine_member_type(age_data["min_years"], age_data["max_years"])
        
        # Add Father row (from Dependent Parents)
        covers.append({
            "Relationship Covered": "Father",
            "Min_Age(In Years)": age_data["min_years"],
            "Min_Age(In Months)": age_data["min_months"],
            "Max_Age(In Years)": age_data["max_years"],
            "Max_Age(In Months)": age_data["max_months"],
            "Member": 1,
            "Member_Type": member_type
        })

        # Add Mother row (from Dependent Parents)
        covers.append({
            "Relationship Covered": "Mother",
            "Min_Age(In Years)": age_data["min_years"],
            "Min_Age(In Months)": age_data["min_months"],
            "Max_Age(In Years)": age_data["max_years"],
            "Max_Age(In Months)": age_data["max_months"],
            "Member": 1,
            "Member_Type": member_type
        })

    # Add Parents-in-law as separate rows with ONLY BASIC FIELDS (Father-in-law and Mother-in-law) if applicable
    if parents_in_law > 0:
        age_data = age_ranges["parents"]
        member_type = determine_member_type(age_data["min_years"], age_data["max_years"])
        
        # Add Father-in-law row (from Dependant Parents in law)
        covers.append({
            "Relationship Covered": "Father-in-law",
            "Min_Age(In Years)": age_data["min_years"],
            "Min_Age(In Months)": age_data["min_months"],
            "Max_Age(In Years)": age_data["max_years"],
            "Max_Age(In Months)": age_data["max_months"],
            "Member": 1,
            "Member_Type": member_type
        })

        # Add Mother-in-law row (from Dependant Parents in law)
        covers.append({
            "Relationship Covered": "Mother-in-law",
            "Min_Age(In Years)": age_data["min_years"],
            "Min_Age(In Months)": age_data["min_months"],
            "Max_Age(In Years)": age_data["max_years"],
            "Max_Age(In Months)": age_data["max_months"],
            "Member": 1,
            "Member_Type": member_type
        })

    return covers
