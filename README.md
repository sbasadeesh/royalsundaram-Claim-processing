Epic 3.4: Doctor's Home Visit & Nursing Charges in Addon Coverages
Business Logic: This epic expands the addon coverage extraction system. It introduces the logic to process Endt. No. 17 - Home Nursing Allowance and integrates it alongside the existing Ambulance and Convalescence benefits. The process is as follows:

Status Identification: The system first checks for the presence of Endt. No. 17 in the policy text to determine if the "Doctor Nurse Home Visit Cover" is active. This is handled in the create_addon.py file.

Targeted Extraction: For an active endorsement, the system isolates the relevant text block and uses specific regular expressions to find key values:

Limit amount: Extracted from the "daily allowance of Rs. [amount]" clause (e.g., Rs. 1,000).

No of days Allowed: Extracted from the "maximum [X] days" clause (e.g., 10 days).

Calculation & Default Values:

Applicable On?: Determined based on keywords. If "following discharge" is present, it is set to "Post Hospitalization".

% Limit Applicable On: This defaults to the policy's Sum Insured (e.g., 500,000).

Limit Percentage: Calculated using the formula: (Limit amount / % Limit Applicable On). For example, (1,000 / 500,000) results in 0.20%.

Excel Template Generation: The system generates a new table titled "Applicability of Doctor's Home Visit & Nursing Charges" in the Addon Coverages sheet, correctly populating it with the extracted and calculated data.

Live Code Location: create_addon_coverages.py.

Direct Code Link: https://github.com/sbasadeesh/royalsundaram-Claim-processing/blob/main/create_addon.py
