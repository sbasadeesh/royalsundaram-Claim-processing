Epic2.2: Primary Covers
Pre & Post Hospitalisation Benefit
Business Logic: Dynamically extracts Pre Hospitalisation and Post Hospitalisation details from the “Special Clauses” section of the policy document.

Pre Hospitalisation: If "Pre Hospitalisation Expenses" is found, sets Type of expense 1 to "Pre Hospitalisation Expense", extracts No. Of Days 1 (default 30), % Limit Applicable 1 as "Sum Insured", Limit Percentage 1 as "100", and Applicability 1 as "Lower".

Post Hospitalisation: If "Post Hospitalisation Expenses" is found, sets Type of expense 2 to "Post Hospitalisation Expense", extracts No. Of Days 2 (default 60), % Limit Applicable 2 as "Sum Insured", Limit Percentage 2 as "100", and Applicability 2 as "Lower".

Fields remain empty unless relevant clauses are present in the text.

Live Code Location: extract_primary_data.py → extract_primary_data() (dynamic Pre & Post Hospitalisation section)

Direct Code Link: View Function extract_primary_data() on GitHub

Code Snippet:
python
Copy
Edit
# === DYNAMIC PRE HOSPITALISATION SECTION - BASED ON SPECIAL CLAUSES ===
if re.search(r'Pre\s+Hospitalisation\s+Expenses', special_clauses_text, re.IGNORECASE):
    data["Type of expense 1"] = "Pre Hospitalisation Expense"
    
    pre_days_match = re.search(r'(\d+)\s*days?\s*preceding', special_clauses_text, re.IGNORECASE)
    if pre_days_match:
        data["No. Of Days 1"] = pre_days_match.group(1)
        print(f"[OK] Pre Hospitalisation days extracted: {pre_days_match.group(1)}")
    else:
        data["No. Of Days 1"] = "30"
        print("[INFO] Pre Hospitalisation days not found, using default: 30")
    
    data["% Limit Applicable 1"] = "Sum Insured"
    data["Limit Percentage 1"] = "100"
    data["Applicability 1"] = "Lower"
    print("[OK] Pre Hospitalisation fields populated from Special Clauses")

# === DYNAMIC POST HOSPITALISATION SECTION - BASED ON SPECIAL CLAUSES ===
if re.search(r'Post\s+Hospitalisation\s+Expenses', special_clauses_text, re.IGNORECASE):
    data["Type of expense 2"] = "Post Hospitalisation Expense"
    
    post_days_match = re.search(r'(\d+)\s*days?\s*immediately\s*after', special_clauses_text, re.IGNORECASE)
    if post_days_match:
        data["No. Of Days 2"] = post_days_match.group(1)
        print(f"[OK] Post Hospitalisation days extracted: {post_days_match.group(1)}")
    else:
        data["No. Of Days 2"] = "60"
        print("[INFO] Post Hospitalisation days not found, using default: 60")
    
    data["% Limit Applicable 2"] = "Sum Insured"
    data["Limit Percentage 2"] = "100"
    data["Applicability 2"] = "Lower"
    print("[OK] Post Hospitalisation fields populated from Special Clauses")



    code link: https://github.com/sbasadeesh/royalsundaram-Claim-processing/blob/Epic2.2/extract_primary_data.py
