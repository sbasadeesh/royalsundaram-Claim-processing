Epic 2.5: Primary Covers
P-2.5: New Born Limit (BY - CF)
Business Logic: Extracts New Born coverage limit for the BY - CF (Birth Year – Current Financial Year) case from the policy text.

Benefit Applicable? → "Yes" if new born coverage is mentioned; "No" otherwise.

If Benefit Applicable? = "Yes" → Extract and populate:

Limit → Currency amount (e.g., Rs. 50,000) from the clause text.

% Limit Applicable On → "Sum Insured" (default unless specified).

% Limit → "100" (default unless specified).

Applicability → "Lower".

If Benefit Applicable? = "No" → Leave all other fields blank.

Live Code Location: extract_primary_data.py → extract_primary_data() (New Born BY - CF section)

Direct Code Link: View Section on GitHub

Code Snippet:
python
Copy
Edit
# === NEW BORN LIMIT (BY - CF) ===
if re.search(r'new\s+born.*(by\s*-\s*cf|birth\s+year.*current\s+financial\s+year)', policy_text, re.IGNORECASE):
    data["Benefit Applicable?"] = "Yes"
    
    limit_match = re.search(r'Rs\.?\s?([\d,]+)', policy_text)
    if limit_match:
        data["Limit"] = limit_match.group(1).replace(",", "")
    else:
        data["Limit"] = ""

    data["% Limit Applicable On"] = "Sum Insured"
    data["% Limit"] = "100"
    data["Applicability"] = "Lower"
else:
    data["Benefit Applicable?"] = "No"
    data["Limit"] = ""
    data["% Limit Applicable On"] = ""
    data["% Limit"] = ""
    data["Applicability"] = ""
