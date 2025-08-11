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

def extract_all_sublimits_from_endorsement_5ii(text: str) -> List[Dict]:
    """Extract ALL sublimits from Endt. No. 5(ii) section dynamically"""
    sublimits = []
    
    # Look for Endt. No. 5(ii) patterns
    endorsement_5ii_match = re.search(r'Endt\.\s*No\.\s*5\(ii\).*?(?=Endt\.\s*No\.|Endorsement\s*No\.|$)', text, re.IGNORECASE | re.DOTALL)
    if endorsement_5ii_match:
        endorsement_5ii_text = endorsement_5ii_match.group(0)
        print(f"[DEBUG] Found Endt. No. 5(ii) section")
        
        # Dynamic pattern to find ALL table rows with conditions and limits
        # Look for patterns like: "Condition Name | Amount" or "Condition Name | Nil Capping"
        
        # Dynamic pattern to extract table rows - find condition names from actual table structure
        table_row_patterns = [
            # Pattern 1: Exact condition names from table (case-insensitive) - ENHANCED VAPORIZATION PATTERNS
            r'(Cataract)\s*(?:\||Nil|50%|$)',
            r'(Balloon\s+Sinsuplasty)\s*(?:\||50%|$)',
            r'(Stem\s+Cell\s+therapy\s*-\s*Hematopoietic\s+stem\s+cells\s+for\s+bone\s+marrow\s+transplant\s+for\s+haematological\s+conditions\s+to\s+be\s+covered)\s*(?:\||50%|$)',
            r'(Oral\s+Chemotherapy,\s+Immunotherapy\s*\(\s*monoclonal\s+antibody\s+to\s+be\s+given\s+as\s+injection\s*\))\s*(?:\||50%|$)',
            r'(Bronchical\s+Thermoplasty)\s*(?:\||50%|$)',
            
            # MULTIPLE VAPORIZATION PATTERNS - to handle different formats
            r'(vaporization\s+of\s+prostate\s*\(\s*green\s+laser\s+treatment\s*\)),?\s*(?:\||Nil|50%|10%)',
            r'(vaporization\s+of\s+prostate\s*\(\s*green\s+laser\s+treatment\s*\))',
            r'(vaporization\s+of\s+prostate\s*\([^)]*\))',
            r'(vaporization\s+of\s+prostate)',
            
            r'(Intra\s+Operative\s+Neuro\s+Monitoring)\s*(?:\||50%|$)',
            r'(Intra\s+vitreal\s+injections)\s*(?:\||50%|$)',
            
            # Pattern 2: More flexible patterns for variations
            r'(Treatment\s+of\s+mental\s+illness,\s+stress\s+or\s+psychological\s+disorders\s+and\s+neurodegenerative\s+disorders\.?)',
            r'(Stem\s+[Cc]ell\s+[Tt]herapy(?:\s*-[^|]*)?)',
            r'(Oral\s+[Cc]hemotherapy,?\s*[Ii]mmunotherapy(?:\s*\([^)]+\))?)',
            r'(Balloon\s+[Ss]in[us]*plasty)',
            r'(Bronchical?\s+[Tt]hermoplasty)',
            r'(Intra\s+[Oo]perative\s+[Nn]euro\s+[Mm]onitoring)',
            r'(Intra\s+[Vv]itreal\s+[Ii]njections)',
            
            # Pattern 3: Condition followed by "Nil Capping" - enhanced for vaporization
            r'^([A-Za-z][A-Za-z\s,\-()]+?)\s+Nil\s+Capping',
            r'(vaporization[^|]+?)\s+Nil\s+Capping',
            
            # Pattern 4: Condition followed by percentage and amount description - enhanced for vaporization
            r'^([A-Za-z][A-Za-z\s,\-()]+?)\s+(?:50%|10%|25%|5%)\s+of\s+the\s+sum\s+insured',
            r'(vaporization[^|]+?)\s+(?:50%|10%|25%|5%)\s+of\s+the\s+sum\s+insured',
            
            # Pattern 5: Medical conditions with specific keywords (broader match)
            r'([A-Za-z\s,\-()]*(?:[Tt]herapy|[Pp]lasty|[Mm]onitoring|[Ii]njections|[Cc]hemotherapy|[Ii]mmunotherapy|[Cc]ell|[Pp]rostate|[Nn]euro|[Vv]itreal|[Cc]ataract|[Tt]reatment)[A-Za-z\s,\-()]*)',
            
        ]
        
        # Split the text into lines and process each line
        lines = endorsement_5ii_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 5:  # Skip empty or very short lines
                continue
                
            print(f"[DEBUG] Processing line: {line[:100]}...")  # Debug first 100 chars
            
            # Special debug for vaporization
            if "vaporization" in line.lower():
                print(f"[DEBUG] Found vaporization line: {line}")
                print(f"[DEBUG] Vaporization line will be tested against {len(table_row_patterns)} patterns")
            
            # Try to extract condition and limit from each line
            for pattern_idx, pattern in enumerate(table_row_patterns):
                match = re.search(pattern, line, re.IGNORECASE | re.MULTILINE)
                if match:
                    condition_name = match.group(1).strip()
                    
                    # Debug for vaporization matches
                    if "vaporization" in condition_name.lower():
                        print(f"[DEBUG] VAPORIZATION MATCH found with pattern {pattern_idx}: '{condition_name}'")
                        print(f"[DEBUG] Pattern was: {pattern}")
                    
                    # Clean up condition name
                    condition_name = re.sub(r'^[\d\.\s\|]+', '', condition_name)  # Remove leading numbers/pipes
                    condition_name = re.sub(r'\s*\|\s*.*$', '', condition_name)  # Remove anything after pipe
                    condition_name = condition_name.strip()
                    
                    # Debug after cleanup
                    if "vaporization" in condition_name.lower():
                        print(f"[DEBUG] VAPORIZATION condition after cleanup: '{condition_name}'")
                    
                    # Skip if condition name is too short, looks like a header, or contains unwanted patterns
                    skip_patterns = [
                        'sublimit', 'type', 'limit', 'condition', 'claim amount', 'payable', 'treatment',
                        'disease', 'illness', 'medical condition', 'injury', 'subject to', 'terms',
                        'exclusions', 'conditions', 'contained', 'policy', 'endorsed', 'declared',
                        'agreed', 'otherwise', 'following', 'HG00', 'Group Health', 'UIN:', 'IRDA'
                    ]
                    
                    if (len(condition_name) < 3 or 
                        any(skip in condition_name.lower() for skip in skip_patterns) or
                        re.match(r'^[0-9%\s\-/]+$', condition_name)):  # Skip if only numbers/symbols
                        continue
                    
                    # Check if we already have this condition
                    existing_condition = False
                    for existing in sublimits:
                        if existing['type'].lower().replace(' ', '') == condition_name.lower().replace(' ', ''):
                            existing_condition = True
                            break
                    
                    if existing_condition:
                        continue
                    
                    sublimit_info = {
                        "applicable": "Yes",
                        "type": condition_name,
                        "limit": ""
                    }
                    
                    # Check if this line has "Nil Capping" anywhere
                    if re.search(r'Nil\s+Capping|nil\s+capping|NIL\s+CAPPING', line, re.IGNORECASE):
                        sublimit_info["limit"] = ""
                        print(f"[DEBUG] Found condition: {condition_name} with Nil Capping")
                    else:
                        # Try to extract amount from the same line
                        amount_match = re.search(r'(?:INR\.?|Rs\.?)\s*([\d,]+)', line, re.IGNORECASE)
                        if amount_match:
                            amount_str = amount_match.group(1).replace(',', '')
                            sublimit_info["limit"] = amount_str
                            print(f"[DEBUG] Found condition: {condition_name} with amount: {amount_str}")
                        else:
                            # Look for amount in the next few lines after this condition
                            for next_line_idx in range(lines.index(line) + 1, min(lines.index(line) + 5, len(lines))):
                                next_line = lines[next_line_idx].strip()
                                amount_match = re.search(r'(?:INR\.?|Rs\.?)\s*([\d,]+)', next_line, re.IGNORECASE)
                                if amount_match:
                                    amount_str = amount_match.group(1).replace(',', '')
                                    sublimit_info["limit"] = amount_str
                                    print(f"[DEBUG] Found condition: {condition_name} with amount in next line: {amount_str}")
                                    break
                            else:
                                sublimit_info["limit"] = ""
                                print(f"[DEBUG] Found condition: {condition_name} with no amount")
                    
                    sublimits.append(sublimit_info)
                    break  # Found a match for this line, move to next line
        
        # Post-process to clean up condition names and merge related entries
        cleaned_sublimits = []
        condition_map = {}
        
        for sublimit in sublimits:
            condition_name = sublimit["type"]
            
            # Clean up condition names based on common patterns
            cleaned_name = condition_name
            
            # Handle specific cleanup cases - standardize the condition names based on exact table format
            condition_lower = condition_name.lower()
            
            # Handle exact matches from the table first - ENHANCED FOR VAPORIZATION
            if "stem cell therapy - hematopoietic" in condition_lower:
                cleaned_name = "Stem Cell therapy - Hematopoietic stem cells for bone marrow transplant for haematological conditions to be covered"
            elif "oral chemotherapy, immunotherapy(monoclonal" in condition_lower:
                cleaned_name = "Oral Chemotherapy, Immunotherapy(monoclonal antibody to be given as injection)"
            # ENHANCED VAPORIZATION HANDLING - Handle different variations
            elif "vaporization of prostate(green laser treatment)" in condition_lower:
                cleaned_name = "vaporization of prostate(green laser treatment)"
            elif "vaporization of prostate(green laser" in condition_lower:
                cleaned_name = "vaporization of prostate(green laser treatment)"
            elif "vaporization of prostate" in condition_lower and "green laser" in condition_lower:
                cleaned_name = "vaporization of prostate(green laser treatment)"
            elif "vaporization of prostate" in condition_lower and "green" not in condition_lower:
                cleaned_name = "vaporization of prostate"
            # Handle any other vaporization variations
            elif "vaporization" in condition_lower and "prostate" in condition_lower:
                if "green" in condition_lower or "laser" in condition_lower:
                    cleaned_name = "vaporization of prostate(green laser treatment)"
                else:
                    cleaned_name = "vaporization of prostate"
                print(f"[DEBUG] VAPORIZATION condition standardized to: '{cleaned_name}'")
            elif "stem cell therapy" in condition_lower or "bone marrow transplant" in condition_lower:
                cleaned_name = "Stem Cell therapy"
            elif "oral chemotherapy" in condition_lower and "immunotherapy" in condition_lower:
                cleaned_name = "Oral Chemotherapy, Immunotherapy"
            elif "bronchial thermoplasty" in condition_lower or "bronchical thermoplasty" in condition_lower:
                cleaned_name = "Bronchical Thermoplasty"
            elif "intra operative neuro monitoring" in condition_lower:
                cleaned_name = "Intra Operative Neuro Monitoring"
            elif "balloon" in condition_lower and ("sinuplasty" in condition_lower or "sinsuplasty" in condition_lower):
                cleaned_name = "Balloon Sinsuplasty"
            elif "treatment of mental illness" in condition_lower:
                cleaned_name = "Treatment of mental illness, stress or psychological disorders and neurodegenerative disorders."
            elif "intra vitreal injections" in condition_lower:
                cleaned_name = "Intra vitreal injections"
            elif "cataract" in condition_lower:
                cleaned_name = "Cataract"
            
            # Remove trailing commas and clean up
            cleaned_name = re.sub(r',\s*$', '', cleaned_name)
            cleaned_name = cleaned_name.strip()
            
            # Skip if this is a duplicate or sub-part of existing condition
            if cleaned_name not in condition_map:
                condition_map[cleaned_name] = {
                    "applicable": sublimit["applicable"],
                    "type": cleaned_name,
                    "limit": sublimit["limit"]
                }
            else:
                # If we already have this condition, keep the one with a limit if available
                if sublimit["limit"] and not condition_map[cleaned_name]["limit"]:
                    condition_map[cleaned_name]["limit"] = sublimit["limit"]
        
        # Convert back to list
        sublimits = list(condition_map.values())
    
    print(f"[DEBUG] Total sublimits extracted: {len(sublimits)}")
    for i, sublimit in enumerate(sublimits):
        print(f"[DEBUG] {i+1}. Type: '{sublimit['type']}', Limit: '{sublimit['limit']}'")
    
    return sublimits


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


def get_complete_row_template():
    """Return a complete row template with all required fields as empty strings"""
    return {
        "Max No Of Members Covered": "",
        "Relationship Covered (Member Count)": "",
        "Relationship Covered": "",
        "Min_Age(In Years)": "",
        "Min_Age(In Months)": "",
        "Max_Age(In Years)": "",
        "Max_Age(In Months)": "",
        "Member_Count": "",
        "Member_Type": "",
        "Sublimit_Applicable": "",
        "Sublimit_Type": "",
        "Sub_Limit": "",
        "Family Buffer Applicable": "",
        "Family Buffer Amount": "",
        "Is Network Applicable": "",
        "Black listed hospitals are applicable?": "",
        "Corporate Buffer applicable": "",
        "Buffer Type": "",
        "Applicable for": "",
        "Total Corporate Buffer": "",
        "Corporate Buffer Limit Per Family": "",
        "Corporate Buffer Limit Per Parent": "",
        "Reload of SI": "",
        "Total Corporate Buffer.1": "",
        "Corporate Buffer Limit Per Family.1": "",
        "Corporate Buffer Limit Per Parent.1": "",
        "Reload of SI.1": "",
        "Approving Authority": "",
        "Buffer OPD Limit": "",
        "Whether increase in sum insured permissible at renewal": "",
        "Total Plan Buffer": "",
        "Corporate Bufferr Limit for Employee/Family": "",
        "Corporate Buffer Limit Per Parent.2": "",
        "Reload of SI.2": "",
        "Approving Authority.1": "",
        "Buffer OPD Limit.1": "",
        "Whether increase in sum insured permissible at renewal.1": "",
        "Critical Illness applicable": "",
        "Critical Illness limit per family": "",
        "Critical Illness Approving Authority": "",
        "Critical Illness Whether increase in sum insured permissible at renewal": ""
    }

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
            
            # Extract Reload of SI options - Per person limit pattern
            if re.search(r'per\s+person\s+limit', endorsement_10_text, re.IGNORECASE):
                reload_of_si = "Reload of SI is up to the Existing SI"
            
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

    # Extract ALL sublimits from Endt. No. 5(ii)
    all_sublimits = extract_all_sublimits_from_endorsement_5ii(text)

    covers = []

    # MAIN EMPLOYEE ROW - Contains all the comprehensive data including first sublimit
    if employee > 0:
        age_data = age_ranges["employee"]
        member_type = determine_member_type(age_data["min_years"], age_data["max_years"])
        
        # Create the main Employee row with ALL comprehensive information INCLUDING first sublimit
        main_employee_row = {
            "Max No Of Members Covered": total_covered,
            "Relationship Covered (Member Count)": total_covered,
            "Relationship Covered": "Employee",
            "Min_Age(In Years)": age_data["min_years"] if age_data["min_years"] != 0 else "",
            "Min_Age(In Months)": age_data["min_months"] if age_data["min_months"] != 0 else "",
            "Max_Age(In Years)": age_data["max_years"] if age_data["max_years"] != 0 else "",
            "Max_Age(In Months)": age_data["max_months"] if age_data["max_months"] != 0 else "",
            "Member_Count": employee,
            "Member_Type": member_type,
            "Sublimit_Applicable": "Yes" if all_sublimits else "No",
            "Sublimit_Type": all_sublimits[0]["type"] if all_sublimits else "",  # First sublimit type
            "Sub_Limit": str(all_sublimits[0]["limit"]) if all_sublimits else "",  # First sublimit amount
            "Family Buffer Applicable": corporate_buffer_applicable,
            "Family Buffer Amount": corporate_buffer_limit_family,
            "Is Network Applicable": "No",
            "Black listed hospitals are applicable?": "Yes",

            # Corporate Buffer & Additional Fields
            "Corporate Buffer applicable": "Yes" if corporate_buffer_applicable == "Yes" else "",
            "Buffer Type": "Both" if corporate_buffer_applicable == "Yes" else "",
            "Applicable for": "",
            "Total Corporate Buffer": "",
            "Corporate Buffer Limit Per Family": "",
            "Corporate Buffer Limit Per Parent": "",
            "Reload of SI": "",
            "Total Corporate Buffer.1": "",
            "Corporate Buffer Limit Per Family.1": "",
            "Corporate Buffer Limit Per Parent.1": "",
            "Reload of SI.1": "",
            "Approving Authority": "" ,
            "Buffer OPD Limit": "",
            "Whether increase in sum insured permissible at renewal": "",
            "Total Plan Buffer": corporate_buffer_limit_family if corporate_buffer_applicable == "Yes" !=0  else "",
            "Corporate Bufferr Limit for Employee/Family": corporate_buffer_limit_family if corporate_buffer_applicable == "Yes" !=0 else "",
            "Corporate Buffer Limit Per Parent.2": corporate_buffer_limit_family if corporate_buffer_applicable == "Yes" !=0 else "",
            "Reload of SI.2": reload_of_si if corporate_buffer_applicable == "Yes" !=0 else "",
            "Approving Authority.1": "Corporate HR" if corporate_buffer_applicable == "Yes" !=0 else "",
            "Buffer OPD Limit.1": buffer_opd_limit if corporate_buffer_applicable == "Yes" !=0 else "",
            "Whether increase in sum insured permissible at renewal.1": "No" if corporate_buffer_applicable == "Yes" !=0 else "",

            # Critical Illness Fields
            "Critical Illness applicable": critical_illness_applicable,
            "Critical Illness limit per family": "",
            "Critical Illness Approving Authority": "" if critical_illness_applicable == "No" else "Corporate HR",
            "Critical Illness Whether increase in sum insured permissible at renewal": ""
        }
        covers.append(main_employee_row)

        # # Add additional rows for remaining sublimits (if more than one sublimit exists)
        # # This should be OUTSIDE the employee condition to ensure it runs
        # if all_sublimits and len(all_sublimits) > 1:
        #     for sublimit in all_sublimits[1:]:  # Start from second sublimit (index 1)
        #         additional_sublimit_row = {
        #             "Max No Of Members Covered": "",
        #             "Relationship Covered (Member Count)": "",
        #             "Relationship Covered": "Employee",
        #             "Min_Age(In Years)": "",
        #             "Min_Age(In Months)": "",
        #             "Max_Age(In Years)": "",
        #             "Max_Age(In Months)": "",
        #             "Member_Count": "",
        #             "Member_Type": "",
        #             "Sublimit_Applicable": "Yes",
        #             "Sublimit_Type": sublimit["type"],
        #             "Sub_Limit": str(sublimit["limit"]),
        #             "Family Buffer Applicable": "",
        #             "Family Buffer Amount": "",
        #             "Is Network Applicable": "",
        #             "Black listed hospitals are applicable?": "",

        #             # Corporate Buffer & Additional Fields - All empty for additional rows
        #             "Corporate Buffer applicable": "",
        #             "Buffer Type": "",
        #             "Applicable for": "",
        #             "Total Corporate Buffer": "",
        #             "Corporate Buffer Limit Per Family": "",
        #             "Corporate Buffer Limit Per Parent": "",
        #             "Reload of SI": "",
        #             "Total Corporate Buffer.1": "",
        #             "Corporate Buffer Limit Per Family.1": "",
        #             "Corporate Buffer Limit Per Parent.1": "",
        #             "Reload of SI.1": "",
        #             "Approving Authority": "",
        #             "Buffer OPD Limit": "",
        #             "Whether increase in sum insured permissible at renewal": "",
        #             "Total Plan Buffer": "",
        #             "Corporate Bufferr Limit for Employee/Family": "",
        #             "Corporate Buffer Limit Per Parent.2": "",
        #             "Reload of SI.2": "",
        #             "Approving Authority.1": "",
        #             "Buffer OPD Limit.1": "",
        #             "Whether increase in sum insured permissible at renewal.1": "",

        #             # Critical Illness Fields - All empty for additional rows
        #             "Critical Illness applicable": "",
        #             "Critical Illness limit per family": "",
        #             "Critical Illness Approving Authority": "",
        #             "Critical Illness Whether increase in sum insured permissible at renewal": ""
        #         }
        #         covers.append(additional_sublimit_row)

        # SPOUSE ROW - Basic information only
        if spouse > 0:
            age_data = age_ranges["spouse"]
            member_type = determine_member_type(age_data["min_years"], age_data["max_years"])
            
            spouse_row = get_complete_row_template()
            spouse_row.update({
                "Relationship Covered": "Spouse",
                "Min_Age(In Years)": age_data["min_years"] if age_data["min_years"] != 0 else "",
                "Min_Age(In Months)": age_data["min_months"] if age_data["min_months"] != 0 else "",
                "Max_Age(In Years)": age_data["max_years"] if age_data["max_years"] != 0 else "",
                "Max_Age(In Months)": age_data["max_months"] if age_data["max_months"] != 0 else "",
                "Member_Count": employee,
                "Member_Type": member_type,
                "Sublimit_Applicable": "yes",
              
            })
            covers.append(spouse_row)

        # SON ROW - Basic information only
        if children > 0:
            age_data = age_ranges["children"]
            member_type = determine_member_type(age_data["min_years"], age_data["max_years"])
            
            son_row = get_complete_row_template()
            son_row.update({
                "Relationship Covered": "Son",
                "Min_Age(In Years)": age_data["min_years"] if age_data["min_years"] != 0 else "",
                "Min_Age(In Months)": age_data["min_months"] if age_data["min_months"] != 0 else "",
                "Max_Age(In Years)": age_data["max_years"] if age_data["max_years"] != 0 else "",
                "Max_Age(In Months)": age_data["max_months"] if age_data["max_months"] != 0 else "",
                "Member_Count": employee,
                "Member_Type": member_type,
                "Sublimit_Applicable": "yes",
            })
            covers.append(son_row)

        # DAUGHTER ROW - Basic information only
        if children > 0:
            age_data = age_ranges["children"]
            member_type = determine_member_type(age_data["min_years"], age_data["max_years"])
            
            daughter_row = get_complete_row_template()
            daughter_row.update({
                "Relationship Covered": "Daughter",
                "Min_Age(In Years)": age_data["min_years"] if age_data["min_years"] != 0 else "",
                "Min_Age(In Months)": age_data["min_months"] if age_data["min_months"] != 0 else "",
                "Max_Age(In Years)": age_data["max_years"] if age_data["max_years"] != 0 else "",
                "Max_Age(In Months)": age_data["max_months"] if age_data["max_months"] != 0 else "",
                "Member_Count": employee,
                "Member_Type": member_type,
                "Sublimit_Applicable": "yes",
            })
            covers.append(daughter_row)

        # FATHER ROW - Basic information only (if dependent parents exist)
        if dependent_parents > 0:
            age_data = age_ranges["parents"]
            member_type = determine_member_type(age_data["min_years"], age_data["max_years"])
            
            father_row = get_complete_row_template()
            father_row.update({
                "Relationship Covered": "Father",
                "Min_Age(In Years)": age_data["min_years"] if age_data["min_years"] != 0 else "",
                "Min_Age(In Months)": age_data["min_months"] if age_data["min_months"] != 0 else "",
                "Max_Age(In Years)": age_data["max_years"] if age_data["max_years"] != 0 else "",
                "Max_Age(In Months)": age_data["max_months"] if age_data["max_months"] != 0 else "",
                "Member_Count": employee,
                "Member_Type": member_type,
                "Sublimit_Applicable": "yes",
            })
            covers.append(father_row)

            # MOTHER ROW - Basic information only
            mother_row = get_complete_row_template()
            mother_row.update({
                "Relationship Covered": "Mother",
                "Min_Age(In Years)": age_data["min_years"] if age_data["min_years"] != 0 else "",
                "Min_Age(In Months)": age_data["min_months"] if age_data["min_months"] != 0 else "",
                "Max_Age(In Years)": age_data["max_years"] if age_data["max_years"] != 0 else "",
                "Max_Age(In Months)": age_data["max_months"] if age_data["max_months"] != 0 else "",
                "Member_Count": employee,
                "Member_Type": member_type,
                "Sublimit_Applicable": "yes",
            })
            covers.append(mother_row)

        # FATHER-IN-LAW ROW - Basic information only (if parents in law exist)
        if parents_in_law > 0:
            age_data = age_ranges["parents"]
            member_type = determine_member_type(age_data["min_years"], age_data["max_years"])
            
            father_in_law_row = get_complete_row_template()
            father_in_law_row.update({
                "Relationship Covered": "Father-in-law",
                "Min_Age(In Years)": age_data["min_years"] if age_data["min_years"] != 0 else "",
                "Min_Age(In Months)": age_data["min_months"] if age_data["min_months"] != 0 else "",
                "Max_Age(In Years)": age_data["max_years"] if age_data["max_years"] != 0 else "",
                "Max_Age(In Months)": age_data["max_months"] if age_data["max_months"] != 0 else "",
                "Member_Count": employee,
                "Member_Type": member_type,
                "Sublimit_Applicable": "yes",
            })
            covers.append(father_in_law_row)

            # MOTHER-IN-LAW ROW - Basic information only
            mother_in_law_row = get_complete_row_template()
            mother_in_law_row.update({
                "Relationship Covered": "Mother-in-law",
                "Min_Age(In Years)": age_data["min_years"] if age_data["min_years"] != 0 else "",
                "Min_Age(In Months)": age_data["min_months"] if age_data["min_months"] != 0 else "",
                "Max_Age(In Years)": age_data["max_years"] if age_data["max_years"] != 0 else "",
                "Max_Age(In Months)": age_data["max_months"] if age_data["max_months"] != 0 else "",
                "Member_Count": employee,
                "Member_Type": member_type,
                "Sublimit_Applicable": "yes",
            })
            covers.append(mother_in_law_row)

        # Clean all data to remove None values and replace with empty strings
        cleaned_covers = []
        for cover in covers:
            cleaned_cover = {}
            for key, value in cover.items():
                if value is None:
                    cleaned_cover[key] = ""
                else:
                    cleaned_cover[key] = value
            cleaned_covers.append(cleaned_cover)

        return cleaned_covers