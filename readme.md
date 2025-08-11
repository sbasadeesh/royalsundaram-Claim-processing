Epic-2.1: 
Business Logic:
Determines whether the maternity benefit is applicable based on “Endorsement No. 11(b) Maternity Treatment Charges Benefit Extension” or other references in the policy text.
The Benefit Applicable? field defaults to "Yes" regardless of whether the endorsement section is found, ensuring that benefits are treated as applicable unless the extraction logic explicitly sets it to "No".
This value is later used by other benefit-specific calculations and display logic in the system.

Live Code Location:
extract_primary_data.py → extract_maternity_from_endt_11b()

Direct Code Link:
View Function extract_maternity_from_endt_11b() on GitHub

Code Snippet
python
Copy
Edit
def extract_maternity_from_endt_11b(text: str) -> Dict:
    """Extract maternity data specifically from Endorsement No. 11(b)"""
    maternity_data = {
        "Benefit Applicable?": "Yes",  # Always defaults to "Yes"
        ...
    }

    endorsement_11b_match = re.search(
        r'Endt\.\s*No\.\s*11\s*\(b\)\s*Maternity Treatment Charges Benefit Extension.*?(?=Endt\.\s*No\.|Endorsement\s*No\.|Group Health Policy|$)',
        text, re.IGNORECASE | re.DOTALL
    )

    if not endorsement_11b_match:
        # Even if section not found, keep default "Yes"
        return maternity_data

    # Additional extraction logic...
    return maternity_data

Direct Code Link: [View Function extract_maternity_from_endt_11b() on GitHu](https://github.com/sbasadeesh/royalsundaram-Claim-processing/blob/Epic2.1/extract_primary_data.py)b
