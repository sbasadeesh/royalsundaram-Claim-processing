Epic 3.1: Addon Cover Automation
Business Logic:
This system automates the extraction and processing of addon coverages from insurance policy PDFs, focusing on "Ambulance Cover" (Endt. 16) and "Convalescence Benefit" (Endt. 15). The logic follows a precise, multi-step process:

Status Identification: The system first determines if a cover is active by searching the entire document for specific endorsement numbers (e.g., Endt. No. 16). This determines the "Yes" or "No" status in the Addon Covers sheet.

Targeted Text Isolation: To ensure accuracy, the system isolates the specific text block belonging to each active endorsement. For example, it will capture all text associated with "Endt. No. 16" before attempting to extract its details. This prevents the system from incorrectly capturing values from other parts of the document.

Value Extraction: Within the isolated text block, the system uses regular expressions (regex) to find and extract key numerical values, such as the limit of Rs. 2,000 for the Ambulance Cover.

Limit Percentage Calculation: The "Limit Percentage" for the Ambulance Cover is calculated using the following formula:

Limit Percentage = (Limit Amount / Policy Sum Insured)
For example: (2,000 / 500,000) = 0.004. This value is then formatted as 0.40% in the final Excel report.

Handling of Multiple Endorsements: The system is designed to find all occurrences of an endorsement. If a PDF contains two separate "Endt. No. 16" clauses, it will extract the details from both and create two corresponding data rows in the final report.

Template Consistency: To maintain a consistent report structure, a table for each addon cover is always generated in the Addon Coverages sheet. If a cover's status is "No" or if its values cannot be extracted, its table is still displayed with empty cells.

Live Code Location: create_addon_coverages.py

Direct Code Link: https://github.com/sbasadeesh/royalsundaram-Claim-processing/blob/Epic3.2/create_addon_coverages.py
