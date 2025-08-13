# Royal Sundaram H-Scope Automation Project

This README is the central catalog of business rules. Each epic links to the live code that implements its logic.

---

## Epic E-1.2: Eligibility

### EPIC 1.2: Sublimit & Buffer Configuration (K -W)

*   **Business Logic:** Extracts Sublimit_type and Sublimt from insurance policy documents. Processes Endorsement No. 5(i) and 5(ii) for 

*   **Live Code Location:** `extract_Eligibility.py`

*   **Direct Code Link:** **[View Function `extract_Eligibility()` on GitHub]([https://github.com/your-org/your-repo/blob/main/extract_Eligibility.py#L373-L834](https://github.com/sbasadeesh/royalsundaram-Claim-processing/tree/Epic1.2))**

#### Core Field Logic Documentation

**Essential Fields Extraction Logic:**

##### 1. Sublimit_Type & Sub_Limit Fields

**Pattern Detection:**
- **Primary Source:** Endorsement No. 5(i) and Endorsement No. 5(ii) sections
- **Detection Method:** `extract_sublimits_from_endorsement_5i()` and `extract_all_sublimits_from_endorsement_5ii()`
- **Regex Patterns:**
  ```python
  # Endt. No. 5(i) patterns
  r'Endt\.\s*No\.\s*5\(i\).*?(?=Endt\.\s*No\.|Endorsement\s*No\.|$)'
  
  # Endt. No. 5(ii) patterns  
  r'Endt\.\s*No\.\s*5\(ii\).*?(?=Endt\.\s*No\.|Endorsement\s*No\.|$)'
  ```

**Business Rules:**
- **First Sublimit:** Only the Employee row contains the first sublimit type and amount
- **Additional Sublimits:** If multiple sublimits exist, additional Employee rows are created for each subsequent sublimit
- **Other Members:** Spouse, Children, Parents rows have empty sublimit fields
- **Format Detection:** Automatically detects between "Merged" and "Individual" formats based on text patterns

**Sublimit Types Extracted:**
1. **Room, Boarding Expenses** - Percentage-based calculation from Endt. No. 5(i)
2. **Intensive Care Unit** - Percentage-based calculation from Endt. No. 5(i)
3. **Cataract** - Special handling for "Nil Capping" scenarios
4. **Treatment of mental illness** - Individual condition extraction
5. **Stress or psychological disorders** - Individual condition extraction
6. **Neurodegenerative disorders** - Individual condition extraction
7. **Balloon Sinsuplasty** - Merged condition handling
8. **Bronchial Thermoplasty** - Merged condition handling
9. **Vaporization of prostate** - Merged condition handling
10. **Intra Operative Neuro Monitoring** - Merged condition handling
11. **Intra vitreal injections** - Merged condition handling
12. **Stem Cell therapy** - Hematopoietic stem cells for bone marrow transplant
13. **Oral Chemotherapy** - Individual condition extraction
14. **Immunotherapy** - Individual condition extraction


extract_sublimits_from_endorsement_5i

This function extracts the specific financial limits (sublimits) for Room, Boarding Expenses and Intensive Care Unit (ICU) from a section of a policy document titled "Endt. No. 5(i)."

Logic: It first identifies the entire Endt. No. 5(i) section using regular expressions.

Extraction: Within that section, it searches for patterns that indicate a percentage for "Room, Boarding Expenses" and "Intensive Care Unit."

Calculation: Assuming a Sum Insured of ₹500,000, it calculates the sublimit amount by applying the extracted percentage.

Return Value: It returns a list of dictionaries, where each dictionary represents a sublimit (e.g., {"type": "Room, Boarding Expenses", "limit": "50000"}).

##### 2. Family Buffer Applicable & Family Buffer Amount

**Pattern Detection:**
- **Source:** Endorsement No. 1 section
- **Regex Pattern:** `r'limit of Rs[\.:]?\s?([\d,]+)'`
- **Business Logic:** Extracted from general buffer limits in eligibility section

**Field Mapping:**
```python
"Family Buffer Applicable": corporate_buffer_applicable,  # "Yes" if Endt. No. 10 found
"Family Buffer Amount": corporate_buffer_limit_family,    # Amount from Endt. No. 10
```

##### 3. Is Network Applicable

**Business Rule:**
- **Fixed Value:** Always set to "No" for all member types
- **Logic:** `"Is Network Applicable": "No"`

##### 4. Black listed hospitals are applicable?

**Business Rule:**
- **Fixed Value:** Always set to "Yes" for Employee row
- **Logic:** `"Black listed hospitals are applicable?": "Yes"`
- **Other Members:** Empty for Spouse, Children, Parents rows

##### 5. Corporate Buffer applicable

**Pattern Detection:**
- **Source:** Endorsement No. 10 section
- **Function:** `extract_corporate_buffer_applicability()`
- **Regex Pattern:** `r'(Endt\.|Endorsement)\s*No\.?\s*10\b'`

**Business Rules:**
- **Applicability:** "Yes" if Endt. No. 10 exists in policy text
- **Employee Row:** Populated only in Employee relationship row
- **Other Members:** Empty for all other member types

##### 6. Buffer Type

**Business Rules:**
- **Value:** "Both" when Corporate Buffer applicable = "Yes"
- **Logic:** `"Buffer Type": "Both" if corporate_buffer_applicable == "Yes" else ""`
- **Employee Row:** Only populated in Employee row
- **Other Members:** Empty for all other member types

##### 7. Applicable for

**Business Rule:**
- **Value:** Always empty string
- **Logic:** `"Applicable for": ""`

##### 8. Total Corporate Buffer

**Business Rules:**
- **Employee Row:** Contains corporate buffer limit family amount
- **Logic:** `corporate_buffer_limit_family if corporate_buffer_applicable == "Yes" != 0 else ""`
- **Other Members:** Empty for all other member types

##### 9. Corporate Buffer Limit Per Family

**Pattern Detection:**
- **Source:** Endorsement No. 10 section
- **Regex Patterns:**
  ```python
  r'limit\s+of\s+Rs[\.:]?\s?([\d,]+).*?corporate\s+(?:buffer|floater)'
  r'corporate\s+buffer\s+limit\s+per\s+family.*?Rs[\.:]?\s?([\d,]+)'
  ```

**Business Rules:**
- **Extraction:** Monetary amount from corporate buffer/floater limits
- **Employee Row:** Populated with extracted amount
- **Other Members:** Empty for all other member types

##### 10. Corporate Buffer Limit Per Parent

**Pattern Detection:**
- **Source:** Endorsement No. 10 section
- **Regex Pattern:** `r'corporate\s+buffer\s+limit\s+per\s+parent.*?Rs[\.:]?\s?([\d,]+)'`

**Business Rules:**
- **Extraction:** Separate limit specifically for parent coverage
- **Employee Row:** Populated with extracted amount
- **Other Members:** Empty for all other member types

##### 11. Reload of SI

**Pattern Detection:**
- **Source:** Endorsement No. 10 section
- **Trigger:** Presence of "per person limit" text
- **Pattern Mapping:**
  ```python
  # Pattern detection logic
  equivalent_pattern = r'equivalent\s+to\s+the\s+per\s+person\s+limit'
  double_pattern = r'double\s+to\s+the\s+per\s+person\s+limit'
  thrice_pattern = r'thrice\s+to\s+the\s+per\s+person\s+limit'
  ```

**Business Rules:**
- **Default Value:** "No limit for the reload of SI"
- **Pattern Mapping:**
  - "equivalent to the Per person limit" → "Reload of SI is up to the Existing SI"
  - "Double to the Per person limit" → "Reload of SI is up to the Double the SI"
  - "Thrice to the Per person limit" → "Reload of SI is up to the Thrice the SI"
- **Employee Row:** Only populated in Employee row
- **Other Members:** Empty for all other member types

#### Row Structure Logic

**Employee Row (Primary):**
- Contains ALL comprehensive data including first sublimit
- Corporate buffer fields populated when applicable
- Critical illness fields populated when applicable
- Network and blacklist fields set to fixed values

**Additional Employee Rows (Sublimits):**
- Created for each additional sublimit beyond the first
- Contains only sublimit-specific data (Sublimit_Type, Sub_Limit)
- All other fields remain empty

**Family Member Rows (Spouse, Children, Parents):**
- Basic demographic information only (age ranges, member counts)
- Sublimit_Applicable set to "yes" but no specific sublimit data
- All corporate buffer and critical illness fields remain empty
- Network and blacklist fields remain empty

---

## Epic Template

### E1.3 - Advanced Buffer & Critical Illness Configuration

---

✅ 1. Description & Logic Location

- **Description:** Extracts comprehensive corporate buffer and critical illness configuration from insurance policy documents. Processes Endorsement No. 10 for corporate buffer details and scans the entire policy text for critical illness provisions.
- **README Link:** [Link to README Section](#epic-13-advanced-buffer--critical-illness-configuration-x-ao)

---

✅ 2. Mandatory Pre-Submission Checklist

- [ ] 100% Accuracy: Output matches the official test data (values, types, formats).
- [ ] 100% Performance: Performance tests for this entire Epic have passed.
- [ ] README Updated: The `README.md` file is updated with this epic's logic.
- [ ] Queries Logged: All questions have been documented in Odoo as required.

---

✅ 3. Evidence

- **Accuracy Report:** (Attach screenshot showing matching values)
- **Performance Report:** (Attach screenshot showing 100% score)

---

✅ 4. Reviewers

Ready for review by @Sadeesh and @Venkatesh
