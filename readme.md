Epic 2.2: Pre & Post Hospitalisation – Combined Benefit
Business Logic: Detects if the policy specifies that Pre and Post Hospitalisation expenses share a single combined limit.

Benefit Applicable? → "Yes" if “pre and post hospitalisation combined” phrase is found in policy text.

Is Pre and Post Combined? → Always "Yes" for this case.

Type Of Expense → "Pre & Post Hospitalisation Expense".

No. Of Days → Left blank (limit applies collectively, not per duration).

% Limit Applicable On → "Sum Insured".

% Limit → "100".

Limit → Left blank (derived from overall sum insured).

Applicability → "Lower".

Live Code Location: extract_primary_data.py → extract_primary_data() (Combined Pre & Post Hospitalisation section)

Direct Code Link: View on GitHub

Code Snippet:
python
Copy
Edit
# === PRE & POST HOSPITALISATION COMBINED BENEFIT SECTION ===
if re.search(r'pre\s*and\s*post\s*hospitalisation\s*combined', policy_text, re.IGNORECASE):
    data["Benefit Applicable?"] = "Yes"
    data["Is Pre and Post Combined?"] = "Yes"
    data["Type Of Expense"] = "Pre & Post Hospitalisation Expense"
    data["No. Of Days"] = ""
    data["% Limit Applicable On"] = "Sum Insured"
    data["% Limit"] = "100"
    data["Limit"] = ""
    data["Applicability"] = "Lower"
