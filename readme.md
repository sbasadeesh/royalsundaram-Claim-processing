Epic P-2.0: Primary Covers
P-2.1: Maternity Benefit
Business Logic: Extracts and determines maternity coverage details from “Endorsement No. 11(b) Maternity Treatment Charges Benefit Extension” and other policy text. Defaults Benefit Applicable? to "Yes", even if the endorsement text is not found. Identifies the waiting period, limit on the number of live children, contribution/copay/deductible terms, and whether the benefit is combined or separate for Normal and Caesarean deliveries. Captures sum insured, percentage limits, and specific Normal/Caesarean limit amounts. Defaults are applied when values are absent in the policy text.

Live Code Location: extract_primary_data.py → extract_maternity_from_endt_11b()

Direct Code Link: [View Function extract_maternity_from_endt_11b() on GitHu](https://github.com/sbasadeesh/royalsundaram-Claim-processing/blob/Epic2.1/extract_primary_data.py)b
