# RS Report - Eligibility Extraction Module

## Overview

The `extract_Eligibility.py` module extracts basic member eligibility information from insurance policy PDFs, focusing on member coverage details and age ranges.

## Business Logic

### Core Purpose
The module processes insurance policy documents to extract basic eligibility data:
- **Member Coverage**: Employee, Spouse, Children, Parents
- **Age Ranges**: Minimum and maximum ages for each member type
- **Member Classification**: Adult or Child based on age ranges

## Key Functions

### 1. `extract_age_ranges(text: str) -> Dict[str, Dict]`

**Purpose**: Dynamically extracts age ranges for different member types from policy text.

**Business Logic**:
- **Employee/Spouse**: Default 18-65 years, can be overridden by policy text
- **Children**: Default 3 months-25 years, supports "over X days" patterns
- **Parents**: Default 40-100 years, extracted from policy specifications

**Patterns Detected**:
- `employee.*age.*between.*(\d+).*to.*(\d+)`
- `children.*age.*between.*(\d+).*to.*(\d+)`
- `over\s+(\d+)\s+days` (for children minimum age)
- `parents.*age.*between.*(\d+).*to.*(\d+)`

**Returns**: Dictionary with age ranges for each member type:
```python
{
    "employee": {"min_years": 18, "min_months": 0, "max_years": 65, "max_months": 0},
    "spouse": {"min_years": 18, "min_months": 0, "max_years": 65, "max_months": 0},
    "children": {"min_years": 0, "min_months": 3, "max_years": 25, "max_months": 0},
    "parents": {"min_years": 40, "min_months": 0, "max_years": 100, "max_months": 0}
}
```

### 2. `determine_member_type(min_age_years: int, max_age_years: int) -> str`

**Purpose**: Determines if a member is classified as "Child" or "Adult" based on age range.

**Business Logic**:
- **Child**: If maximum age ≤ 18 years
- **Adult**: If minimum age ≥ 18 years
- **Mixed**: If range spans both child and adult ages, uses midpoint calculation

**Classification Rules**:
- If max_age ≤ 18 → "Child"
- If min_age ≥ 18 → "Adult"
- If range spans both → Calculate midpoint, classify based on midpoint

### 3. `extract_Eligibility(text: str) -> List[Dict]`

**Purpose**: Main function that orchestrates the entire eligibility extraction process.

**Business Logic Flow**:

#### Step 1: Extract Endt. No. 1 Section
- Searches for Endorsement No. 1 in policy text
- Falls back to alternative patterns if not found
- Uses entire text if section not found

#### Step 2: Extract Member Counts
**Employee Detection**:
- Looks for "Insured Person covers employees"
- Searches for "employee" keyword
- Assumes employee coverage if spouse/children found

**Spouse Detection**:
- Multiple patterns: "Spouse means the employee's legally married partner"
- "Dependent Spouse", "Spouse - 1", etc.

**Children Detection**:
- Multiple patterns for dependent children
- Supports various formats and spellings
- Defaults to 2 children if mentioned but no count specified

**Parents Detection**:
- Separate detection for dependent parents and parents-in-law
- Defaults to 2 each (father + mother, father-in-law + mother-in-law)

#### Step 3: Generate Output
Creates structured data for each member type with basic fields only.

## Data Structure

### Output Format
The function returns a list of dictionaries, each representing a covered member with basic fields only.

#### **Basic Member Fields (12 fields)**:
```python
{
    "Max No Of Members Covered": total_covered,
    "Relationship Covered (Member Count)": total_covered,
    "Relationship Covered": "Employee/Spouse/Son/Daughter/Father/Mother/Father-in-law/Mother-in-law",
    "Min_Age(In Years)": min_age_years,
    "Min_Age(In Months)": min_age_months,
    "Max_Age(In Years)": max_age_years,
    "Max_Age(In Months)": max_age_months,
    "Member": 1,
    "Member_Count": member_count,
    "Member_Type": "Adult/Child"
}
```

#### **Field Descriptions**:

**Basic Member Fields (12 fields):**
- `Max No Of Members Covered` - Total members covered under the policy
- `Relationship Covered (Member Count)` - Same as above
- `Relationship Covered` - Member type (Employee, Spouse, Son, Daughter, Father, Mother, Father-in-law, Mother-in-law)
- `Min_Age(In Years)` - Minimum age in years
- `Min_Age(In Months)` - Minimum age in months
- `Max_Age(In Years)` - Maximum age in years
- `Max_Age(In Months)` - Maximum age in months
- `Member` - Always 1 for individual members
- `Member_Count` - Number of members of this type covered
- `Member_Type` - "Adult" or "Child" based on age classification

## Key Features

### 1. Robust Pattern Matching
- Multiple regex patterns for each data point
- Fallback mechanisms when primary patterns fail
- Support for various PDF formats and layouts

### 2. Dynamic Age Extraction
- Extracts age ranges from policy text
- Supports different age formats and units
- Handles various member types

### 3. Member Classification
- Automatically classifies members as Adult or Child
- Uses age-based logic for classification
- Handles edge cases with midpoint calculation

### 4. Error Handling
- Graceful fallbacks when sections not found
- Default values for missing information
- Debug output for troubleshooting

### 5. Business Rule Compliance
- Follows insurance industry standards
- Handles various policy formats
- Supports multiple endorsement types

## Usage Example

```python
from extract_Eligibility import extract_Eligibility

# Extract eligibility from policy text
policy_text = "..." # PDF text content
eligibility_data = extract_Eligibility(policy_text)

# Process the results
for member in eligibility_data:
    print(f"Member: {member['Relationship Covered']}")
    print(f"Age Range: {member['Min_Age(In Years)']}-{member['Max_Age(In Years)']}")
    print(f"Member Type: {member['Member_Type']}")
```

## Debug Information

The module provides debug output to track extraction results:
```
[DEBUG] Endt. No. 1 extraction results:
[DEBUG] - Employee: 1
[DEBUG] - Spouse: 1
[DEBUG] - Children: 2
[DEBUG] - Parents: 2
[DEBUG] - Total covered: 6
```

This helps identify what information was successfully extracted and troubleshoot any issues.

## Business Impact

This module is critical for:
- **Policy Analysis**: Understanding member coverage details
- **Age Classification**: Determining Adult vs Child members
- **Compliance**: Ensuring all required fields are captured
- **Reporting**: Generating structured data for business intelligence
- **Automation**: Reducing manual processing of policy documents

The extracted data supports business analysts in making informed decisions about insurance coverage and policy comparisons.
