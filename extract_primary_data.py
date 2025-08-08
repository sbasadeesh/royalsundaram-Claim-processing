import re
from typing import List, Dict

def extract_newborn_from_endt_12(text: str) -> Dict:
    """Extract New Born data specifically from Endorsement No. 12/12a"""
    newborn_data = {
        "New Born Covered?": "No",
        "New Born Covered": "No",
        "Covered From": "Day 0",
        "Is New Born Limit Applicable": "No",
        "Sum Insured": "",
        "% Limit Applicable On": "Sum Insured",
        "Limit Percentage": "",
        "Limit Amount": "",
        "Applicability": "Lower",
        "New Born Sum Insured": "Sum Insured",
        "New Born % Limit": "",
        "New Born Limit": "",
        "New Born Applicability": "Lower",
        "New Born % Limit Applicable On": "Sum Insured"
    }
    
    # Extract Endorsement No. 12/12a section
    endorsement_12_match = re.search(r'Endt\.\s*No\.\s*12\s*(?:\(?a?\)?)?.*?(?=Endt\.\s*No\.|Endorsement\s*No\.|$)', text, re.IGNORECASE | re.DOTALL)
    
    if not endorsement_12_match:
        return newborn_data
    
    endorsement_12_text = endorsement_12_match.group(0)
    
    # Check if New Born is covered
    if re.search(r'new\s*born', endorsement_12_text, re.IGNORECASE) or \
       re.search(r'newborn', endorsement_12_text, re.IGNORECASE) or \
       re.search(r'new\s*Born', endorsement_12_text, re.IGNORECASE):
        
        newborn_data["New Born Covered?"] = "Yes"
        newborn_data["New Born Covered"] = "Yes"
        
        # Set default Covered From to "Day 0" as per instructions
        newborn_data["Covered From"] = "Day 0"
        
        # Check if New Born Limit is applicable
        if re.search(r'limit', endorsement_12_text, re.IGNORECASE) or \
           re.search(r'amount', endorsement_12_text, re.IGNORECASE) or \
           re.search(r'premium', endorsement_12_text, re.IGNORECASE) or \
           re.search(r'deposit', endorsement_12_text, re.IGNORECASE):
            newborn_data["Is New Born Limit Applicable"] = "Yes"
            
            # Set default Sum Insured dropdown to "Sum Insured"
            newborn_data["Sum Insured"] = "Sum Insured"
            newborn_data["New Born Sum Insured"] = "Sum Insured"
            
            # Set default % Limit Applicable On to "Sum Insured"
            newborn_data["% Limit Applicable On"] = "Sum Insured"
            newborn_data["New Born % Limit Applicable On"] = "Sum Insured"
            
            # Extract Sum Insured amount (from corporate floater or main policy)
            sum_insured_match = re.search(r'limit of Rs\.([\d,]+)/- as Corporate floater', text, re.IGNORECASE)
            if sum_insured_match:
                sum_insured = sum_insured_match.group(1).replace(",", "")
                # Store the numeric value for calculation
                newborn_data["_sum_insured_numeric"] = sum_insured
            
            # Extract New Born Limit Amount from Policy PDF
            newborn_limit_match = re.search(r'new\s*born.*?limit.*?Rs\.?([\d,]+)', endorsement_12_text, re.IGNORECASE)
            if newborn_limit_match:
                newborn_limit = newborn_limit_match.group(1).replace(",", "")
                newborn_data["Limit Amount"] = newborn_limit
                newborn_data["New Born Limit"] = newborn_limit
            else:
                # Look for general newborn amount
                newborn_amount_match = re.search(r'new\s*born.*?amount.*?Rs\.?([\d,]+)', endorsement_12_text, re.IGNORECASE)
                if newborn_amount_match:
                    newborn_amount = newborn_amount_match.group(1).replace(",", "")
                    newborn_data["Limit Amount"] = newborn_amount
                    newborn_data["New Born Limit"] = newborn_amount
                else:
                    # Look for any amount mentioned in newborn context
                    newborn_general_match = re.search(r'Rs\.?([\d,]+).*?new\s*born', endorsement_12_text, re.IGNORECASE)
                    if newborn_general_match:
                        newborn_amount = newborn_general_match.group(1).replace(",", "")
                        newborn_data["Limit Amount"] = newborn_amount
                        newborn_data["New Born Limit"] = newborn_amount
            
            # Calculate % Limit if both Sum Insured and New Born Limit are available
            if newborn_data.get("_sum_insured_numeric") and newborn_data.get("Limit Amount"):
                try:
                    sum_insured_val = int(newborn_data["_sum_insured_numeric"])
                    newborn_limit_val = int(newborn_data["Limit Amount"])
                    if newborn_limit_val > 0:
                        newborn_percentage = (sum_insured_val / newborn_limit_val) * 100
                        newborn_data["Limit Percentage"] = f"{newborn_percentage:.1f}"
                        newborn_data["New Born % Limit"] = f"{newborn_percentage:.1f}"
                except (ValueError, TypeError):
                    pass
            
            # Set default applicability to "Lower"
            newborn_data["Applicability"] = "Lower"
            newborn_data["New Born Applicability"] = "Lower"
        else:
            newborn_data["Is New Born Limit Applicable"] = "No"
    
    return newborn_data

def extract_pre_post_natal_from_endt_11b(text: str) -> Dict:
    """Extract Pre & Post Natal data from Endorsement 11b and Special Conditions"""
    pre_post_natal_data = {
        # Pre-Natal fields
        "Pre-Natal Benefit Applicable?": "No",
        "Pre-Natal Waiting Period": "0",
        "Pre-Natal Limit On Children": "2",
        "Pre-Natal Member Contribution": "No",
        "Pre-Natal Copay/Deductible": "No",
        "Pre-Natal Is Combined": "No",
        "Pre-Natal Sum Insured": "",
        "Pre-Natal % Limit": "",
        "Pre-Natal Limit": "",
        "Pre-Natal Applicability": "Lower",
        "Pre-Natal Copay": "",
        "Pre-Natal Deductible": "",
        "Pre-Natal Is Combined (2)": "No",
        "Pre-Natal No of Days": "30",
        "Pre-Natal % Limit Applicable On": "Sum Insured",
        
        # Post-Natal fields
        "Post-Natal Benefit Applicable?": "No",
        "Post-Natal Waiting Period": "0",
        "Post-Natal Limit On Children": "2",
        "Post-Natal Member Contribution": "No",
        "Post-Natal Copay/Deductible": "No",
        "Post-Natal Is Combined": "No",
        "Post-Natal Sum Insured": "",
        "Post-Natal % Limit": "",
        "Post-Natal Limit": "",
        "Post-Natal Applicability": "Lower",
        "Post-Natal Copay": "",
        "Post-Natal Deductible": "",
        "Post-Natal Is Combined (2)": "No",
        "Post-Natal No of Days": "60",
        "Post-Natal % Limit Applicable On": "Sum Insured",
        
        # Combined fields
        "Pre-Post-Natal Benefit Applicable?": "No",
        "Over-Above-Maternity Applicable?": "No",
        "Over-Above-Maternity Limit": ""
    }
    
    # Extract Endorsement No. 11b section
    endorsement_11b_match = re.search(r'Endt\.\s*No\.\s*11\s*\(?b?\)?.*?(?=Endt\.\s*No\.|Endorsement\s*No\.|$)', text, re.IGNORECASE | re.DOTALL)
    
    # Check for Pre & Post Natal in Special Conditions
    special_conditions_match = re.search(r'Special\s+Conditions.*?(?=Endorsement|Endt\.|$)', text, re.IGNORECASE | re.DOTALL)
    
    # Combine both sections for analysis
    analysis_text = ""
    if endorsement_11b_match:
        analysis_text += endorsement_11b_match.group(0) + " "
    if special_conditions_match:
        analysis_text += special_conditions_match.group(0) + " "
    
    if not analysis_text:
        return pre_post_natal_data
    
    # Check if Pre & Post Natal is applicable
    if re.search(r'pre.*?natal.*?post.*?natal', analysis_text, re.IGNORECASE) or \
       re.search(r'pre.*?post.*?natal', analysis_text, re.IGNORECASE) or \
       re.search(r'pre-natal.*?post-natal', analysis_text, re.IGNORECASE):
        
        pre_post_natal_data["Pre-Natal Benefit Applicable?"] = "Yes"
        pre_post_natal_data["Post-Natal Benefit Applicable?"] = "Yes"
        pre_post_natal_data["Pre-Post-Natal Benefit Applicable?"] = "Yes"
        
        # Check for Over & Above Maternity Limit
        if re.search(r'over.*?above.*?maternity.*?limit', analysis_text, re.IGNORECASE):
            pre_post_natal_data["Over-Above-Maternity Applicable?"] = "Yes"
            
            # Extract Over & Above Maternity Limit amount
            over_above_match = re.search(r'over.*?above.*?maternity.*?limit.*?Rs\.?([\d,]+)', analysis_text, re.IGNORECASE)
            if over_above_match:
                pre_post_natal_data["Over-Above-Maternity Limit"] = over_above_match.group(1).replace(",", "")
        
        # Set default values for Pre-Natal
        pre_post_natal_data["Pre-Natal No of Days"] = "30"
        pre_post_natal_data["Pre-Natal % Limit Applicable On"] = "Sum Insured"
        pre_post_natal_data["Pre-Natal Is Combined"] = "No"
        pre_post_natal_data["Pre-Natal Is Combined (2)"] = "No"
        
        # Set default values for Post-Natal
        pre_post_natal_data["Post-Natal No of Days"] = "60"
        pre_post_natal_data["Post-Natal % Limit Applicable On"] = "Sum Insured"
        pre_post_natal_data["Post-Natal Is Combined"] = "No"
        pre_post_natal_data["Post-Natal Is Combined (2)"] = "No"
        
        # Extract Sum Insured (from corporate floater or main policy)
        sum_insured_match = re.search(r'limit of Rs\.([\d,]+)/- as Corporate floater', text, re.IGNORECASE)
        if sum_insured_match:
            sum_insured = sum_insured_match.group(1).replace(",", "")
            pre_post_natal_data["Pre-Natal Sum Insured"] = sum_insured
            pre_post_natal_data["Post-Natal Sum Insured"] = sum_insured
        
        # Extract Maternity Limit for percentage calculation
        maternity_limit_match = re.search(r'limited to Rs\.([\d,]+)', analysis_text, re.IGNORECASE)
        if maternity_limit_match:
            maternity_limit = maternity_limit_match.group(1).replace(",", "")
            
            # Calculate % Limit for Pre-Natal
            if pre_post_natal_data["Pre-Natal Sum Insured"] and maternity_limit:
                try:
                    sum_insured_val = int(pre_post_natal_data["Pre-Natal Sum Insured"])
                    maternity_limit_val = int(maternity_limit)
                    if maternity_limit_val > 0:
                        pre_natal_percentage = (sum_insured_val / maternity_limit_val) * 100
                        pre_post_natal_data["Pre-Natal % Limit"] = f"{pre_natal_percentage:.1f}"
                except (ValueError, TypeError):
                    pass
            
            # Calculate % Limit for Post-Natal
            if pre_post_natal_data["Post-Natal Sum Insured"] and maternity_limit:
                try:
                    sum_insured_val = int(pre_post_natal_data["Post-Natal Sum Insured"])
                    maternity_limit_val = int(maternity_limit)
                    if maternity_limit_val > 0:
                        post_natal_percentage = (sum_insured_val / maternity_limit_val) * 100
                        pre_post_natal_data["Post-Natal % Limit"] = f"{post_natal_percentage:.1f}"
                except (ValueError, TypeError):
                    pass
        
        # Extract Pre & Post Natal Limit Amount from Policy PDF
        pre_post_limit_match = re.search(r'pre.*?post.*?natal.*?limit.*?Rs\.?([\d,]+)', analysis_text, re.IGNORECASE)
        if pre_post_limit_match:
            limit_amount = pre_post_limit_match.group(1).replace(",", "")
            pre_post_natal_data["Pre-Natal Limit"] = limit_amount
            pre_post_natal_data["Post-Natal Limit"] = limit_amount
        else:
            # Look for general sublimit
            sublimit_match = re.search(r'sublimit.*?Rs\.?([\d,]+)', analysis_text, re.IGNORECASE)
            if sublimit_match:
                limit_amount = sublimit_match.group(1).replace(",", "")
                pre_post_natal_data["Pre-Natal Limit"] = limit_amount
                pre_post_natal_data["Post-Natal Limit"] = limit_amount
        
        # Extract Copay and Deductible information
        copay_match = re.search(r'(\d+)%.*?admissible', analysis_text, re.IGNORECASE)
        if copay_match:
            copay_percentage = copay_match.group(1)
            pre_post_natal_data["Pre-Natal Copay"] = copay_percentage
            pre_post_natal_data["Post-Natal Copay"] = copay_percentage
            pre_post_natal_data["Pre-Natal Copay/Deductible"] = "Copay"
            pre_post_natal_data["Post-Natal Copay/Deductible"] = "Copay"
        
        deductible_match = re.search(r'deductible.*?Rs\.?([\d,]+)', analysis_text, re.IGNORECASE)
        if deductible_match:
            deductible_amount = deductible_match.group(1).replace(",", "")
            pre_post_natal_data["Pre-Natal Deductible"] = deductible_amount
            pre_post_natal_data["Post-Natal Deductible"] = deductible_amount
            pre_post_natal_data["Pre-Natal Copay/Deductible"] = "Deductible"
            pre_post_natal_data["Post-Natal Copay/Deductible"] = "Deductible"
        
        # Extract Member Contribution
        if re.search(r'member.*?contribution', analysis_text, re.IGNORECASE):
            pre_post_natal_data["Pre-Natal Member Contribution"] = "Yes"
            pre_post_natal_data["Post-Natal Member Contribution"] = "Yes"
        
        # Extract waiting period
        waiting_period_match = re.search(r'(\d+)\s*days\s*waiting\s*period', analysis_text, re.IGNORECASE)
        if waiting_period_match:
            waiting_period = waiting_period_match.group(1)
            pre_post_natal_data["Pre-Natal Waiting Period"] = waiting_period
            pre_post_natal_data["Post-Natal Waiting Period"] = waiting_period
        
        # Extract limit on number of children
        children_limit_match = re.search(r'first\s*(\d+)\s*children', analysis_text, re.IGNORECASE)
        if children_limit_match:
            children_limit = children_limit_match.group(1)
            pre_post_natal_data["Pre-Natal Limit On Children"] = children_limit
            pre_post_natal_data["Post-Natal Limit On Children"] = children_limit
    
    return pre_post_natal_data

def extract_maternity_from_endt_11b(text: str) -> Dict:
    """Extract maternity data specifically from Endorsement No. 11b"""
    maternity_data = {
        "Benefit Applicable?": "No",
        "Waiting Period(In Days)": "0",
        "Limit On Number Of Live Children": "2",
        "Member Contribution Applicable?": "No",
        "Copay or deductible Applicable?": "No",
        "Is Maternity Combined?": "No",
        "Sum Insured": "",
        "% Limit": "",
        "Limit": "",
        "Applicability": "Lower",
        "Copay": "",
        "Deductible": "",
        "Is Maternity Combined? (2)": "No"
    }
    
    # Extract Endorsement No. 11b section
    endorsement_11b_match = re.search(r'Endt\.\s*No\.\s*11\s*\(?b?\)?.*?(?=Endt\.\s*No\.|Endorsement\s*No\.|$)', text, re.IGNORECASE | re.DOTALL)
    
    if not endorsement_11b_match:
        return maternity_data
    
    endorsement_11b_text = endorsement_11b_match.group(0)
    
    # Check if maternity benefit is applicable
    if re.search(r'maternity', endorsement_11b_text, re.IGNORECASE):
        maternity_data["Benefit Applicable?"] = "Yes"
        
        # Set default waiting period to 0 as per instructions
        maternity_data["Waiting Period(In Days)"] = "0"
        
        # Set default limit on number of children to 2 as per instructions
        maternity_data["Limit On Number Of Live Children"] = "2"
        
        # Extract waiting period from policy if available
        waiting_period_match = re.search(r"(\d+)\s*days\s*waiting\s*period", endorsement_11b_text, re.IGNORECASE)
        if waiting_period_match:
            maternity_data["Waiting Period(In Days)"] = waiting_period_match.group(1)
        
        # Extract limit on number of children from policy if available
        children_limit_match = re.search(r"first\s*(\d+)\s*children", endorsement_11b_text, re.IGNORECASE)
        if children_limit_match:
            maternity_data["Limit On Number Of Live Children"] = children_limit_match.group(1)
        
        # Check for Member Contribution
        if re.search(r"member.*?contribution", endorsement_11b_text, re.IGNORECASE):
            maternity_data["Member Contribution Applicable?"] = "Yes"
            
            # Extract Copay or Deductible from Endorsement 11b
            if re.search(r"copay", endorsement_11b_text, re.IGNORECASE):
                maternity_data["Copay or deductible Applicable?"] = "Copay"
                # Extract copay percentage
                copay_match = re.search(r"(\d+)%.*?copay", endorsement_11b_text, re.IGNORECASE)
                if copay_match:
                    maternity_data["Copay"] = copay_match.group(1)
                else:
                    # Look for general copay percentage
                    general_copay_match = re.search(r"(\d+)%.*?admissible", endorsement_11b_text, re.IGNORECASE)
                    if general_copay_match:
                        maternity_data["Copay"] = general_copay_match.group(1)
            
            elif re.search(r"deductible", endorsement_11b_text, re.IGNORECASE):
                maternity_data["Copay or deductible Applicable?"] = "Deductible"
                # Extract deductible amount
                deductible_match = re.search(r"deductible.*?Rs\.?([\d,]+)", endorsement_11b_text, re.IGNORECASE)
                if deductible_match:
                    maternity_data["Deductible"] = deductible_match.group(1).replace(",", "")
                else:
                    # Look for general deductible
                    general_deductible_match = re.search(r"deductible.*?(\d+)", endorsement_11b_text, re.IGNORECASE)
                    if general_deductible_match:
                        maternity_data["Deductible"] = general_deductible_match.group(1)
        else:
            maternity_data["Member Contribution Applicable?"] = "No"
            maternity_data["Copay or deductible Applicable?"] = "No"
        
        # Check if Maternity is Combined
        if re.search(r"maternity.*?combined", endorsement_11b_text, re.IGNORECASE):
            maternity_data["Is Maternity Combined?"] = "Yes"
            maternity_data["Is Maternity Combined? (2)"] = "Yes"
        else:
            maternity_data["Is Maternity Combined?"] = "No"
            maternity_data["Is Maternity Combined? (2)"] = "No"
        
        # Extract Sum Insured
        sum_insured_match = re.search(r"sum\s+insured.*?Rs\.?([\d,]+)", endorsement_11b_text, re.IGNORECASE)
        if sum_insured_match:
            maternity_data["Sum Insured"] = sum_insured_match.group(1).replace(",", "")
        else:
            # Fallback to corporate floater
            corp_floater_match = re.search(r"limit of Rs\.([\d,]+)/- as Corporate floater", text, re.IGNORECASE)
            if corp_floater_match:
                maternity_data["Sum Insured"] = corp_floater_match.group(1).replace(",", "")
        
        # Set % Limit to "Sum Insured" as per instructions
        maternity_data["% Limit"] = "Sum Insured"
        
        # Extract Maternity Limit Amount from Policy PDF
        maternity_limit_match = re.search(r"maternity.*?limit.*?Rs\.?([\d,]+)", endorsement_11b_text, re.IGNORECASE)
        if maternity_limit_match:
            maternity_data["Limit"] = maternity_limit_match.group(1).replace(",", "")
        else:
            # Look for general maternity limit
            general_limit_match = re.search(r"limited to Rs\.([\d,]+)", endorsement_11b_text, re.IGNORECASE)
            if general_limit_match:
                maternity_data["Limit"] = general_limit_match.group(1).replace(",", "")
        
        # Set default applicability to "Lower"
        maternity_data["Applicability"] = "Lower"
        
        # Extract Copay and Deductible amounts if not already set
        if not maternity_data.get("Copay"):
            copay_match = re.search(r"(\d+)%.*?admissible", endorsement_11b_text, re.IGNORECASE)
            if copay_match:
                maternity_data["Copay"] = copay_match.group(1)
        
        if not maternity_data.get("Deductible"):
            deductible_match = re.search(r"deductible.*?Rs\.?([\d,]+)", endorsement_11b_text, re.IGNORECASE)
            if deductible_match:
                maternity_data["Deductible"] = deductible_match.group(1).replace(",", "")
            else:
                general_deductible_match = re.search(r"deductible.*?(\d+)", endorsement_11b_text, re.IGNORECASE)
                if general_deductible_match:
                    maternity_data["Deductible"] = general_deductible_match.group(1)
    
    return maternity_data

def extract_primary_data(text: str) -> List[Dict[str, str]]:
    """Extract Pre & Post Hospitalisation, Maternity, and OPD details"""
    
    data = {
        # Combined section
        "Benefit Applicable?": "",
        "Is Pre and Post Combined?": "",
        "Type Of Expense": "",
        "No. Of Days": "",
        "% Limit Applicable On": "",
        "% Limit": "",
        "Limit": "",
        "Applicability": "",
        
        # Pre Hospitalisation section
        "Type of expense 1": "",
        "No. Of Days 1": "",
        "% Limit Applicable 1": "",
        "Limit Percentage 1": "",
        "Limit Amount 1": "",
        "Applicability 1": "",
        
        # Post Hospitalisation or OPD section
        "Type of expense 2": "",
        "No. Of Days 2": "",
        "% Limit Applicable 2": "",
        "Limit Percentage 2": "",
        "Limit Amount 2": "",
        "Applicability 2": "",

        # Main Maternity fields
        "Maternity Benefit Applicable?": "",
        "Maternity Waiting Period(In Days)": "",
        "Maternity Limit On Number Of Live Children": "",
        "Maternity Member Contribution Applicable?": "",
        "Maternity Copay or deductible Applicable?": "",
        "Maternity Is Combined?": "",
        "Maternity Sum Insured": "",
        "Maternity % Limit": "",
        "Maternity Limit": "",
        "Maternity Applicability": "",
        "Maternity Copay": "",
        "Maternity Deductible": "",
        "Maternity Is Combined? (2)": "",
        
        # Pre-Natal specific fields
        "Pre-Natal Benefit Applicable?": "",
        "Pre-Natal Waiting Period": "",
        "Pre-Natal Limit On Children": "",
        "Pre-Natal Member Contribution": "",
        "Pre-Natal Copay/Deductible": "",
        "Pre-Natal Is Combined": "",
        "Pre-Natal Sum Insured": "",
        "Pre-Natal % Limit": "",
        "Pre-Natal Limit": "",
        "Pre-Natal Applicability": "",
        "Pre-Natal Copay": "",
        "Pre-Natal Deductible": "",
        "Pre-Natal Is Combined (2)": "",
        
        # Post-Natal specific fields
        "Post-Natal Benefit Applicable?": "",
        "Post-Natal Waiting Period": "",
        "Post-Natal Limit On Children": "",
        "Post-Natal Member Contribution": "",
        "Post-Natal Copay/Deductible": "",
        "Post-Natal Is Combined": "",
        "Post-Natal Sum Insured": "",
        "Post-Natal % Limit": "",
        "Post-Natal Limit": "",
        "Post-Natal Applicability": "",
        "Post-Natal Copay": "",
        "Post-Natal Deductible": "",
        "Post-Natal Is Combined (2)": "",
        
        # New Born specific fields
        "New Born Covered?": "",
        "New Born Covered": "",
        "New Born Sum Insured": "",
        "New Born % Limit": "",
        "New Born Limit": "",
        "New Born Applicability": "",
        "New Born % Limit Applicable On": "",
        
        # Additional fields that appear in the logic
        "Sum Insured": "",
        "Waiting Period(In Days)": "",
        "Over-Above-Maternity Limit": "",
        "Over-Above-Maternity Applicable?": "",
        "Member Contribution Applicable?": "",
        "Copay": "",
        "Deductible": "",
        "Is New Born Limit Applicable": "",
        "covered From": "",
        
        # Additional fields from the code logic
        "Maternity": "",
        "maternity_2": "",
        "limit": "",
        "limit_2": "",
        "limit amount": "",
        "Sum insured": "",
        "%limit": "",
        "%Limit": "",
        "%limit_2": "",
        "Limit Percentage": "",
        "No.of Days": "",
        "no.of Days": "",
        "No.of Days_2": "",
        "%Limit Applicable on": "",
        "%Limit Applicable on_2": "",
        "%Limit Applicable on_3": "",
        "%Limit applicable on": "",
        "applicability": "",
        "applicability_2": "",
        "applicability_3": "",
        "new born covered?": ""
    }

    # === Benefit Applicability Check ===
    # Default to "Yes" as per instructions
    data["Benefit Applicable?"] = "Yes"
    
    # Check if Pre and Post are combined
    if "Pre Hospitalisation Expenses" in text and "Post Hospitalisation Expenses" in text:
        # Check if they are mentioned as combined
        if re.search(r"pre.*?post.*?combined", text, re.IGNORECASE) or re.search(r"combined.*?pre.*?post", text, re.IGNORECASE):
            data["Is Pre and Post Combined?"] = "Yes"
            data["Type Of Expense"] = "Pre And Post Hospitalization Combined"
            # No. Of Days should not be filled as per instructions
            data["No. Of Days"] = ""
        else:
            data["Is Pre and Post Combined?"] = "No"
            data["Type Of Expense"] = "Pre Hospitalisation"
            # No. Of Days should not be filled as per instructions
            data["No. Of Days"] = ""
    else:
        data["Is Pre and Post Combined?"] = "No"
        data["Type Of Expense"] = "Pre Hospitalisation"
        # No. Of Days should not be filled as per instructions
        data["No. Of Days"] = ""

    # === Pre Hospitalisation ===
    pre_match = re.search(
        r"Pre Hospitalisation Expenses\s*Medical Expenses incurred during (\d+)\s*days",
        text, re.IGNORECASE
    )
    if pre_match:
        # Extract days from policy if available
        extracted_days = pre_match.group(1)
        if data["Is Pre and Post Combined?"] == "No":
            data["Type of expense 1"] = "Pre Hospitalization Expenses"
            data["No. Of Days 1"] = "30"  # Default 30 days as per instructions
            data["% Limit Applicable 1"] = "Sum Insured"  # Default as per instructions
            data["Applicability 1"] = "Lower"  # Default as per instructions
        else:
            data["Type of expense 1"] = "Pre Hospitalization Expenses"
            data["No. Of Days 1"] = extracted_days
            data["% Limit Applicable 1"] = "Sum Insured"
            data["Applicability 1"] = "Lower"

    # === Post Hospitalisation ===
    post_match = re.search(
        r"Post Hospitalisation Expenses\s*Medical Expenses incurred during (\d+)\s*days",
        text, re.IGNORECASE
    )
    if post_match:
        # Extract days from policy if available
        extracted_days = post_match.group(1)
        if data["Is Pre and Post Combined?"] == "No":
            data["Type of expense 2"] = "Post Hospitalization Expenses"
            data["No. Of Days 2"] = "60"  # Default 60 days as per instructions
            data["% Limit Applicable 2"] = "Sum Insured"  # Default as per instructions
            data["Applicability 2"] = "Lower"  # Default as per instructions
        else:
            data["Type of expense 2"] = "Post Hospitalization Expenses"
            data["No. Of Days 2"] = extracted_days
            data["% Limit Applicable 2"] = "Sum Insured"
            data["Applicability 2"] = "Lower"

    # Set defaults for Pre & Post Hospitalization when not combined
    if data["Is Pre and Post Combined?"] == "No":
        # Ensure Pre Hospitalization defaults are set
        if not data.get("Type of expense 1"):
            data["Type of expense 1"] = "Pre Hospitalization Expenses"
        if not data.get("No. Of Days 1"):
            data["No. Of Days 1"] = "30"
        if not data.get("% Limit Applicable 1"):
            data["% Limit Applicable 1"] = "Sum Insured"
        if not data.get("Applicability 1"):
            data["Applicability 1"] = "Lower"
            
        # Ensure Post Hospitalization defaults are set
        if not data.get("Type of expense 2"):
            data["Type of expense 2"] = "Post Hospitalization Expenses"
        if not data.get("No. Of Days 2"):
            data["No. Of Days 2"] = "60"
        if not data.get("% Limit Applicable 2"):
            data["% Limit Applicable 2"] = "Sum Insured"
        if not data.get("Applicability 2"):
            data["Applicability 2"] = "Lower"

    # === Pre & Post Natal OPD ===
    if "Pre-Natal and Post-Natal Expense is extended to be covered on Out-patient basis" in text:
        data["Type of expense 2"] = "Pre & Post Natal OPD"
        data["Applicability 2"] = "Lower"  # Default as per instructions

        opd_days = re.search(r"Pre-Natal.*?(\d+).*?days", text, re.IGNORECASE)
        data["No. Of Days 2"] = opd_days.group(1) if opd_days else "90"

        opd_perc = re.search(r"Pre-Natal.*?(\d+)%", text, re.IGNORECASE)
        data["Limit Percentage 2"] = opd_perc.group(1) if opd_perc else "100"

        data["% Limit Applicable 2"] = "Sum Insured"  # Default as per instructions

        opd_limit = re.search(r"sublimit of Rs\.?\s?([\d,]+)", text, re.IGNORECASE)
        if opd_limit:
            data["Limit Amount 2"] = opd_limit.group(1).replace(",", "")

    # === Maternity Limit ===
    maternity_limit = re.search(r"limited to Rs\.([\d,]+)", text, re.IGNORECASE)
    if maternity_limit:
        data["Limit"] = maternity_limit.group(1).replace(",", "")

    # === Co-payment % ===
    co_pay = re.search(r"(\d+)% of the admissible claim", text, re.IGNORECASE)
    if co_pay:
        data["% Limit"] = co_pay.group(1)
        data["% Limit Applicable On"] = "Sum Insured"  # Default as per instructions

    # === Corporate Floater ===
    corp_floater = re.search(r"limit of Rs\.([\d,]+)/- as Corporate floater", text, re.IGNORECASE)
    if corp_floater:
        data["Limit Amount 1"] = corp_floater.group(1).replace(",", "")

    # === Ambulance limit fallback ===
    ambulance = re.search(r"limit of Rs\.([\d,]+)/- per claim", text, re.IGNORECASE)
    if ambulance and not data["Limit Amount 1"]:
        data["Limit Amount 1"] = ambulance.group(1).replace(",", "")

    # === AYUSH treatment ===
    ayush = re.search(r"covered up to (\d+)% of the Sum Insured", text, re.IGNORECASE)
    if ayush:
        data["Limit Percentage 1"] = ayush.group(1)

    # === Specific disease limits ===
    disease = re.search(
        r"(\d+)% of the sum insured subject to a maximum of INR\.([\d,]+)/-",
        text, re.IGNORECASE
    )
    if disease:
        data["Limit Percentage 2"] = disease.group(1)
        data["Limit Amount 2"] = disease.group(2).replace(",", "")

    # === Fallback: generic % ===
    percentages = re.findall(r"(\d+)%", text)
    used = {data["% Limit"], data["Limit Percentage 1"], data["Limit Percentage 2"]}
    unused = [p for p in percentages if p not in used]
    if unused:
        data["% Limit Applicable 1"] = unused[0]

    # Set default % Limit Applicable On if not set
    if not data["% Limit Applicable On"]:
        data["% Limit Applicable On"] = "Sum Insured"  # Default as per instructions

    # Set default Applicability if not set
    if not data["Applicability"]:
        data["Applicability"] = "Lower"  # Default as per instructions

    # === Maternity Benefits from Endorsement 11b ===
    # Extract maternity data specifically from Endorsement No. 11b
    maternity_data = extract_maternity_from_endt_11b(text)
    
    # Update the main data dictionary with maternity data
    data.update(maternity_data)

    # === Pre & Post Natal Benefits from Endorsement 11b and Special Conditions ===
    # Extract Pre & Post Natal data specifically from Endorsement 11b and Special Conditions
    pre_post_natal_data = extract_pre_post_natal_from_endt_11b(text)
    
    # Update the main data dictionary with Pre & Post Natal data
    data.update(pre_post_natal_data)

    # Extract Maternity limit from Endorsement 11b
    maternity_limit_match = re.search(r"limited to Rs\.([\d,]+)", text, re.IGNORECASE)
    if maternity_limit_match:
        maternity_limit = int(maternity_limit_match.group(1).replace(",", ""))
        data["Maternity Limit"] = str(maternity_limit)
    
    # Extract Sum Insured (assuming from corporate floater or main policy)
    sum_insured_match = re.search(r"limit of Rs\.([\d,]+)/- as Corporate floater", text, re.IGNORECASE)
    if sum_insured_match:
        sum_insured = int(sum_insured_match.group(1).replace(",", ""))
        data["Maternity Sum Insured"] = str(sum_insured)
        data["Pre-Natal Sum Insured"] = str(sum_insured)
        data["Post-Natal Sum Insured"] = str(sum_insured)
        
    # Calculate % Limit for Pre-Natal only if both values exist
    if data["Maternity Sum Insured"] and data["Maternity Limit"]:
        sum_insured_val = int(data["Maternity Sum Insured"])
        maternity_limit_val = int(data["Maternity Limit"])
        if maternity_limit_val > 0:
            pre_natal_percentage = (sum_insured_val / maternity_limit_val) * 100
            data["Pre-Natal % Limit"] = f"{pre_natal_percentage:.1f}"

    # Calculate % Limit for Post-Natal only if both values exist
    if data["Maternity Sum Insured"] and data["Maternity Limit"]:
        sum_insured_val = int(data["Maternity Sum Insured"])
        maternity_limit_val = int(data["Maternity Limit"])
        if maternity_limit_val > 0:
            post_natal_percentage = (sum_insured_val / maternity_limit_val) * 100
            data["Post-Natal % Limit"] = f"{post_natal_percentage:.1f}"

    # Extract Pre & Post Natal sublimit from Special Conditions
    opd_sublimit_match = re.search(r"sublimit of Rs\.?\s?([\d,]+)", text, re.IGNORECASE)
    if opd_sublimit_match:
        opd_sublimit = int(opd_sublimit_match.group(1).replace(",", ""))
        data["Pre-Natal Limit"] = str(opd_sublimit)
        data["Post-Natal Limit"] = str(opd_sublimit)

    # Extract Co-payment information
    co_payment_matches = re.findall(r"(\d+)% of the admissible claim", text, re.IGNORECASE)
    if co_payment_matches:
        co_payment_percentage = co_payment_matches[0]
        data["Maternity Copay"] = co_payment_percentage
        data["Pre-Natal Copay"] = co_payment_percentage
        data["Post-Natal Copay"] = co_payment_percentage

    

    # Set applicability for Pre-Natal and Post-Natal
    if data["Pre-Natal Benefit Applicable?"] == "Yes":
        data["Pre-Natal Applicability"] = "Pre-Natal Expenses"
    if data["Post-Natal Benefit Applicable?"] == "Yes":
        data["Post-Natal Applicability"] = "Post-Natal Expenses"

    
    # Check for Pre & Post Natal in Special Conditions
    if "Pre and Post Natal OPD Expenses" in text:
        data["Pre-Natal Benefit Applicable?"] = "Yes"
        data["Post-Natal Benefit Applicable?"] = "Yes"
        data["Pre-Post-Natal Benefit Applicable?"] = "Yes"
        print("[OK] Pre & Post Natal OPD benefits found in Special Conditions")

    # Extract Sum Insured for Pre-Natal and Post-Natal
    sum_insured_match = re.search(r"limit of Rs\.([\d,]+)/- as Corporate floater", text, re.IGNORECASE)
    if sum_insured_match:
        sum_insured = int(sum_insured_match.group(1).replace(",", ""))
        data["Sum Insured"] = str(sum_insured)
        data["Pre-Natal % Limit Applicable On"] = "Sum Insured"
        data["Post-Natal % Limit Applicable On"] = "Sum Insured"
        data["Pre-Post-Natal % Limit Applicable On"] = "Sum Insured"
        print(f"[OK] Sum Insured: Rs. {sum_insured}")

    # Set % Limit as "Sum Insured" if no numeric value found
    if not data["% Limit"]:
        data["% Limit"] = "Sum Insured"
        print("[OK] % Limit set to 'Sum Insured' (no numeric value found)")

    # Set default applicability as "Lower"
    data["Applicability"] = "Lower"
    data["Pre-Natal Amount Applicability"] = "Lower"
    data["Post-Natal Amount Applicability"] = "Lower"
    data["Pre-Post-Natal Applicability"] = "Lower"

    # Extract Co-payment information
    co_payment_matches = re.findall(r"(\d+)% of the admissible claim", text, re.IGNORECASE)
    if co_payment_matches:
        co_payment_percentage = co_payment_matches[0]
        data["Copay"] = co_payment_percentage
        print(f"[OK] Co-payment: {co_payment_percentage}%")

    # Extract deductible information if present
    deductible_match = re.search(r"deductible.*?(\d+)", text, re.IGNORECASE)
    if deductible_match:
        data["Deductible"] = deductible_match.group(1)
        print(f"[OK] Deductible: {deductible_match.group(1)}")

    # Extract member contribution information
    member_contribution_match = re.search(r"member.*?contribution.*?(\d+)", text, re.IGNORECASE)
    if member_contribution_match:
        data["Member Contribution Applicable?"] = "Yes"
        print(f"[OK] Member contribution: {member_contribution_match.group(1)}%")

    # Set Pre & Post Natal defaults as per instructions
    if data["Pre-Natal Benefit Applicable?"] == "Yes":
        data["Pre-Natal No of Days"] = "30"  # Default 30 days
        data["Pre-Natal Is Combined"] = "No"  # Default No
        
        # Calculate % Limit for Pre-Natal
        if data["Sum Insured"] and data["Limit"]:
            sum_insured_val = int(data["Sum Insured"])
            maternity_limit_val = int(data["Limit"])
            if maternity_limit_val > 0:
                pre_natal_percentage = (sum_insured_val / maternity_limit_val) * 100
                data["Pre-Natal % Limit"] = f"{pre_natal_percentage:.1f}"
                print(f"[OK] Pre-Natal % Limit calculated: {pre_natal_percentage:.1f}%")

    if data["Post-Natal Benefit Applicable?"] == "Yes":
        data["Post-Natal No of Days"] = "60"  # Default 60 days
        data["Post-Natal Is Combined"] = "No"  # Default No
        
        # Calculate % Limit for Post-Natal
        if data["Sum Insured"] and data["Limit"]:
            sum_insured_val = int(data["Sum Insured"])
            maternity_limit_val = int(data["Limit"])
            if maternity_limit_val > 0:
                post_natal_percentage = (sum_insured_val / maternity_limit_val) * 100
                data["Post-Natal % Limit"] = f"{post_natal_percentage:.1f}"
                print(f"[OK] Post-Natal % Limit calculated: {post_natal_percentage:.1f}%")

    # Extract Pre & Post Natal sublimit from Special Conditions
    opd_sublimit_match = re.search(r"sublimit of Rs\.?\s?([\d,]+)", text, re.IGNORECASE)
    if opd_sublimit_match:
        opd_sublimit = int(opd_sublimit_match.group(1).replace(",", ""))
        data["Pre-Natal Limit"] = str(opd_sublimit)
        data["Post-Natal Limit"] = str(opd_sublimit)
        data["Pre-Post-Natal Limit"] = str(opd_sublimit)
        print(f"[OK] Pre & Post Natal OPD sublimit: Rs. {opd_sublimit}")

    # Set Pre & Post Natal Combined defaults - FIXED: Use .get() to safely check
    if data.get("Pre-Post-Natal Benefit Applicable?") == "Yes":
        data["Pre-Post-Natal Is Combined"] = "No"  # Default No
        data["Pre-Post-Natal Type Of Expense"] = "Pre And Post Natal Combined Expense"
        data["Pre-Post-Natal No. Of Days"] = "90"  # Default 90 days (30+60)
        
        # Calculate % Limit for Pre-Post-Natal Combined
        if data["Sum Insured"] and data["Limit"]:
            sum_insured_val = int(data["Sum Insured"])
            maternity_limit_val = int(data["Limit"])
            if maternity_limit_val > 0:
                combined_percentage = (sum_insured_val / maternity_limit_val) * 100
                data["Pre-Post-Natal % Limit"] = f"{combined_percentage:.1f}"
                print(f"[OK] Pre-Post-Natal Combined % Limit calculated: {combined_percentage:.1f}%")

    # Check for Over & Above Maternity Limit with better extraction
    if "over and above maternity limit" in text.lower():
        data["Over-Above-Maternity Applicable?"] = "Yes"
        # Try to extract the specific limit amount
        over_above_match = re.search(r"over.*?above.*?maternity.*?limit.*?Rs\.([\d,]+)", text, re.IGNORECASE)
        if over_above_match:
            over_above_limit = int(over_above_match.group(1).replace(",", ""))
            data["Over-Above-Maternity Limit"] = str(over_above_limit)
            print(f"[OK] Over & Above Maternity Limit: Rs. {over_above_limit}")
        else:
            print("[OK] Over & Above Maternity Limit applicable (amount not found)")

    # === New Born Benefits from Endorsement No. 12/12a ===
    # Extract New Born data specifically from Endorsement No. 12/12a
    newborn_data = extract_newborn_from_endt_12(text)
    
    # Update the main data dictionary with New Born data
    data.update(newborn_data)

    # Extract waiting period information
    waiting_period_match = re.search(r"(\d+)\s*days\s*waiting\s*period", text, re.IGNORECASE)
    if waiting_period_match:
        data["Waiting Period(In Days)"] = waiting_period_match.group(1)
        print(f"[OK] Waiting period: {waiting_period_match.group(1)} days")

    # Extract limit on number of children
    children_limit_match = re.search(r"first\s*(\d+)\s*children", text, re.IGNORECASE)
    if children_limit_match:
        data["Maternity Limit On Number Of Live Children"] = children_limit_match.group(1)
        data["Pre-Natal Limit On Children"] = children_limit_match.group(1)
        data["Post-Natal Limit On Children"] = children_limit_match.group(1)
        print(f"[OK] Limit on children: {children_limit_match.group(1)}")

    # Set member contribution and deductible applicability based on extracted data
    if data["Maternity Copay"] or data["Maternity Deductible"]:
        data["Maternity Copay or deductible Applicable?"] = "Yes"

    # Set maternity combined status
    data["Maternity Is Combined?"] = "No"  # Default as per instructions
    data["Maternity Is Combined? (2)"] = "No"

    if "Endt. No. 11 (b) Maternity Treatment Charges Benefit Extension" in text:
        data["Maternity Benefit Applicable?"] = "Yes"
        print("[OK] Maternity benefits found in Endorsement 11b")

    # Extract Maternity limit from Endorsement 11b
    maternity_limit_match = re.search(r"limited to Rs\.([\d,]+)", text, re.IGNORECASE)
    if maternity_limit_match:
        maternity_limit = int(maternity_limit_match.group(1).replace(",", ""))
        data["limit"] = str(maternity_limit)
        data["Limit"] = str(maternity_limit)
        data["limit_2"] = str(maternity_limit)
        data["limit amount"] = str(maternity_limit)

    sum_insured_match = re.search(r"limit of Rs\.([\d,]+)/- as Corporate floater", text, re.IGNORECASE)
    if sum_insured_match:
        sum_insured = int(sum_insured_match.group(1).replace(",", ""))
        data["Sum insured"] = str(sum_insured)
        print(f"[OK] Sum Insured: Rs. {sum_insured}")

    # Calculate % Limit for all sections if both values exist
    if data["Sum insured"] and data["limit"]:
        sum_insured_val = int(data["Sum insured"])
        maternity_limit_val = int(data["limit"])
        if maternity_limit_val > 0:
            percentage = (sum_insured_val / maternity_limit_val) * 100
            data["%limit"] = f"{percentage:.1f}"
            data["%Limit"] = f"{percentage:.1f}"
            data["%limit_2"] = f"{percentage:.1f}"
            data["Limit Percentage"] = f"{percentage:.1f}"
            print(f"[OK] % Limit calculated: {percentage:.1f}%")

    # Extract Pre & Post Natal sublimit from Special Conditions
    opd_sublimit_match = re.search(r"sublimit of Rs\.?\s?([\d,]+)", text, re.IGNORECASE)
    if opd_sublimit_match:
        opd_sublimit = int(opd_sublimit_match.group(1).replace(",", ""))
        data["limit amount"] = str(opd_sublimit)
        print(f"[OK] Pre & Post Natal OPD sublimit: Rs. {opd_sublimit}")

    # Extract Co-payment information
    co_payment_matches = re.findall(r"(\d+)% of the admissible claim", text, re.IGNORECASE)
    if co_payment_matches:
        co_payment_percentage = co_payment_matches[0]
        print(f"[OK] Co-payment: {co_payment_percentage}%")

    # Extract waiting period information
    waiting_period_match = re.search(r"(\d+)\s*days\s*waiting\s*period", text, re.IGNORECASE)
    if waiting_period_match:
        data["No.of Days"] = waiting_period_match.group(1)
        data["no.of Days"] = waiting_period_match.group(1)
        data["No.of Days_2"] = waiting_period_match.group(1)
        print(f"[OK] Waiting period: {waiting_period_match.group(1)} days")

    # Set default values for % Limit Applicable On
    data["%Limit Applicable on"] = "Sum Insured"
    data["%Limit Applicable on_2"] = "Sum Insured"
    data["%Limit Applicable on_3"] = "Sum Insured"
    data["%Limit applicable on"] = "Sum Insured"

    # Set default applicability
    data["Applicability"] = "Lower"
    data["applicability"] = "Lower"
    data["applicability_2"] = "Lower"
    data["applicability_3"] = "Lower"

    # Check for New Born coverage in Endorsement 12/12a
    if "Endt. No. 12" in text or "Endt. No. 12 (a)" in text:
        data["new born covered?"] = "Yes"
        data["Is New Born Limit Applicable"] = "Yes"
        print("[OK] New Born coverage found in Endorsement 12/12a")

    # Set default values for New Born
    data["covered From"] = "Day 0"

    # Extract New Born limit if present
    newborn_limit_match = re.search(r"new born.*?limit.*?Rs\.([\d,]+)", text, re.IGNORECASE)
    if newborn_limit_match:
        newborn_limit = int(newborn_limit_match.group(1).replace(",", ""))
        data["limit amount"] = str(newborn_limit)
        print(f"[OK] New Born limit: Rs. {newborn_limit}")

    

    return [data]