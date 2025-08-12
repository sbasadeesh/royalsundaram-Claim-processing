Epic P-2.X: Maternity Benefit – Excel Output Logic
Business Logic:
This section writes maternity benefit data into the Excel output file (ws2) with column-level control based on two key flags:

Maternity Benefit Applicable? – Determines whether maternity details should be populated at all.

Maternity Is Combined? – Determines whether combined maternity coverage is used or separate Normal/Caesarean limits apply.

Logic Flow:

Columns 21–26: Always filled with general maternity details (Benefit Applicable, Waiting Period, Limit on Number of Live Children, Member Contribution Applicable, Copay/Deductible Applicable, Is Combined).

If Maternity Is Combined? = "No":

Columns 27–33 → Left blank (combined maternity fields not applicable).

Columns 34–48 → Populated with separate Normal and Caesarean delivery details (sum insured, limits, applicability, copay, etc.).

If Maternity Is Combined? = "Yes":

Columns 27–33 → Populated with combined maternity details (sum insured, % limit, delivery limit, applicability, copay, deductible).

Columns 34–48 → Left blank (no separate limits).

If Maternity Benefit Applicable? = "Yes" AND Maternity Is Combined? ≠ "Yes":

Columns 34–48 → Populated with Normal and Caesarean delivery details.

If Maternity Benefit Applicable? = "No" OR Maternity Is Combined? = "Yes":

Columns 34–48 → Left blank.

Live Code Location: extract_primary_data.py → extract_primary_data() (Maternity Benefit Excel writing section)


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
        # First check for Normal delivery and Caesarean amounts
        normal_caesarean_match = re.search(r"limited to Rs\.([\d,]+)/-.*?Normal\s+delivery.*?([\d,]+)/-.*?Caesarean", endorsement_11b_text, re.IGNORECASE | re.DOTALL)
        if not normal_caesarean_match:
            # Alternative pattern for different text formats
            normal_caesarean_match = re.search(r"maximum.*?benefit.*?limited.*?Rs\.([\d,]+)/-.*?Normal\s+delivery.*?([\d,]+)/-.*?Caesarean", endorsement_11b_text, re.IGNORECASE | re.DOTALL)
        if not normal_caesarean_match:
            # Pattern for "Rs. 25000/- Per Family for Normal delivery and 35000/- for Caesarean"
            normal_caesarean_match = re.search(r"Rs\.\s*([\d,]+)/-.*?Normal\s+delivery.*?([\d,]+)/-.*?Caesarean", endorsement_11b_text, re.IGNORECASE | re.DOTALL)
        if not normal_caesarean_match:
            # Pattern for "limited to Rs. 25000/- Per Family for Normal delivery and 35000/- for Caesarean"
            normal_caesarean_match = re.search(r"limited to Rs\.\s*([\d,]+)/-.*?Normal\s+delivery.*?([\d,]+)/-.*?Caesarean", endorsement_11b_text, re.IGNORECASE | re.DOTALL)
        if not normal_caesarean_match:
            # Pattern for "Rs.75,000 for both Normal and Caesarean per Family"
            normal_caesarean_match = re.search(r"Rs\.([\d,]+).*?for both Normal and Caesarean", endorsement_11b_text, re.IGNORECASE | re.DOTALL)
        if not normal_caesarean_match:
            # Pattern for "limited to Rs.75,000 for both Normal and Caesarean per Family"
            normal_caesarean_match = re.search(r"limited to Rs\.([\d,]+).*?for both Normal and Caesarean", endorsement_11b_text, re.IGNORECASE | re.DOTALL)
        
        if normal_caesarean_match:
            # Check if this is the "for both Normal and Caesarean" pattern (only one amount)
            if "for both Normal and Caesarean" in endorsement_11b_text:
                # Same amount for both Normal and Caesarean
                shared_amount = int(normal_caesarean_match.group(1).replace(",", ""))
                maternity_data["Normal Delivery Limit"] = str(shared_amount)
                maternity_data["Caesarean Limit"] = str(shared_amount)
                maternity_data["Limit"] = str(shared_amount)
                print(f"[OK] Maternity limit extracted - Normal and Caesarean (same amount): Rs. {shared_amount}")
            else:
                # Different amounts for Normal and Caesarean
                normal_amount = int(normal_caesarean_match.group(1).replace(",", ""))
                caesarean_amount = int(normal_caesarean_match.group(2).replace(",", ""))
                # Store both amounts separately
                maternity_data["Normal Delivery Limit"] = str(normal_amount)
                maternity_data["Caesarean Limit"] = str(caesarean_amount)
                # Use the higher amount as the maternity limit
                maternity_limit = max(normal_amount, caesarean_amount)
                maternity_data["Limit"] = str(maternity_limit)
                print(f"[OK] Maternity limit extracted - Normal: Rs. {normal_amount}, Caesarean: Rs. {caesarean_amount}, Using: Rs. {maternity_limit}")
        else:
            # Fallback to standard single amount pattern
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

