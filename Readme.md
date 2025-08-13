

## EPIC 3.3 – Addon Coverages Extraction

### **Description**

This module processes **policy endorsement text blocks** to extract details for selected addon covers:

* **Convalescence Benefit**
* **Critical Illness**
* **Daily Cash Cover**

It ensures the output is **always a list of dictionaries** for each cover, and when a cover is **not applicable**, the result contains default empty values.

---

## **Functions & Code Explanation**

---

### **1. Extract Convalescence Benefit Details**

**Purpose:** Extracts Sum Insured, Minimum Length of Stay (LOS), Applicable From date, and Benefit Amount from an endorsement block.

```python
def extract_convalescence_benefit_details(text_block: str, policy_sum_insured: float) -> Dict[str, Any]:
    details = {
        "Sum Insured": policy_sum_insured,
        "Minimum LOS in days": "",
        "Applicable From": "",
        "Benefit Amount": ""
    }
    days_match = re.search(r'exceeds\s+(\d+)\s+days', text_block, re.IGNORECASE)
    if days_match:
        details["Minimum LOS in days"] = int(days_match.group(1))

    benefit_match = re.search(r'benefit of Rs\.?\s*([\d,]+)', text_block, re.IGNORECASE)
    if benefit_match:
        details["Benefit Amount"] = float(benefit_match.group(1).replace(',', ''))
    return details
```

* **Logic:**

  * Detects `"exceeds X days"` → sets **Minimum LOS**.
  * Detects `"benefit of Rs XXXX"` → sets **Benefit Amount**.

---

### **2. Extract Critical Illness Fields**

**Purpose:** Extracts identifiers and financial limits from endorsement no. 20.

```python
def extract_critical_illness_field_identifiers(text_block: str) -> Dict[str, Any]:
    field_identifiers = {
        "Over And Above Policy Sum Insured?": "No",
        "Survival Period Applicable?": "No", 
        "Applicable Limit": "",
        "Sum Insured Per Person": "",
        "Maximum Limit": "",
        "Survival Period": "",
        "Maximum Limit Percentage": ""
    }
    
    # Check for 'Over And Above' policy sum insured
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

    # Extract Sum Insured per person
    sum_insured_match = re.search(r'sum insured of Rs\.?\s*([\d,]+)', text_block, re.IGNORECASE)
    if sum_insured_match:
        field_identifiers["Sum Insured Per Person"] = float(sum_insured_match.group(1).replace(',', ''))

    # Extract Maximum Limit and calculate percentage
    max_limit_match = re.search(r'maximum limit of Rs\.?\s*([\d,]+)', text_block, re.IGNORECASE)
    if max_limit_match:
        max_limit_value = float(max_limit_match.group(1).replace(',', ''))
        field_identifiers["Maximum Limit"] = max_limit_value
        field_identifiers["Applicable Limit"] = f"Rs. {max_limit_match.group(1)}"
        field_identifiers["Maximum Limit Percentage"] = round((max_limit_value / 500000) * 100, 2)

    # Detect Survival Period
    survival_patterns = [r'survival period', r'waiting period', r'minimum survival']
    for pattern in survival_patterns:
        if re.search(pattern, text_block, re.IGNORECASE):
            field_identifiers["Survival Period Applicable?"] = "Yes"
            survival_duration_match = re.search(r'(\d+)\s*(?:days?|months?|years?)\s*(?:survival|waiting)', text_block, re.IGNORECASE)
            if survival_duration_match:
                field_identifiers["Survival Period"] = survival_duration_match.group(1)
            break
    return field_identifiers
```

* **Logic:**

  * Detects if cover is **over and above** policy sum insured.
  * Extracts **Sum Insured Per Person** & **Maximum Limit**.
  * Calculates **Maximum Limit Percentage**.
  * Detects **Survival Period** and extracts duration.

---

### **3. Extract Daily Cash Cover Details**

**Purpose:** Extracts financial limits, applicability, and coverage conditions for Daily Cash Cover.

```python
def extract_daily_cash_cover_details(text_block: str) -> Dict[str, Any]:
    field_identifiers = {
        "DailyCash_Over_And_Above_Policy_Sum_Insured": "No",
        "DailyCash_Max_Days_Per_Policy_year": "",
        "DailyCash_Max_Days_Per_Illness": "",
        "DailyCash_Fixed_limit": "No",
        "DailyCash_Sum_Insured": "",
        "DailyCash_Threshold": "",
        "DailyCash_Limit_Amount": "",
        "DailyCash_Daily_Cash_Amount": "",
        "DailyCash_Daily_cash_percentage": "",
        "DailyCash_Minimum_Hospitalization_Days": "",
        "DailyCash_Minimum_LOS_in_days": "",
        "DailyCash_Maximum_Days_Per_Person": "",
        "DailyCash_Waiting_Period_Days": "",
        "DailyCash_Maternity_Exclusion": "No",
        "DailyCash_First_Days_Exclusion": "",
        "DailyCash_Open_range": "No",
        "DailyCash_Daily_Limit_Range_From": "",
        "DailyCash_Daily_Limit_Range_To": ""
    }
    
    # Check 'Over And Above' Policy Sum Insured
    over_above_patterns = [r'over and above.*?sum insured', r'over and above.*?individual sum insured', r'over and above.*?policy sum insured']
    for pattern in over_above_patterns:
        if re.search(pattern, text_block, re.IGNORECASE):
            field_identifiers["DailyCash_Over_And_Above_Policy_Sum_Insured"] = "Yes"
            break

    # Extract Max Days limits
    max_days_policy_match = re.search(r'maximum days of\s*(\d+)\s*per.*?policy', text_block, re.IGNORECASE)
    if max_days_policy_match:
        field_identifiers["DailyCash_Max_Days_Per_Policy_year"] = int(max_days_policy_match.group(1))

    max_days_illness_match = re.search(r'maximum days of\s*(\d+)\s*per.*?event', text_block, re.IGNORECASE)
    if max_days_illness_match:
        field_identifiers["DailyCash_Max_Days_Per_Illness"] = int(max_days_illness_match.group(1))

    # Extract Daily Cash Amount and percentage
    daily_amount_match = re.search(r'Rs\.?\s*([\d,]+)\s*per day', text_block, re.IGNORECASE)
    if daily_amount_match:
        daily_amount = float(daily_amount_match.group(1).replace(',', ''))
        field_identifiers["DailyCash_Daily_Cash_Amount"] = daily_amount
        field_identifiers["DailyCash_Limit_Amount"] = daily_amount
        field_identifiers["DailyCash_Daily_cash_percentage"] = round((daily_amount / 500000) * 100, 2)
    
    return field_identifiers
```

* **Logic:**

  * Detects "Over And Above" coverage.
  * Extracts **maximum days limits**.
  * Captures **Daily Cash Amount** & calculates **percentage**.

---

### **4. Create Addon Coverages**

**Purpose:** Orchestrates extraction for all addon covers.

```python
def create_addon_coverages(text: str, addon_covers_status: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
    DEFAULT_SUM_INSURED = 500000.0
    coverages_data = {}

    # Convalescence Benefit
    if addon_covers_status.get("Convalescence Benefit") == "Yes":
        blocks = re.findall(r'Endt\. No\.\s*15(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        coverages_data["Convalescence Benefit"] = [extract_convalescence_benefit_details(b, DEFAULT_SUM_INSURED) for b in blocks] or [{}]
    else:
        coverages_data["Convalescence Benefit"] = [{"Sum Insured": "", "Minimum LOS in days": "", "Applicable From": "", "Benefit Amount": ""}]

    # Critical Illness
    if addon_covers_status.get("Critical Illness") == "Yes":
        blocks = re.findall(r'Endt\. No\.\s*20(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        coverages_data["Critical Illness"] = [extract_critical_illness_field_identifiers(b) for b in blocks] or [{}]
    else:
        coverages_data["Critical Illness"] = [{"Over And Above Policy Sum Insured?": "", "Survival Period Applicable?": "", "Applicable Limit": "", "Sum Insured Per Person": "", "Maximum Limit": "", "Survival Period": "", "Maximum Limit Percentage": ""}]

    # Daily Cash Cover
    if addon_covers_status.get("Daily Cash Cover") == "Yes":
        blocks = re.findall(r'Endt\. No\.\s*14(.*?)(?=Endt\. No\.|$)', text, re.DOTALL | re.IGNORECASE)
        coverages_data["Daily Cash Cover"] = [extract_daily_cash_cover_details(b) for b in blocks] or [{}]
    else:
        coverages_data["Daily Cash Cover"] = [{"DailyCash_Over_And_Above_Policy_Sum_Insured": "", "DailyCash_Max_Days_Per_Policy_year": "", "DailyCash_Max_Days_Per_Illness": "", "DailyCash_Fixed_limit": "", "DailyCash_Sum_Insured": "", "DailyCash_Threshold": "", "DailyCash_Limit_Amount": "", "DailyCash_Daily_Cash_Amount": "", "DailyCash_Daily_cash_percentage": "", "DailyCash_Minimum_Hospitalization_Days": "", "DailyCash_Minimum_LOS_in_days": "", "DailyCash_Maximum_Days_Per_Person": "", "DailyCash_Waiting_Period_Days": "", "DailyCash_Maternity_Exclusion": "", "DailyCash_First_Days_Exclusion": "", "DailyCash_Open_range": "", "DailyCash_Daily_Limit_Range_From": "", "DailyCash_Daily_Limit_Range_To": ""}]
    
    return coverages_data
```

---

Do you want me to now also make the **PR submission template** for this exact README so you can attach it directly to your GitHub PR? That way it’s consistent with your other epics.
