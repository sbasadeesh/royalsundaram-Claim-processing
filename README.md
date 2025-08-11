# Royal Sundaram H-Scope Automation Project

This README is the central catalog of business rules. Each epic links to the live code that implements its logic.

---

## Epic E-1.0: Eligibility

### EPIC 1.3: Advanced Buffer & Critical Illness Configuration (X-AO)

*   **Business Logic:** Extracts comprehensive corporate buffer and critical illness configuration from insurance policy documents. Processes Endorsement No. 10 for corporate buffer details and scans the entire policy text for critical illness provisions.

*   **Live Code Location:** `extract_Eligibility.py`

*   **Direct Code Link:** **[View Function `extract_Eligibility()` on GitHub](https://github.com/sbasadeesh/royalsundaram-Claim-processing/tree/Epic1.3)**

#### Corporate Buffer Extraction (Lines 533-572)

**Pattern Detection:**
- Searches for `Endt\.\s*No\.\s*10` sections in policy text
- Identifies corporate buffer/floater keywords using regex: `r'corporate\s+(?:buffer|floater)'`
- Extracts monetary limits with pattern: `r'limit\s+of\s+Rs[\.:]?\s?([\d,]+)'`

**Business Rules:**
- **Buffer Applicability:** Determined by presence of Endorsement No. 10
- **Family Limit:** Extracted from "corporate buffer limit per family" or general floater limit
- **Parent Limit:** Separate extraction for "corporate buffer limit per parent"
- **Reload Logic:** Detects "per person limit" patterns to set reload options
- **OPD Buffer:** Searches for "buffer opd limit" with monetary values

**Field Mapping:**
```python
"Total Plan Buffer": corporate_buffer_limit_family,
"Corporate Buffer Limit for Employee/Family": corporate_buffer_limit_family,
"Corporate Buffer Limit Per Parent": corporate_buffer_limit_parent,
"Reload of SI": reload_of_si,  # Default: "No limit for the reload of SI"
"Approving Authority": "Corporate HR",
"Buffer OPD Limit": buffer_opd_limit,
"Whether increase in sum insured permissible at renewal": "No"
```

#### Critical Illness Detection (Lines 573-589)

**Pattern Detection:**
- Scans entire policy text for `r'critical\s+illness'` keyword
- Extracts family limits with: `r'critical\s+illness\s+limit\s+per\s+family.*?Rs[\.:]?\s?([\d,]+)'`
- Fallback pattern: `r'critical\s+illness.*?limit.*?Rs[\.:]?\s?([\d,]+)'`

**Business Rules:**
- **Applicability:** Set to "Yes" if critical illness keyword found anywhere in policy
- **Limit Extraction:** Prioritizes family-specific limits over general limits
- **Authority Assignment:** Automatically assigns "Corporate HR" as approving authority when applicable

**Field Mapping:**
```python
"Critical Illness applicable": "Yes/No",
"Critical Illness limit per family": critical_illness_limit_family,
"Critical Illness Approving Authority": "Corporate HR",
"Critical Illness Whether increase in sum insured permissible at renewal": ""
```

#### Data Population Strategy

**Main Employee Row (Lines 620-648):**
- Only the Employee relationship row contains complete buffer and critical illness data
- All other family member rows (Spouse, Son, Daughter, etc.) have empty values for these fields
- Ensures centralized configuration while maintaining relational structure

**Validation Logic:**
- Corporate buffer fields populated only when `corporate_buffer_applicable == "Yes"`
- Critical illness authority assigned only when `critical_illness_applicable != "No"`
- Monetary values extracted as integers with comma removal: `int(match.group(1).replace(',', ''))`
