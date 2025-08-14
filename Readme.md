Excel Validator Automation Project


This README is the central catalog of business rules for the Excel Validator application. Each epic links to the live code that implements its specific logic.

Epic E-1.0: Core Validation Engine
E-1.1: Cell-by-Cell Comparison
Business Logic: This is the heart of the validator. It systematically compares two Excel files (Input Template and Output File) on a cell-by-cell basis. The engine iterates through each sheet and row, checking every non-empty cell in the template against the corresponding cell in the output file for both its data type and its value.

Epic C-2.0: Data Classification & Intelligence
C-2.1: Precise Data Type Identification
Business Logic: This function acts as the "brain" for identifying a cell's conceptual data type. It inspects the raw Excel number_format string and uses a prioritized series of checks to classify it precisely as Numeric, Currency, Accounting, Percentage, Date, Text, or General. This ensures that the data type validation is highly accurate.

Epic R-3.0: Reporting & Visualization
R-3.1: Multi-Sheet Summary Report
Business Logic: This module compiles all validation results into a comprehensive, multi-sheet Excel report. It generates a "QA Dashboard" with high-level accuracy KPIs, and two separate detailed sheets for "Data Type Results" and "Value Match Results".


R-3.2: Enhanced Readability & Formatting
Business Logic: To make the report easy to understand at a glance, this logic applies specific formatting rules. All cells in the report have text_wrap enabled. Most importantly, the headers are color-coded into distinct groups: Dark Blue for identifiers, Dark Red for data values, and Dark Green for results.

Live Code Location: main.py

Direct Code Link: https://github.com/sbasadeesh/royalsundaram-Claim-processing/blob/Testing/main.py

