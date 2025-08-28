from enum import Enum

# -------------------------------
# Existing constants
# -------------------------------
NOTE_TYPE_MAP = {
    "Therapist": ["Session Note", "Progress Note"],
    "Counselor": ["Session Note", "Progress Note"],
    "Patient": ["Client Note"]
}

# -------------------------------
# New Enums for Expand API
# -------------------------------
class Audience(str, Enum):
    school_staff = "school_staff"
    therapist = "therapist"
    student = "student"
    parent = "parent"

class Tone(str, Enum):
    neutral_clinical = "neutral_clinical"
    supportive = "supportive"
    plain_language = "plain_language"
    culturally_sensitive = "culturally_sensitive"
    formal_report = "formal_report"
    student_friendly = "student_friendly"
    parent_friendly = "parent_friendly"
    crisis_informational = "crisis_informational"

# -------------------------------
# Defaults for Expand API
# -------------------------------
DEFAULT_TARGET_WORDS = 320
DEFAULT_READING_LEVEL = "grade10"
DEFAULT_INCLUDE_CA_CONTEXT = True

# Model to load locally / Azure
MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"
# MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"


# -------------------------------
# Safety disclaimer
# -------------------------------
EDU_DISCLAIMER = (
    "This expanded text is for illustrative and educational purposes only. "
    "It is not a substitute for professional mental health advice, diagnosis, or treatment. "
    "Students and families in California should consult qualified school-based mental health professionals "
    "or licensed providers for personal guidance. "
    "If you or someone you know is in immediate distress or at risk of harm, call or text 988 in the U.S. "
    "or contact local emergency services right away."
)

"""
DROPDOWNS
---------

Audience:
---------
school_staff, therapist, student, parent

Tone:
-----
neutral_clinical (default)
supportive
plain_language
culturally_sensitive
formal_report
student_friendly
parent_friendly
crisis_informational (educational, non-directive; reminds to seek help/988)
"""
