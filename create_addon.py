import re
from typing import List, Dict

def create_addon(text: str) -> List[Dict[str, str]]:
    """
    Analyzes the provided text to determine the status of various add-on covers.
    This function is NOT responsible for Excel formatting.
    """
    ADDON_COVER_HEADERS = [
        "Ambulance Cover", "Anyone Illness", "Attendant Care", "Cancer Cover",
        "Convalescence Benefit", "Critical Illness Benefit", "Daily/Hospital Cash Benefit",
        "Dental Cover", "Diabetic Cover", "Doctor & Nurse Home Visit Cover",
        "Education Fund", "Funeral", "Getwell Benefit", "Hardship Critical Illness Cover",
        "Health Check up", "Hypertension Cover", "Intensive Care Benefit",
        "Loss Of Pay Cover", "Medical Evacuation Cover", "Medical Second Opinion",
        "Non Medical Expense Cover", "Out Patient Cover", "Optical Cover",
        "Organ Donor Medical Expense Cover", "Personal Accident Cover",
        "Pre Existing Disease Benefit", "Psychiatric Cover", "Recovery Benefit",
        "Referral Hospital Care", "Surgical Benefit", "Top Up Cover",
        "Vaccination/Immunization Cover"
    ]

    SEARCH_KEYWORD_MAP = {
        "Ambulance Cover": ("Endorsement 16", "Endt. No. 16"),
        "Convalescence Benefit": ("Endorsement 15", "Endt. No. 15"),
        "Critical Illness Benefit": ("Endorsement 20", "Endt. No. 20"),
        "Daily/Hospital Cash Benefit": ("Endorsement 14", "Endt. No. 14", "Hospital Cash Allowance"),
        "Doctor & Nurse Home Visit Cover": ("Endorsement 17", "Endt. No. 17"),
    }

    addon_results = {header: "No" for header in ADDON_COVER_HEADERS}

    if not text:
        return [addon_results]

    normalized_text = text.lower()

    for cover_name, search_terms in SEARCH_KEYWORD_MAP.items():
        if cover_name in addon_results:
            found = False
            for term in search_terms:
                cleaned_term = term.lower().replace('.', r'\.').replace(' ', r'\s*')
                pattern = r'\b' + cleaned_term + r'\b'
                if re.search(pattern, normalized_text):
                    found = True
                    break
            if found:
                addon_results[cover_name] = "Yes"

    return [addon_results]
