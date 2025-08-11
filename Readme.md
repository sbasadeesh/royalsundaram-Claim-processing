Excel Validation and Reporting Automation

This README is the central catalog of business rules and validation logic for the Excel Validator Tool. Each epic links to the live code that implements its logic.

Epic V-1.0: Core Validation Logic
V-1.1: Header Validation
Business Logic: Compares the header text in Row 3 of the input template against Row 3 of the output file. It flags any cell where the text value does not match exactly. This check ensures structural accuracy.

Live Code Location: src/excel_validator.py

Direct Code Link: https://github.com/sbasadeesh/royalsundaram-Claim-processing/blob/Testing/main.py

V-1.2: Data Type Validation
Business Logic: Reads the data type rules (e.g., Numeric, Text, Binary(Yes/No)) from Row 4 of the input template. It then validates every data cell from Row 4 downwards in the output file to ensure it conforms to the corresponding rule.

Live Code Location: src/excel_validator.py

Direct Code Link: https://github.com/sbasadeesh/royalsundaram-Claim-processing/blob/Testing/main.py

Output File : [EPIC_1.1_Validation_Report_11-08-2025_05-58.xlsx](https://github.com/user-attachments/files/21709914/EPIC_1.1_Validation_Report_11-08-2025_05-58.xlsx)
