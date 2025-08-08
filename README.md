# RS Report - Eligibility Extraction Module

## Overview

The `extract_Eligibility.py` module is designed to extract and process eligibility information from insurance policy PDFs, specifically focusing on member coverage details, age ranges, sublimits, and corporate buffer information. This module is part of a larger system for analyzing and reporting on insurance policy documents.

## Business Logic

### Core Purpose
The module processes insurance policy documents to extract structured eligibility data that includes:
- **Member Coverage**: Employee, Spouse, Children, Parents
- **Age Ranges**: Minimum and maximum ages for each member type
- **Sublimits**: Specific coverage limits for medical conditions
- **Corporate Buffer**: Additional coverage limits and reload options
- **Critical Illness**: Special coverage for critical illness conditions

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

### 2. `extract_sublimit_info(text: str) -> Dict`

**Purpose**: Extracts sublimit information from policy text, including Endt. No. 5(ii) sections.

**Business Logic**:
- Searches for sublimit patterns in policy text
- Extracts specific medical conditions and their coverage limits
- Calculates percentages and maximum amounts
- Supports conditions like Cataract, Mental Illness, Balloon Sinuplasty, etc.

**Supported Conditions**:
- Cataract (10% of Sum Insured, max ₹50,000)
- Treatment of mental illness (25% of Sum Insured, max ₹30,000)
- Balloon Sinuplasty (10% of Sum Insured, max ₹100,000)
- Stem Cell therapy (10% of Sum Insured, max ₹100,000)
- Oral Chemotherapy (5% of Sum Insured, max ₹100,000)
- And more...

**Returns**: Dictionary with sublimit information:
```python
{
    "applicable": "Yes/No",
    "type": "Condition name",
    "limit": calculated_amount,
    "percentage": "10%/25%/5%",
    "max_amount": maximum_limit
}
```

### 3. `determine_member_type(min_age_years: int, max_age_years: int) -> str`

**Purpose**: Determines if a member is classified as "Child" or "Adult" based on age range.

**Business Logic**:
- **Child**: If maximum age ≤ 18 years
- **Adult**: If minimum age ≥ 18 years
- **Mixed**: If range spans both child and adult ages, uses midpoint calculation

**Classification Rules**:
- If max_age ≤ 18 → "Child"
- If min_age ≥ 18 → "Adult"
- If range spans both → Calculate midpoint, classify based on midpoint

### 4. `extract_corporate_buffer_applicability(text: str) -> str`

**Purpose**: Checks if Endt. No. 10 (Corporate Buffer) is applicable in the policy.

**Business Logic**:
- Searches for "Endt. No. 10" or "Endorsement No. 10" in text
- Returns "Yes" if found, "No" if not found

### 5. `calculate_sublimit(sum_insured: int, percentage: str, max_amount: int) -> int`

**Purpose**: Calculates actual sublimit amount based on sum insured and percentage.

**Business Logic**:
- Calculates percentage of sum insured
- Applies maximum limit constraint
- Supports 5%, 10%, and 25% percentages

**Formula**: `min(calculated_amount, max_amount)`

### 6. `extract_Eligibility(text: str) -> List[Dict]`

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

#### Step 3: Extract Additional Information
**Sum Insured**:
- Extracts from "Corporate floater" patterns
- Falls back to general "sum insured" patterns
- Defaults to ₹200,000 if not found

**Corporate Buffer**:
- Extracts from Endt. No. 10
- Includes family limits, parent limits, reload options
- Extracts OPD limits

**Critical Illness**:
- Searches for critical illness mentions
- Extracts family limits and coverage details

#### Step 4: Calculate Sublimits
- Uses extracted sum insured and sublimit percentages
- Applies maximum limits from policy
- Calculates actual payable amounts

#### Step 5: Generate Output
Creates structured data for each member type:

**Employee Row** (Complete with all fields):
- Basic member information
- Age ranges
- Sublimit details
- Corporate buffer information
- Critical illness details
- All policy-specific fields

**Other Member Rows** (Basic fields only):
- Spouse, Son, Daughter, Father, Mother, Father-in-law, Mother-in-law
- Age ranges and member type only

## Data Structure

### Output Format
The function returns a list of dictionaries, each representing a covered member. The **Employee row** contains all comprehensive fields, while other member rows contain only basic fields.

#### **Employee Row (Complete Fields)**:
```python
{
    # Basic Member Information
    "Max No Of Members Covered": total_covered,
    "Relationship Covered (Member Count)": total_covered,
    "Relationship Covered": "Employee",
    "Min_Age(In Years)": min_age_years,
    "Min_Age(In Months)": min_age_months,
    "Max_Age(In Years)": max_age_years,
    "Max_Age(In Months)": max_age_months,
    "Member": 1,
    "Member_Count": employee_count,
    "Member_Type": "Adult/Child",
    
    # Sublimit Information
    "Sublimit_Applicable": "Yes/No",
    "Sublimit_Type": "Condition name (e.g., Cataract)",
    "Sub_Limit": calculated_amount,
    
    # Family Buffer Information
    "Family Buffer Applicable": "Yes/No",
    "Family Buffer Amount": buffer_limit,
    "Is Network Applicable": "No",
    "Black listed hospitals are applicable?": "Yes",
    
    # Corporate Buffer Information
    "Corporate Buffer applicable": "Yes/No",
    "Buffer Type": "Both" if applicable else "",
    "Applicable for": "Normal Illness and Critical Illness" if applicable else "",
    "Total Corporate Buffer": corporate_buffer_limit_family,
    "Corporate Buffer Limit Per Family": corporate_buffer_limit_family,
    "Corporate Buffer Limit Per Parent": corporate_buffer_limit_parent,
    "Reload of SI": reload_option,
    "Total Corporate Buffer.1": corporate_buffer_limit_family,
    "Corporate Buffer Limit Per Family.1": corporate_buffer_limit_family,
    "Corporate Buffer Limit Per Parent.1": corporate_buffer_limit_parent,
    "Reload of SI.1": reload_option,
    "Approving Authority": "Corporate HR" if applicable else "",
    "Buffer OPD Limit": buffer_opd_limit,
    "Whether increase in sum insured permissible at renewal": "No",
    "Total Plan Buffer": corporate_buffer_limit_family,
    "Corporate Bufferr Limit for Employee/Family": corporate_buffer_limit_family,
    "Corporate Buffer Limit Per Parent.2": corporate_buffer_limit_parent,
    "Reload of SI.2": reload_option,
    "Approving Authority.1": "Corporate HR" if applicable else "",
    "Buffer OPD Limit.1": buffer_opd_limit,
    "Whether increase in sum insured permissible at renewal.1": "No",
    
    # Critical Illness Information
    "Critical Illness applicable": "Yes/No",
    "Critical Illness limit per family": critical_illness_limit,
    "Critical Illness Approving Authority": "Corporate HR" if applicable else "",
    "Critical Illness Whether increase in sum insured permissible at renewal": "No"
}
```

#### **Other Member Rows (Basic Fields Only)**:
```python
{
    "Relationship Covered": "Spouse/Son/Daughter/Father/Mother/Father-in-law/Mother-in-law",
    "Min_Age(In Years)": min_age_years,
    "Min_Age(In Months)": min_age_months,
    "Max_Age(In Years)": max_age_years,
    "Max_Age(In Months)": max_age_months,
    "Member": 1,
    "Member_Type": "Adult/Child"
}
```

#### **Complete Field List for Employee Row**:

**Basic Member Fields:**
- `Max No Of Members Covered` - Total members covered under the policy
- `Relationship Covered (Member Count)` - Same as above
- `Relationship Covered` - "Employee"
- `Min_Age(In Years)` - Minimum age in years
- `Min_Age(In Months)` - Minimum age in months
- `Max_Age(In Years)` - Maximum age in years
- `Max_Age(In Months)` - Maximum age in months
- `Member` - Always 1 for individual members
- `Member_Count` - Number of employees covered
- `Member_Type` - "Adult" or "Child"

**Sublimit Fields:**
- `Sublimit_Applicable` - "Yes" or "No"
- `Sublimit_Type` - Specific condition (e.g., "Cataract", "Mental Illness")
- `Sub_Limit` - Calculated sublimit amount

**Family Buffer Fields:**
- `Family Buffer Applicable` - "Yes" or "No"
- `Family Buffer Amount` - Buffer limit amount
- `Is Network Applicable` - Always "No"
- `Black listed hospitals are applicable?` - Always "Yes"

**Corporate Buffer Fields:**
- `Corporate Buffer applicable` - "Yes" or "No"
- `Buffer Type` - "Both" if applicable, empty if not
- `Applicable for` - "Normal Illness and Critical Illness" if applicable
- `Total Corporate Buffer` - Total buffer amount
- `Corporate Buffer Limit Per Family` - Family limit
- `Corporate Buffer Limit Per Parent` - Parent limit
- `Reload of SI` - Reload option (e.g., "No limit for the reload of SI")
- `Total Corporate Buffer.1` - Duplicate of total buffer
- `Corporate Buffer Limit Per Family.1` - Duplicate of family limit
- `Corporate Buffer Limit Per Parent.1` - Duplicate of parent limit
- `Reload of SI.1` - Duplicate of reload option
- `Approving Authority` - "Corporate HR" if applicable, empty if not
- `Buffer OPD Limit` - OPD limit amount
- `Whether increase in sum insured permissible at renewal` - Always "No"
- `Total Plan Buffer` - Same as total corporate buffer
- `Corporate Bufferr Limit for Employee/Family` - Same as family limit
- `Corporate Buffer Limit Per Parent.2` - Duplicate of parent limit
- `Reload of SI.2` - Duplicate of reload option
- `Approving Authority.1` - Duplicate of approving authority
- `Buffer OPD Limit.1` - Duplicate of OPD limit
- `Whether increase in sum insured permissible at renewal.1` - Always "No"

**Critical Illness Fields:**
- `Critical Illness applicable` - "Yes" or "No"
- `Critical Illness limit per family` - Critical illness limit amount
- `Critical Illness Approving Authority` - "Corporate HR" if applicable, empty if not
- `Critical Illness Whether increase in sum insured permissible at renewal` - Always "No"

## Key Features

### 1. Robust Pattern Matching
- Multiple regex patterns for each data point
- Fallback mechanisms when primary patterns fail
- Support for various PDF formats and layouts

### 2. Dynamic Calculation
- Calculates actual sublimit amounts based on sum insured
- Applies percentage and maximum constraints
- Handles different percentage types (5%, 10%, 25%)

### 3. Comprehensive Coverage
- Extracts all member types (Employee, Spouse, Children, Parents)
- Includes age ranges, member counts, and coverage details
- Captures corporate buffer and critical illness information

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
    print(f"Sublimit: {member['Sub_Limit']}")
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
- **Policy Analysis**: Understanding coverage details and limitations
- **Risk Assessment**: Evaluating sublimits and coverage amounts
- **Compliance**: Ensuring all required fields are captured
- **Reporting**: Generating structured data for business intelligence
- **Automation**: Reducing manual processing of policy documents

The extracted data supports business analysts in making informed decisions about insurance coverage and policy comparisons.
