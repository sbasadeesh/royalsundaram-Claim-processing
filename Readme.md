
## **E2.4 – Pre & Post Natal Extraction Logic**

### **Description**

This function **`extract_pre_post_natal_from_endt_11b(text: str) -> Dict`** is responsible for extracting **Pre-Natal** and **Post-Natal** benefit information from **Endorsement 11b** and **Special Conditions** sections of the policy text.

It handles:

* Determining whether **Pre-Natal** and **Post-Natal** benefits are applicable.
* Identifying **combined vs separate limits** for Pre & Post Natal expenses.
* Extracting **sum insured**, **limits**, **applicability**, **copay/deductible**, **member contribution**, **waiting periods**, and **number of children limits**.
* Recognizing whether benefits are **over & above maternity limits** or **within maternity limits**.

---

### **Logic Flow**

#### **1. Initialize Default Data**

* Pre-fills a dictionary (`pre_post_natal_data`) with default `"No"`, `"0"`, or empty values for all Pre-Natal, Post-Natal, and combined benefit fields.
* This ensures that **if no match is found** in the policy text, the output remains consistent and predictable.

#### **2. Extract Relevant Policy Sections**

* Uses regex to locate **Endorsement 11b** and **Special Conditions** text.
* Merges them into `analysis_text` for processing.

#### **3. Determine Benefit Applicability**

* Searches for variations of `"pre-natal and post-natal"` patterns in text.
* If found, sets:

  ```python
  "Pre-Natal Benefit Applicable?" = "Yes"
  "Post-Natal Benefit Applicable?" = "Yes"
  "Pre-Post-Natal Benefit Applicable?" = "Yes"
  ```

#### **4. Over & Above Maternity Limit Check**

* Looks for phrases like `"over above maternity limit"` to determine if this benefit is separate from the maternity limit.
* Extracts numeric value if specified (e.g., `"Rs. 50,000"`).

#### **5. Coverage Restriction Check**

* If coverage is only for **in-patient hospital cases**, sets `"Pre-Natal and Post-Natal Expenses Covered"` to `"No"`.
* Otherwise, `"Yes"` if explicitly covered.

#### **6. Default Day Limits & Applicability**

* Sets **Pre-Natal No. of Days** = `30`
* Sets **Post-Natal No. of Days** = `60`
* Applicability = `"Lower"` unless otherwise stated.

#### **7. Sum Insured Extraction**

* Searches for `"Corporate floater"` or `"main policy"` sum insured and assigns it to both Pre & Post Natal.

#### **8. Maternity Limit Extraction & % Calculation**

* Finds `"limited to Rs. XXX"` and calculates percentage limit for both Pre & Post Natal based on `Sum Insured / Maternity Limit * 100`.

#### **9. Pre & Post Natal Limit Extraction**

* Looks for `"pre & post natal limit"` or `"sublimit"` and assigns the amount to both Pre & Post Natal limits.
* Also calculates `"Pre-Natal Limit Calc Percentage"` as `(Limit / 500000) * 100`.

#### **10. Copay & Deductible Extraction**

* If `"X% admissible"` → Sets copay percentage.
* If `"deductible Rs. XXX"` → Sets deductible amount.

#### **11. Member Contribution**

* If `"member contribution"` found, sets `"Yes"`.

#### **12. Waiting Period & Children Limit**

* Extracts `waiting period (days)` and `max number of children covered`.

---

### **Example Output**

```python
{
  "Pre-Natal Benefit Applicable?": "Yes",
  "Pre-Natal Waiting Period": "30",
  "Pre-Natal Limit On Children": "2",
  "Pre-Natal Member Contribution": "No",
  "Pre-Natal Copay/Deductible": "Copay",
  "Pre-Natal Is Combined": "No",
  "Pre-Natal Sum Insured": "500000",
  "Pre-Natal % Limit": "100.0",
  "Pre-Natal Limit": "25000",
  "Pre-Natal Applicability": "Lower",
  "Pre-Natal Copay": "10",
  "Pre-Natal Deductible": "",
  "Pre-Natal No of Days": "30",
  "Pre-Natal % Limit Applicable On": "Sum Insured",
  
  "Post-Natal Benefit Applicable?": "Yes",
  "Post-Natal Waiting Period": "30",
  "Post-Natal Limit On Children": "2",
  "Post-Natal Member Contribution": "No",
  "Post-Natal Copay/Deductible": "Copay",
  "Post-Natal Is Combined": "No",
  "Post-Natal Sum Insured": "500000",
  "Post-Natal % Limit": "100.0",
  "Post-Natal Limit": "25000",
  "Post-Natal Applicability": "Lower",
  "Post-Natal Copay": "10",
  "Post-Natal Deductible": "",
  "Post-Natal No of Days": "60",
  "Post-Natal % Limit Applicable On": "Sum Insured",
  
  "Pre-Post-Natal Benefit Applicable?": "Yes",
  "Over-Above-Maternity Applicable?": "No",
  "Over-Above-Maternity Limit": "",
  
  "Pre-Natal and Post-Natal Expenses Covered": "Yes",
  "Over-Above-Maternity Limit Applicable": "No"
}
```

---


