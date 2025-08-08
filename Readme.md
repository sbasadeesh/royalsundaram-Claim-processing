
Epic Documentation 2.1 to 2.2

## Overview

The `extract_primary_data.py` file is a comprehensive module for extracting structured data from insurance policy PDFs. It focuses on two critical epics:

- **EPIC 2.1**: Core Primary Cover Applicability (Columns A-K)
- **EPIC 2.2**: Pre and Post Hospitalization (Columns I-T)

## File Structure

```python
extract_primary_data.py
├── extract_newborn_from_endt_12()           # New Born benefits extraction
├── extract_pre_post_natal_from_endt_11b()   # Pre/Post Natal benefits
├── extract_maternity_from_endt_11b()        # Maternity benefits
└── extract_primary_data()                   # Main extraction function
```

## EPIC 2.1: Core Primary Cover Applicability (Columns A-K)

### Business Logic

The Core Primary Cover section dynamically detects when combined benefits are applicable based on Special Clauses and Value Added Services sections in insurance policy documents.

### Data Structure

```python
# === DYNAMIC COMBINED SECTION - BASED ON SPECIAL CLAUSES ===
data = {
    "Combined_Benefit_Applicable": "",        # Column A
    "Combined_Is_Pre_and_Post_Combined": "No", # Column B
    "Combined_Type_Of_Expense": "",           # Column C
    "Combined_No_Of_Days": "",               # Column D
    "Combined_Percent_Limit_Applicable_On": "", # Column E
    "Combined_Percent_Limit": "",            # Column F
    "Combined_Limit": "",                    # Column G
    "Combined_Applicability": "",            # Column H
}
```

### Implementation Details

#### 1. Special Clauses Detection
```python
# Check if Special Clauses or Value Added Services section exists
special_clauses_match = re.search(r'Special\s+Clauses:\s*(.*?)(?=Endorsement|Endt\.|Group Health Policy|$)', text, re.IGNORECASE | re.DOTALL)
value_added_services_match = re.search(r'Value\s+Added\s+Services:\s*(.*?)(?=Endorsement|Endt\.|Group Health Policy|$)', text, re.IGNORECASE | re.DOTALL)
```

#### 2. Combined Benefit Logic
```python
# Check Special Clauses first
if special_clauses_match:
    special_clauses_text = special_clauses_match.group(1).strip()
    
    # Check if Special Clauses contains relevant content for combined benefits
    pre_found = re.search(r'Pre\s+Hospitalisation\s+Expenses', special_clauses_text, re.IGNORECASE)
    post_found = re.search(r'Post\s+Hospitalisation\s+Expenses', special_clauses_text, re.IGNORECASE)
    
    if pre_found or post_found:
        data["Combined_Benefit_Applicable"] = "Yes"
        relevant_content_found = True
        print("[OK] Combined_Benefit_Applicable set to 'Yes' - relevant content found in Special Clauses")
```

#### 3. Value Added Services Fallback
```python
# Check Value Added Services if Special Clauses didn't have relevant content
if not relevant_content_found and value_added_services_match:
    value_added_services_text = value_added_services_match.group(1).strip()
    
    # Check if Value Added Services contains relevant content for combined benefits
    pre_found = re.search(r'Pre\s+Hospitalisation\s+Expenses', value_added_services_text, re.IGNORECASE)
    post_found = re.search(r'Post\s+Hospitalisation\s+Expenses', value_added_services_text, re.IGNORECASE)
    
    if pre_found or post_found:
        data["Combined_Benefit_Applicable"] = "Yes"
        relevant_content_found = True
        print("[OK] Combined_Benefit_Applicable set to 'Yes' - relevant content found in Value Added Services")
```

### Business Rules

1. **Combined_Benefit_Applicable**: 
   - "Yes" if Pre/Post Hospitalization found in Special Clauses or Value Added Services
   - "No" if no relevant content found

2. **Combined_Is_Pre_and_Post_Combined**: Always "No" (hardcoded)

3. **Other Combined Fields**: Always empty (hardcoded)

## EPIC 2.2: Pre and Post Hospitalization (Columns I-T)

### Business Logic

The Pre and Post Hospitalization section extracts detailed information about hospitalization expenses from Special Clauses sections, including expense types, number of days, limits, and applicability.

### Data Structure

```python
# === DYNAMIC PRE HOSPITALISATION SECTION - BASED ON SPECIAL CLAUSES ===
data = {
    "Type of expense 1": "",           # Column I
    "No. Of Days 1": "",              # Column J
    "% Limit Applicable 1": "",        # Column K
    "Limit Percentage 1": "",          # Column L
    "Limit Amount 1": "",              # Column M
    "Applicability 1": "",             # Column N
}

# === DYNAMIC POST HOSPITALISATION SECTION - BASED ON SPECIAL CLAUSES ===
data = {
    "Type of expense 2": "",           # Column O
    "No. Of Days 2": "",              # Column P
    "% Limit Applicable 2": "",        # Column Q
    "Limit Percentage 2": "",          # Column R
    "Limit Amount 2": "",              # Column S
    "Applicability 2": "",             # Column T
}
```

### Implementation Details

#### 1. Pre Hospitalization Extraction
```python
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
```

#### 2. Post Hospitalization Extraction
```python
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
```

#### 3. Limit Amount Extraction
```python
# === Corporate Floater ===
corp_floater = re.search(r"limit of Rs\.([\d,]+)/- as Corporate floater", text, re.IGNORECASE)
if corp_floater:
    data["Limit Amount 1"] = corp_floater.group(1).replace(",", "")

# === Ambulance limit fallback ===
ambulance = re.search(r"limit of Rs\.([\d,]+)/- per claim", text, re.IGNORECASE)
if ambulance and not data["Limit Amount 1"]:
    data["Limit Amount 1"] = ambulance.group(1).replace(",", "")

# === Pre & Post Natal OPD ===
if "Pre-Natal and Post-Natal Expense is extended to be covered on Out-patient basis" in text:
    opd_limit = re.search(r"sublimit of Rs\.?\s?([\d,]+)", text, re.IGNORECASE)
    if opd_limit:
        data["Limit Amount 2"] = opd_limit.group(1).replace(",", "")
```

### Business Rules

#### Pre Hospitalization (Columns I-N)
1. **Type of expense 1**: "Pre Hospitalisation Expense" if found in Special Clauses
2. **No. Of Days 1**: Extracted from text or defaults to "30"
3. **% Limit Applicable 1**: Always "Sum Insured"
4. **Limit Percentage 1**: Always "100"
5. **Limit Amount 1**: From Corporate Floater or Ambulance limit
6. **Applicability 1**: Always "Lower"

#### Post Hospitalization (Columns O-T)
1. **Type of expense 2**: "Post Hospitalisation Expense" if found in Special Clauses
2. **No. Of Days 2**: Extracted from text or defaults to "60"
3. **% Limit Applicable 2**: Always "Sum Insured"
4. **Limit Percentage 2**: Always "100"
5. **Limit Amount 2**: From OPD sublimit or disease limits
6. **Applicability 2**: Always "Lower"

## Regex Patterns Used

### Special Clauses Detection
```python
r'Special\s+Clauses:\s*(.*?)(?=Endorsement|Endt\.|Group Health Policy|$)'
```

### Value Added Services Detection
```python
r'Value\s+Added\s+Services:\s*(.*?)(?=Endorsement|Endt\.|Group Health Policy|$)'
```

### Pre Hospitalization Patterns
```python
r'Pre\s+Hospitalisation\s+Expenses'  # Detection
r'(\d+)\s*days?\s*preceding'         # Days extraction
```

### Post Hospitalization Patterns
```python
r'Post\s+Hospitalisation\s+Expenses'  # Detection
r'(\d+)\s*days?\s*immediately\s*after' # Days extraction
```

### Limit Amount Patterns
```python
r"limit of Rs\.([\d,]+)/- as Corporate floater"  # Corporate floater
r"limit of Rs\.([\d,]+)/- per claim"             # Ambulance limit
r"sublimit of Rs\.?\s?([\d,]+)"                  # OPD sublimit
```

## Error Handling and Logging

### Debug Logging
```python
print(f"[DEBUG] Special Clauses found: {special_clauses_match is not None}")
print(f"[DEBUG] Value Added Services found: {value_added_services_match is not None}")
print(f"[DEBUG] Special Clauses text: {special_clauses_text[:200]}...")
```

### Success Logging
```python
print("[OK] Combined_Benefit_Applicable set to 'Yes' - relevant content found in Special Clauses")
print(f"[OK] Pre Hospitalisation days extracted: {pre_days_match.group(1)}")
print("[OK] Pre Hospitalisation fields populated from Special Clauses")
```

### Information Logging
```python
print("[INFO] Special Clauses found but no relevant content")
print("[INFO] Pre Hospitalisation days not found, using default: 30")
print("[INFO] Combined_Benefit_Applicable set to 'No' - no relevant content found")
```

## Performance Considerations

1. **Regex Optimization**: Uses compiled regex patterns for efficient matching
2. **Early Exit**: Stops processing when relevant content is found
3. **Default Values**: Provides fallback values to avoid empty fields
4. **Memory Efficiency**: Processes text in chunks to handle large documents

## Testing Scenarios

### EPIC 2.1 Test Cases
1. **Special Clauses with Pre/Post**: Should set Combined_Benefit_Applicable to "Yes"
2. **Value Added Services with Pre/Post**: Should set Combined_Benefit_Applicable to "Yes"
3. **No Special Clauses**: Should set Combined_Benefit_Applicable to "No"
4. **Empty Special Clauses**: Should set Combined_Benefit_Applicable to "No"

### EPIC 2.2 Test Cases
1. **Pre Hospitalization Found**: Should populate columns I-N with appropriate values
2. **Post Hospitalization Found**: Should populate columns O-T with appropriate values
3. **Both Found**: Should populate both sections
4. **Days Extraction**: Should extract specific days or use defaults
5. **Limit Amounts**: Should extract from various sources (Corporate Floater, OPD, etc.)

## Integration Points

### Excel Output
The extracted data is mapped to specific Excel columns:
- **Columns A-H**: Core Primary Cover (EPIC 2.1)
- **Columns I-N**: Pre Hospitalization (EPIC 2.2)
- **Columns O-T**: Post Hospitalization (EPIC 2.2)

### Main Application
Called from `Main.py`:
```python
from extract_primary_data import extract_primary_data
primary_data = extract_primary_data(extracted_text)
```

### Excel Formatting
Processed by `create_comprehensive_excel_with_formatting.py`:
```python
# Pre Hospitalisation section (columns 9-14)
ws2.cell(row=row_idx, column=9, value=data.get("Type of expense 1", ""))
ws2.cell(row=row_idx, column=10, value=data.get("No. Of Days 1", ""))
# ... etc
```

This documentation provides a comprehensive overview of the two epics implemented in `extract_primary_data.py`, including business logic, implementation details, and integration points.
