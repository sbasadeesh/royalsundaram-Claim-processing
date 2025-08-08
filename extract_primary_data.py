import re
from typing import List, Dict

Newborn_sum_insured = ""
Newborn_Limit_applicable_on = ""
Newborn_Limit_percentage = ""
Newborn_Limit_amount = ""
Newborn_applicability = ""

def extract_newborn_from_endt_12(text: str) -> Dict:
    """Extract New Born data specifically from Endorsement No. 12/12a"""
    newborn_data = {
        "New Born Covered?": "No",
        "New Born Covered": "No",
        "Covered From": "0",
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
        newborn_data["Covered From"] = "0"
        
        # Check if New Born Limit is applicable
        if re.search(r'limit', endorsement_12_text, re.IGNORECASE) or \
           re.search(r'amount', endorsement_12_text, re.IGNORECASE) or \
           re.search(r'premium', endorsement_12_text, re.IGNORECASE) or \
           re.search(r'deposit', endorsement_12_text, re.IGNORECASE):
            newborn_data["Is New Born Limit Applicable"] = "No"
            
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
    """Extract maternity data specifically from Endorsement No. 11(b)"""
    maternity_data = {
        "Benefit Applicable?": "No",
        "Waiting Period (In Days)": "0",
        "Limit On Number Of Live Children": "2",
        "Member Contribution Applicable?": "No",
        "Copay or deductible Applicable?": "No",
        "Is Maternity Combined?": "No",
        "Sum Insured": "",
        "% Limit": "Sum Insured",
        "Limit": "",
        "Applicability": "Lower",
        "Copay": "",
        "Deductible": ""
    }
    
    # Extract Endorsement No. 11(b) section specifically
    endorsement_11b_match = re.search(r'Endt\.\s*No\.\s*11\s*\(b\)\s*Maternity Treatment Charges Benefit Extension.*?(?=Endt\.\s*No\.|Endorsement\s*No\.|Group Health Policy|$)', text, re.IGNORECASE | re.DOTALL)
    
    if not endorsement_11b_match:
        print("[EMPTY] Endt. No. 11(b) section not found")
        return maternity_data
    
    endorsement_11b_text = endorsement_11b_match.group(0)
    print("[OK] Endt. No. 11(b) section found")
    
    # Check if maternity benefit is applicable (Endt. No. 11(b) exists)
    if "Endt. No. 11 (b) Maternity Treatment Charges Benefit Extension" in text:
        maternity_data["Benefit Applicable?"] = "Yes"
        print("[OK] Maternity benefit applicable")
        
        # Set default waiting period to 0 as per instructions
        maternity_data["Waiting Period (In Days)"] = "0"
        print("[OK] Waiting period set to 0 (default)")
        
        # Set default limit on number of children to 2 as per instructions
        maternity_data["Limit On Number Of Live Children"] = "2"
        print("[OK] Limit on number of live children set to 2 (default)")
        
        # Extract limit on number of children from policy if available
        children_limit_match = re.search(r"first\s*(\d+)\s*children", endorsement_11b_text, re.IGNORECASE)
        if children_limit_match:
            maternity_data["Limit On Number Of Live Children"] = children_limit_match.group(1)
            print(f"[OK] Limit on children updated to: {children_limit_match.group(1)}")
        
        # Check for Member Contribution
        if re.search(r"member.*?contribution", endorsement_11b_text, re.IGNORECASE):
            maternity_data["Member Contribution Applicable?"] = "Yes"
            print("[OK] Member contribution applicable")
            
            # Extract Copay or Deductible from Endorsement 11b
            if re.search(r"copay", endorsement_11b_text, re.IGNORECASE):
                maternity_data["Copay or deductible Applicable?"] = "Copay"
                print("[OK] Copay applicable")
                # Extract copay percentage
                copay_match = re.search(r"(\d+)%.*?copay", endorsement_11b_text, re.IGNORECASE)
                if copay_match:
                    maternity_data["Copay"] = copay_match.group(1)
                    print(f"[OK] Copay percentage: {copay_match.group(1)}%")
                else:
                    # Look for general copay percentage
                    general_copay_match = re.search(r"(\d+)%.*?admissible", endorsement_11b_text, re.IGNORECASE)
                    if general_copay_match:
                        maternity_data["Copay"] = general_copay_match.group(1)
                        print(f"[OK] Copay percentage (general): {general_copay_match.group(1)}%")
            
            elif re.search(r"deductible", endorsement_11b_text, re.IGNORECASE):
                maternity_data["Copay or deductible Applicable?"] = "Deductible"
                print("[OK] Deductible applicable")
                # Extract deductible amount
                deductible_match = re.search(r"deductible.*?Rs\.?([\d,]+)", endorsement_11b_text, re.IGNORECASE)
                if deductible_match:
                    maternity_data["Deductible"] = deductible_match.group(1).replace(",", "")
                    print(f"[OK] Deductible amount: Rs. {deductible_match.group(1)}")
                else:
                    # Look for general deductible
                    general_deductible_match = re.search(r"deductible.*?(\d+)", endorsement_11b_text, re.IGNORECASE)
                    if general_deductible_match:
                        maternity_data["Deductible"] = general_deductible_match.group(1)
                        print(f"[OK] Deductible amount (general): Rs. {general_deductible_match.group(1)}")
        else:
            maternity_data["Member Contribution Applicable?"] = "No"
            maternity_data["Copay or deductible Applicable?"] = "No"
            print("[OK] Member contribution not applicable")
        
        # Check if Maternity is Combined
        if re.search(r"maternity.*?combined", endorsement_11b_text, re.IGNORECASE):
            maternity_data["Is Maternity Combined?"] = "Yes"
            print("[OK] Maternity is combined")
        else:
            maternity_data["Is Maternity Combined?"] = "No"
            print("[OK] Maternity is not combined")
        
        # Extract Sum Insured if maternity is combined
        if maternity_data["Is Maternity Combined?"] == "Yes":
            sum_insured_match = re.search(r"sum\s+insured.*?Rs\.?([\d,]+)", endorsement_11b_text, re.IGNORECASE)
            if sum_insured_match:
                maternity_data["Sum Insured"] = sum_insured_match.group(1).replace(",", "")
                print(f"[OK] Sum Insured: Rs. {sum_insured_match.group(1)}")
            else:
                # Fallback to corporate floater
                corp_floater_match = re.search(r"limit of Rs\.([\d,]+)/- as Corporate floater", text, re.IGNORECASE)
                if corp_floater_match:
                    maternity_data["Sum Insured"] = corp_floater_match.group(1).replace(",", "")
                    print(f"[OK] Sum Insured (corporate floater): Rs. {corp_floater_match.group(1)}")
        
        # Set % Limit to "Sum Insured" as per instructions
        maternity_data["% Limit"] = "Sum Insured"
        print("[OK] % Limit set to 'Sum Insured'")
        
        # Extract Maternity Limit Amount from Policy PDF under Maternity amount
        maternity_limit_match = re.search(r"limited to Rs\.([\d,]+)", endorsement_11b_text, re.IGNORECASE)
        if maternity_limit_match:
            maternity_data["Limit"] = maternity_limit_match.group(1).replace(",", "")
            print(f"[OK] Maternity limit amount: Rs. {maternity_limit_match.group(1)}")
        else:
            # Look for alternative maternity limit patterns
            alt_limit_match = re.search(r"maternity.*?limit.*?Rs\.?([\d,]+)", endorsement_11b_text, re.IGNORECASE)
            if alt_limit_match:
                maternity_data["Limit"] = alt_limit_match.group(1).replace(",", "")
                print(f"[OK] Maternity limit amount (alternative): Rs. {alt_limit_match.group(1)}")
            else:
                print("[EMPTY] Maternity limit amount not found")
        
        # Set default applicability to "Lower"
        maternity_data["Applicability"] = "Lower"
        print("[OK] Applicability set to 'Lower'")
        
        # Extract Copay and Deductible amounts if not already set
        if not maternity_data.get("Copay"):
            copay_match = re.search(r"(\d+)%.*?admissible", endorsement_11b_text, re.IGNORECASE)
            if copay_match:
                maternity_data["Copay"] = copay_match.group(1)
                print(f"[OK] Copay percentage: {copay_match.group(1)}%")
        
        if not maternity_data.get("Deductible"):
            deductible_match = re.search(r"deductible.*?Rs\.?([\d,]+)", endorsement_11b_text, re.IGNORECASE)
            if deductible_match:
                maternity_data["Deductible"] = deductible_match.group(1).replace(",", "")
                print(f"[OK] Deductible amount: Rs. {deductible_match.group(1)}")
            else:
                general_deductible_match = re.search(r"deductible.*?(\d+)", endorsement_11b_text, re.IGNORECASE)
                if general_deductible_match:
                    maternity_data["Deductible"] = general_deductible_match.group(1)
                    print(f"[OK] Deductible amount (general): Rs. {general_deductible_match.group(1)}")
    else:
        print("[EMPTY] Maternity benefit not applicable")
    
    return maternity_data

def extract_primary_data(text: str) -> List[Dict[str, str]]:
    """Extract Pre & Post Hospitalisation, Maternity, and OPD details"""
    
    data = {
        # === DYNAMIC COMBINED SECTION - BASED ON SPECIAL CLAUSES ===
        "Combined_Benefit_Applicable": "",
        "Combined_Is_Pre_and_Post_Combined": "No",
        "Combined_Type_Of_Expense": "",
        "Combined_No_Of_Days": "",
        "Combined_Percent_Limit_Applicable_On": "",
        "Combined_Percent_Limit": "",
        "Combined_Limit": "",
        "Combined_Applicability": "",
        # === END OF HARDCODED COMBINED SECTION ===
        
        # === DYNAMIC PRE HOSPITALISATION SECTION - BASED ON SPECIAL CLAUSES ===
        "Type of expense 1": "",
        "No. Of Days 1": "",
        "% Limit Applicable 1": "",
        "Limit Percentage 1": "",
        "Limit Amount 1": "",
        "Applicability 1": "",
        # === END OF DYNAMIC PRE HOSPITALISATION SECTION ===
        
        # === DYNAMIC POST HOSPITALISATION SECTION - BASED ON SPECIAL CLAUSES ===
        "Type of expense 2": "",
        "No. Of Days 2": "",
        "% Limit Applicable 2": "",
        "Limit Percentage 2": "",
        "Limit Amount 2": "",
        "Applicability 2": "",
        # === END OF HARDCODED POST HOSPITALISATION SECTION ===

        # === HARDCODED MATERNITY SECTION - THESE VALUES WILL ALWAYS BE THE SAME ===
        "Maternity Benefit Applicable?": "",
        "Maternity Waiting Period(In Days)": "0",
        "Maternity Limit On Number Of Live Children": "",
        "Maternity Member Contribution Applicable?": "No",
        "Maternity Copay or deductible Applicable?": "",
        "Maternity Is Combined?": "No",
        "Maternity Sum Insured": "",
        "Maternity % Limit": "",
        "Maternity Limit": "",
        "Maternity Applicability": "",
        "Maternity Copay": "",
        "Maternity Deductible": "",
        "Maternity Is Combined? (2)": "",
        # === END OF HARDCODED MATERNITY SECTION ===
        
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

    # NOTE: The Combined section values are now DYNAMIC and will be modified by the logic below
    # "Combined_Benefit_Applicable": "Yes" if "Special Clauses:" found in text, else "No"
    # "Combined_Is_Pre_and_Post_Combined": "No" - Always No  
    # "Combined_Type_Of_Expense": "" - Always empty
    # "Combined_No_Of_Days": "" - Always empty
    # "Combined_Percent_Limit_Applicable_On": "" - Always empty
    # "Combined_Percent_Limit": "" - Always empty
    # "Combined_Limit": "" - Always empty
    # "Combined_Applicability": "" - Always empty

    # === DYNAMIC LOGIC FOR COMBINED_BENEFIT_APPLICABLE ===
    # Check if Special Clauses or Value Added Services section exists and contains relevant content
    special_clauses_match = re.search(r'Special\s+Clauses:\s*(.*?)(?=Endorsement|Endt\.|Group Health Policy|$)', text, re.IGNORECASE | re.DOTALL)
    value_added_services_match = re.search(r'Value\s+Added\s+Services:\s*(.*?)(?=Endorsement|Endt\.|Group Health Policy|$)', text, re.IGNORECASE | re.DOTALL)
    
    print(f"[DEBUG] Special Clauses found: {special_clauses_match is not None}")
    print(f"[DEBUG] Value Added Services found: {value_added_services_match is not None}")
    
    # Initialize flag to track if relevant content is found
    relevant_content_found = False
    
    # Check Special Clauses first
    if special_clauses_match:
        special_clauses_text = special_clauses_match.group(1).strip()
        print(f"[DEBUG] Special Clauses text: {special_clauses_text[:200]}...")
        
        # Check if Special Clauses contains relevant content for combined benefits
        pre_found = re.search(r'Pre\s+Hospitalisation\s+Expenses', special_clauses_text, re.IGNORECASE)
        post_found = re.search(r'Post\s+Hospitalisation\s+Expenses', special_clauses_text, re.IGNORECASE)
        
        if pre_found or post_found:
            data["Combined_Benefit_Applicable"] = "Yes"
            relevant_content_found = True
            print("[OK] Combined_Benefit_Applicable set to 'Yes' - relevant content found in Special Clauses")
        else:
            print("[INFO] Special Clauses found but no relevant content")
    
    # Check Value Added Services if Special Clauses didn't have relevant content
    if not relevant_content_found and value_added_services_match:
        value_added_services_text = value_added_services_match.group(1).strip()
        print(f"[DEBUG] Value Added Services text: {value_added_services_text[:200]}...")
        
        # Check if Value Added Services contains relevant content for combined benefits
        pre_found = re.search(r'Pre\s+Hospitalisation\s+Expenses', value_added_services_text, re.IGNORECASE)
        post_found = re.search(r'Post\s+Hospitalisation\s+Expenses', value_added_services_text, re.IGNORECASE)
        
        if pre_found or post_found:
            data["Combined_Benefit_Applicable"] = "Yes"
            relevant_content_found = True
            print("[OK] Combined_Benefit_Applicable set to 'Yes' - relevant content found in Value Added Services")
        else:
            print("[INFO] Value Added Services found but no relevant content")
    
    # Set to No if no relevant content found in either section
    if not relevant_content_found:
        data["Combined_Benefit_Applicable"] = "No"
        print("[INFO] Combined_Benefit_Applicable set to 'No' - no relevant content found in Special Clauses or Value Added Services")

    # === DYNAMIC LOGIC FOR PRE & POST HOSPITALISATION FIELDS ===
    # Check if Special Clauses section exists and contains relevant content
    if special_clauses_match:
        special_clauses_text = special_clauses_match.group(1).strip()
        
        # Check for Pre Hospitalisation Expenses
        if re.search(r'Pre\s+Hospitalisation\s+Expenses', special_clauses_text, re.IGNORECASE):
            data["Type of expense 1"] = "Pre Hospitalisation Expense"
            
            # Extract number of days from Pre Hospitalisation text
            pre_days_match = re.search(r'(\d+)\s*days?\s*preceding', special_clauses_text, re.IGNORECASE)
            if pre_days_match:
                data["No. Of Days 1"] = pre_days_match.group(1)
                print(f"[OK] Pre Hospitalisation days extracted: {pre_days_match.group(1)}")
            else:
                data["No. Of Days 1"] = "30"  # Default fallback
                print("[INFO] Pre Hospitalisation days not found, using default: 30")
            
            data["% Limit Applicable 1"] = "Sum Insured"
            data["Limit Percentage 1"] = "100"
            data["Applicability 1"] = "Lower"
            print("[OK] Pre Hospitalisation fields populated from Special Clauses")
        
        # Check for Post Hospitalisation Expenses
        if re.search(r'Post\s+Hospitalisation\s+Expenses', special_clauses_text, re.IGNORECASE):
            data["Type of expense 2"] = "Post Hospitalisation Expense"
            
            # Extract number of days from Post Hospitalisation text
            post_days_match = re.search(r'(\d+)\s*days?\s*immediately\s*after', special_clauses_text, re.IGNORECASE)
            if post_days_match:
                data["No. Of Days 2"] = post_days_match.group(1)
                print(f"[OK] Post Hospitalisation days extracted: {post_days_match.group(1)}")
            else:
                data["No. Of Days 2"] = "60"  # Default fallback
                print("[INFO] Post Hospitalisation days not found, using default: 60")
            
            data["% Limit Applicable 2"] = "Sum Insured"
            data["Limit Percentage 2"] = "100"
            data["Applicability 2"] = "Lower"
            print("[OK] Post Hospitalisation fields populated from Special Clauses")

    # Check if Pre and Post are combined (this logic is preserved but won't affect the hardcoded combined section)
    if "Pre Hospitalisation Expenses" in text and "Post Hospitalisation Expenses" in text:
        # Check if they are mentioned as combined (but won't change the hardcoded "Combined_Is_Pre_and_Post_Combined" value)
        if re.search(r"pre.*?post.*?combined", text, re.IGNORECASE) or re.search(r"combined.*?pre.*?post", text, re.IGNORECASE):
            # The hardcoded value "No" will remain unchanged
            pass
        else:
            # The hardcoded value "No" will remain unchanged
            pass
    else:
        # The hardcoded value "No" will remain unchanged
        pass

    # === Pre Hospitalisation ===
    # NOTE: Pre Hospitalisation section values are now DYNAMIC and will be populated only if found in Special Clauses
    # "Type of expense 1": "Pre Hospitalisation Expense" - Only if Pre Hospitalisation Expenses found in Special Clauses
    # "No. Of Days 1": "30" - Only if Pre Hospitalisation Expenses found in Special Clauses
    # "% Limit Applicable 1": "Sum Insured" - Only if Pre Hospitalisation Expenses found in Special Clauses
    # "Limit Percentage 1": "100" - Only if Pre Hospitalisation Expenses found in Special Clauses
    # "Applicability 1": "Lower" - Only if Pre Hospitalisation Expenses found in Special Clauses

    # NOTE: Post Hospitalisation section values are now DYNAMIC and will be populated only if found in Special Clauses
    # "Type of expense 2": "Post Hospitalisation Expense" - Only if Post Hospitalisation Expenses found in Special Clauses
    # "No. Of Days 2": "60" - Only if Post Hospitalisation Expenses found in Special Clauses
    # "% Limit Applicable 2": "Sum Insured" - Only if Post Hospitalisation Expenses found in Special Clauses
    # "Limit Percentage 2": "100" - Only if Post Hospitalisation Expenses found in Special Clauses
    # "Applicability 2": "Lower" - Only if Post Hospitalisation Expenses found in Special Clauses

    # NOTE: Both Pre Hospitalisation and Post Hospitalisation section values are now DYNAMIC and will only be populated if found in Special Clauses

    # NOTE: Post Hospitalisation section values are now DYNAMIC and will only be populated if found in Special Clauses
    # === Pre & Post Natal OPD ===
    if "Pre-Natal and Post-Natal Expense is extended to be covered on Out-patient basis" in text:
        # Note: Post Hospitalisation fields are hardcoded and will not be updated here
        # Only Limit Amount 2 can be updated for OPD sublimit
        opd_limit = re.search(r"sublimit of Rs\.?\s?([\d,]+)", text, re.IGNORECASE)
        if opd_limit:
            data["Limit Amount 2"] = opd_limit.group(1).replace(",", "")

    # === Maternity Limit ===
    maternity_limit = re.search(r"limited to Rs\.([\d,]+)", text, re.IGNORECASE)
    if maternity_limit:
        # Note: This will NOT affect the hardcoded "Combined_Limit" field in Combined section
        pass

    # === Co-payment % ===
    co_pay = re.search(r"(\d+)% of the admissible claim", text, re.IGNORECASE)
    if co_pay:
        # Note: This will NOT affect the hardcoded "Combined_Percent_Limit" field in Combined section
        pass

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

    # NOTE: Post Hospitalisation "Limit Percentage 2" is hardcoded to "100" and will not be modified by any logic
    # === Specific disease limits ===
    disease = re.search(
        r"(\d+)% of the sum insured subject to a maximum of INR\.([\d,]+)/-",
        text, re.IGNORECASE
    )
    if disease:
        # Note: Post Hospitalisation "Limit Percentage 2" is hardcoded and will not be updated here
        # Only Limit Amount 2 can be updated for disease limits
        data["Limit Amount 2"] = disease.group(2).replace(",", "")

    # NOTE: Pre Hospitalisation "% Limit Applicable 1" is hardcoded to "Sum Insured" and will not be modified by any logic
    # === Fallback: generic % ===
    percentages = re.findall(r"(\d+)%", text)
    used = {data.get("Limit Percentage 1"), data.get("Limit Percentage 2")}
    unused = [p for p in percentages if p not in used]
    # Removed logic that was updating "% Limit Applicable 1" as it's now hardcoded

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
    # First check for Normal delivery and Caesarean amounts
    maternity_limit_match = re.search(r"limited to Rs\.([\d,]+)/-.*?Normal\s+delivery.*?([\d,]+)/-.*?Caesarean", text, re.IGNORECASE | re.DOTALL)
    if not maternity_limit_match:
        # Alternative pattern for different text formats
        maternity_limit_match = re.search(r"maximum.*?benefit.*?limited.*?Rs\.([\d,]+)/-.*?Normal\s+delivery.*?([\d,]+)/-.*?Caesarean", text, re.IGNORECASE | re.DOTALL)
    
    if maternity_limit_match:
        normal_amount = int(maternity_limit_match.group(1).replace(",", ""))
        caesarean_amount = int(maternity_limit_match.group(2).replace(",", ""))
        # Use the higher amount as the maternity limit
        maternity_limit = max(normal_amount, caesarean_amount)
        data["Maternity Limit"] = str(maternity_limit)
        print(f"[OK] Maternity limit extracted - Normal: Rs. {normal_amount}, Caesarean: Rs. {caesarean_amount}, Using: Rs. {maternity_limit}")
    else:
        # Fallback to standard single amount pattern
        maternity_limit_match = re.search(r"limited to Rs\.([\d,]+)", text, re.IGNORECASE)
        if maternity_limit_match:
            maternity_limit = int(maternity_limit_match.group(1).replace(",", ""))
            data["Maternity Limit"] = str(maternity_limit)
            print(f"[OK] Maternity limit extracted (single amount): Rs. {maternity_limit}")
    
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
        if data["Sum Insured"] and data.get("Limit"):
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
        if data["Sum Insured"] and data.get("Limit"):
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
        if data["Sum Insured"] and data.get("Limit"):
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

    # Extract limit on number of children using improved regex
    children_limit_match = re.search(r"first\s+(one|two|1|2)\s+children?", text, re.IGNORECASE)
    if children_limit_match:
        value = children_limit_match.group(1).lower()
        if value in ["two", "2"]:
            count = 2
        elif value in ["one", "1"]:
            count = 1
        else:
            count = 0
        
        data["Maternity Limit On Number Of Live Children"] = str(count)
        data["Pre-Natal Limit On Children"] = str(count)
        data["Post-Natal Limit On Children"] = str(count)
        print(f"[OK] Limit on children: {count}")
    else:
        # Default to 0 if no match found
        data["Maternity Limit On Number Of Live Children"] = "0"
        data["Pre-Natal Limit On Children"] = "0"
        data["Post-Natal Limit On Children"] = "0"
        print("[INFO] No children limit found, defaulting to 0")

    # NOTE: Maternity Copay or deductible Applicable? is left empty and will not be automatically set

    # NOTE: Maternity Is Combined? is hardcoded to "No" and will not be modified by any logic

    # Check for maternity benefits in various forms
    maternity_found = False
    
    # Check for specific endorsement
    if "Endt. No. 11 (b) Maternity Treatment Charges Benefit Extension" in text:
        data["Maternity Benefit Applicable?"] = "Yes"
        maternity_found = True
        print("[OK] Maternity benefits found in Endorsement 11b")
    
    # Check for other maternity-related content
    if re.search(r"maternity", text, re.IGNORECASE) or re.search(r"maternal", text, re.IGNORECASE):
        if not maternity_found:
            data["Maternity Benefit Applicable?"] = "Yes"
            maternity_found = True
            print("[OK] Maternity benefits found in text")
    
    # Check for maternity limits or coverage
    if re.search(r"maternity.*?limit", text, re.IGNORECASE) or re.search(r"maternity.*?coverage", text, re.IGNORECASE):
        if not maternity_found:
            data["Maternity Benefit Applicable?"] = "Yes"
            maternity_found = True
            print("[OK] Maternity coverage/limits found in text")

    # Extract Maternity limit from Endorsement 11b
    maternity_limit_match = re.search(r"limited to Rs\.([\d,]+)", text, re.IGNORECASE)
    if maternity_limit_match:
        maternity_limit = int(maternity_limit_match.group(1).replace(",", ""))
        data["limit"] = str(maternity_limit)
        data["limit_2"] = str(maternity_limit)
        data["limit amount"] = str(maternity_limit)

    sum_insured_match = re.search(r"limit of Rs\.([\d,]+)/- as Corporate floater", text, re.IGNORECASE)
    if sum_insured_match:
        sum_insured = int(sum_insured_match.group(1).replace(",", ""))
        data["Sum insured"] = str(sum_insured)
        print(f"[OK] Sum Insured: Rs. {sum_insured}")

    # Calculate % Limit for other sections if both values exist (not combined section)
    if data["Sum insured"] and data["limit"]:
        sum_insured_val = int(data["Sum insured"])
        maternity_limit_val = int(data["limit"])
        if maternity_limit_val > 0:
            # percentage = (sum_insured_val / maternity_limit_val) * 100
            percentage = 100
            data["%limit"] = f"{percentage:.1f}"
            # Note: Combined section "% Limit" is hardcoded and not updated here
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

    # Set default values for % Limit Applicable On (for other sections, not combined section)
    data["%Limit Applicable on"] = "Sum Insured"
    data["%Limit Applicable on_2"] = "Sum Insured"
    data["%Limit Applicable on_3"] = "Sum Insured"
    data["%Limit applicable on"] = "Sum Insured"

    # Set default applicability (for other sections, not combined section)
    data["applicability"] = "Lower"
    data["applicability_2"] = "Lower"
    data["applicability_3"] = "Lower"

    # Check for New Born coverage in Endorsement 12/12a
    if "Endt. No. 12" in text or "Endt. No. 12 (a)" in text:
        data["new born covered?"] = "Yes"
        data["Is New Born Limit Applicable"] = "No"
        print("[OK] New Born coverage found in Endorsement 12/12a")

    # Set default values for New Born
    data["covered From"] = "0"

    # Extract New Born limit if present
    newborn_limit_match = re.search(r"new born.*?limit.*?Rs\.([\d,]+)", text, re.IGNORECASE)
    if newborn_limit_match:
        newborn_limit = int(newborn_limit_match.group(1).replace(",", ""))
        data["limit amount"] = str(newborn_limit)
        print(f"[OK] New Born limit: Rs. {newborn_limit}")

    # Set default values for Benefit Applicable fields if not found
    if not data.get("Maternity Benefit Applicable?"):
        data["Maternity Benefit Applicable?"] = "No"
        print("[INFO] Maternity Benefit Applicable set to 'No' (no maternity benefits found in text)")
    
    if not data.get("Pre-Natal Benefit Applicable?"):
        data["Pre-Natal Benefit Applicable?"] = "No"
        print("[INFO] Pre-Natal Benefit Applicable set to 'No' (not found in text)")
    
    if not data.get("Post-Natal Benefit Applicable?"):
        data["Post-Natal Benefit Applicable?"] = "No"
        print("[INFO] Post-Natal Benefit Applicable set to 'No' (not found in text)")

    # Clear ALL maternity fields if Maternity Benefit Applicable is "No"
    if data.get("Maternity Benefit Applicable?") == "No":
        print("[INFO] Clearing ALL maternity fields as Maternity Benefit Applicable is 'No'")
        # Clear ALL maternity fields including hardcoded ones
        data["Maternity Waiting Period(In Days)"] = ""
        data["Maternity Limit On Number Of Live Children"] = ""
        data["Maternity Member Contribution Applicable?"] = ""
        data["Maternity Copay or deductible Applicable?"] = ""
        data["Maternity Is Combined?"] = ""
        data["Maternity Sum Insured"] = ""
        data["Maternity % Limit"] = ""
        data["Maternity Limit"] = ""
        data["Maternity Applicability"] = ""
        data["Maternity Copay"] = ""
        data["Maternity Deductible"] = ""
        data["Maternity Is Combined? (2)"] = ""

    # Clear ALL maternity fields if Maternity Is Combined? is "No"
    if data.get("Maternity Is Combined?") == "No":
        print("[INFO] Clearing ALL maternity fields as Maternity Is Combined? is 'No'")
        # Clear ALL maternity fields when maternity is not combined
        data["Maternity Sum Insured"] = ""
        data["Maternity % Limit"] = ""
        data["Maternity Limit"] = ""
        data["Maternity Applicability"] = ""
        data["Maternity Copay"] = ""
        data["Maternity Deductible"] = ""
        data["Maternity Is Combined? (2)"] = ""

    # Clear ALL Pre-Natal fields if Pre-Natal Benefit Applicable is "No"
    if data.get("Pre-Natal Benefit Applicable?") == "No":
        print("[INFO] Clearing ALL Pre-Natal fields as Pre-Natal Benefit Applicable is 'No'")
        # Clear ALL Pre-Natal fields
        data["Pre-Natal Waiting Period"] = ""
        data["Pre-Natal Limit On Children"] = ""
        data["Pre-Natal Member Contribution"] = ""
        data["Pre-Natal Copay/Deductible"] = ""
        data["Pre-Natal Is Combined"] = ""
        data["Pre-Natal Sum Insured"] = ""
        data["Pre-Natal % Limit"] = ""
        data["Pre-Natal Limit"] = ""
        data["Pre-Natal Applicability"] = ""
        data["Pre-Natal Copay"] = ""
        data["Pre-Natal Deductible"] = ""
        data["Pre-Natal Is Combined (2)"] = ""

    # Clear ALL Post-Natal fields if Post-Natal Benefit Applicable is "No"
    if data.get("Post-Natal Benefit Applicable?") == "No":
        print("[INFO] Clearing ALL Post-Natal fields as Post-Natal Benefit Applicable is 'No'")
        # Clear ALL Post-Natal fields
        data["Post-Natal Waiting Period"] = ""
        data["Post-Natal Limit On Children"] = ""
        data["Post-Natal Member Contribution"] = ""
        data["Post-Natal Copay/Deductible"] = ""
        data["Post-Natal Is Combined"] = ""
        data["Post-Natal Sum Insured"] = ""
        data["Post-Natal % Limit"] = ""
        data["Post-Natal Limit"] = ""
        data["Post-Natal Applicability"] = ""
        data["Post-Natal Copay"] = ""
        data["Post-Natal Deductible"] = ""
        data["Post-Natal Is Combined (2)"] = ""

    # New Born logic: Two-step check
    # Step 1: If New Born Covered? is "Yes", set Covered From to "0"
    if data.get("New Born Covered?") == "Yes":
        data["Covered From"] = "0"
        print("[INFO] New Born Covered is 'Yes', setting Covered From to '0'")
    
    # Step 2: If Is New Born Limit Applicable is "No", clear all other New Born fields
    if data.get("Is New Born Limit Applicable") == "No":
        print("[INFO] Clearing New Born fields as Is New Born Limit Applicable is 'No'")
        # Clear New Born fields but keep Covered From if it was set
        data["New Born Covered?"] = ""
        data["New Born Covered"] = ""
        data["New Born Sum Insured"] = ""
        data["New Born % Limit"] = ""
        data["New Born Limit"] = ""
        data["New Born Applicability"] = ""
        data["New Born % Limit Applicable On"] = ""

    return [data]