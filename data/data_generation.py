# Generate synthetic CSVs and SQL schema for the user's FastAPI project.
# Files created:
# - /mnt/data/tad_transcriber/data/students.csv
# - /mnt/data/tad_transcriber/data/notes_summary.csv
# - /mnt/data/tad_transcriber/data/notes_generation.csv
# - /mnt/data/tad_transcriber/db/schema.sql

import os, csv, random, uuid, datetime, textwrap, json
from pathlib import Path

# Try to use Faker for better names; fallback if unavailable.
try:
    from faker import Faker
    fake = Faker()
except Exception:
    class _MiniFake:
        first = ["Alex","Sam","Jamie","Jordan","Taylor","Morgan","Casey","Riley","Avery","Quinn",
                 "Noah","Liam","Mason","Ethan","Logan","Lucas","Emma","Olivia","Ava","Sophia"]
        last  = ["Kimani","Otieno","Mwangi","Mutiso","Njoroge","Omollo","Omondi","Kiptoo","Barasa","Cheruiyot",
                 "Smith","Brown","Wilson","Johnson","Davis","Miller","Garcia","Martinez","Lopez","Gonzalez"]
        def name(self):
            return f"{random.choice(self.first)} {random.choice(self.last)}"
    fake = _MiniFake()

BASE = Path("/tad_ai")
DATA = BASE / "data"
DB   = BASE / "db"
DATA.mkdir(parents=True, exist_ok=True)
DB.mkdir(parents=True, exist_ok=True)

# -------------------------
# CONFIG
# -------------------------
N_STUDENTS = 1200
NOTES_PER_STUDENT = 3  # avg
N_NOTES = N_STUDENTS * NOTES_PER_STUDENT  # 3600 >= 3000
N_GEN = 3200  # notes_generation

GENDERS = ["male", "female", "nonbinary"]
USER_TYPES = ["Therapist", "Counselor", "Patient"]
NOTE_TYPES = ["session_note", "progress_note"]
ISSUES = ["family_conflict","substance_use","low_self_esteem","academic_stress","anxiety",
          "depression","sleep_issues","bullying","grief","trauma"]
AUDIENCES = ["school_staff","therapist","student","parent"]
TONES = ["neutral_clinical","supportive","plain_language","culturally_sensitive",
         "formal_report","student_friendly","parent_friendly","crisis_informational"]

# Distributions: keep balanced by cycling rather than pure random
def cycle_pick(pool, i):
    return pool[i % len(pool)]

def cycle_multi_issues(index):
    # Ensure each issue appears roughly equally by rotating the start
    k = random.choice([1,2,3])  # 1-3 issues per note
    start = index % len(ISSUES)
    picks = []
    for j in range(k):
        picks.append(ISSUES[(start + j) % len(ISSUES)])
    return picks

def rand_sentence(words=12):
    # simple sentence builder if Faker isn't available
    parts = ["student","reports","concern","about","stress","and","home","situation","with","peers","and","exams"]
    return " ".join(random.sample(parts, min(len(parts), words))).capitalize() + "."

def make_transcript(issues_list):
    openings = [
        "Okay so this session focused on",
        "In today's conversation we explored",
        "The student described experiences related to",
        "We discussed current challenges including",
        "The session reviewed coping and support for",
    ]
    fillers = [
        "They noted patterns over the past few weeks and shared examples.",
        "We paused to check grounding and breathing before continuing.",
        "The student asked about ways to reduce worry during class hours.",
        "We also talked about how to involve safe supports when needed.",
        "The conversation stayed practical and respectful throughout.",
    ]
    sents = [
        f"{random.choice(openings)} {', '.join(issues_list).replace('_',' ')}.",
        "The goal was to understand triggers and plan small next steps.",
        random.choice(fillers),
        rand_sentence(10),
        rand_sentence(10),
    ]
    return " ".join(sents)

def make_summary(issues_list, user_type, note_type):
    header = "Session Note" if note_type == "session_note" else "Progress Note"
    focus = ", ".join(i.replace("_"," ") for i in issues_list)
    body = (f"{header}: Focused on {focus}. Validated feelings, identified triggers, "
            f"and reviewed coping strategies. {user_type} recommended brief, achievable actions "
            f"and documented safety resources. Student agreed to practice skills and report back.")
    return body

def make_prompt():
    return "Summarize the transcript into a structured clinical note (SOAP style) using neutral, respectful language."

def brief_from_issue(issue):
    mapping = {
        "family_conflict": "Student reports frequent arguments at home.",
        "substance_use": "Student mentions using alcohol on weekends due to stress.",
        "low_self_esteem": "Student says they don't feel good enough compared to peers.",
        "academic_stress": "Student feels overwhelmed by assignments and exams.",
        "anxiety": "Student experiences worry and physical tension before class.",
        "depression": "Student reports low mood and low motivation recently.",
        "sleep_issues": "Student has difficulty falling asleep and staying asleep.",
        "bullying": "Student reports being teased and excluded by peers.",
        "grief": "Student is grieving a recent loss in the family.",
        "trauma": "Student avoids reminders of a past distressing event.",
    }
    return mapping.get(issue, "Student reports a challenge and seeks support.")

def expand_text(brief, audience, tone):
    guidance = {
        "school_staff": "Focus on accommodations and classroom strategies.",
        "therapist": "Emphasize formulation, risk, and intervention planning.",
        "student": "Use encouraging, clear steps the student can try this week.",
        "parent": "Offer supportive, practical steps for home and communication.",
    }
    style = {
        "neutral_clinical": "Use objective, concise clinical language.",
        "supportive": "Use empathic language and normalize common reactions.",
        "plain_language": "Avoid jargon and keep sentences short and clear.",
        "culturally_sensitive": "Acknowledge cultural context and family values respectfully.",
        "formal_report": "Use formal structure with headings and bullet points.",
        "student_friendly": "Use simple, motivational language with concrete tips.",
        "parent_friendly": "Offer collaborative tone and step-by-step guidance.",
        "crisis_informational": "Include immediate safety steps and crisis contacts.",
    }
    paragraphs = [
        brief,
        guidance.get(audience, ""),
        style.get(tone, ""),
        "Next steps include identifying triggers, practicing coping skills, and connecting with trusted supports. Monitor progress and adjust as needed."
    ]
    return " ".join(p for p in paragraphs if p)

# -------------------------
# Generate students
# -------------------------
students_path = DATA / "students.csv"
with students_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["student_id","student_name","gender"])
    for sid in range(1, N_STUDENTS+1):
        name = fake.name()
        gender = cycle_pick(GENDERS, sid-1)
        w.writerow([sid, name, gender])

# -------------------------
# Generate notes_summary
# -------------------------
notes_path = DATA / "notes_summary.csv"
start_date = datetime.date.today() - datetime.timedelta(days=365)

with notes_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow([
        "uuid","student_id","notes","summary","prompt","user_type","note_type","issue","session_date"
    ])
    idx = 0
    for sid in range(1, N_STUDENTS+1):
        # 3 notes per student
        for s in range(NOTES_PER_STUDENT):
            note_uuid = str(uuid.uuid4())
            user_type = cycle_pick(USER_TYPES, idx)
            note_type = cycle_pick(NOTE_TYPES, idx)
            issues_list = cycle_multi_issues(idx)
            issues_csv = "{" + ",".join(issues_list) + "}"
            transcript = make_transcript(issues_list)
            summary = make_summary(issues_list, user_type, note_type)
            prompt = make_prompt()
            # spread dates evenly
            dt = start_date + datetime.timedelta(days=int((365/N_NOTES)*idx))
            w.writerow([note_uuid, sid, transcript, summary, prompt, user_type, note_type, issues_csv, dt.isoformat()])
            idx += 1

# -------------------------
# Generate notes_generation
# -------------------------
gen_path = DATA / "notes_generation.csv"
with gen_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["uuid","brief","notes","audience","tone","issue_tag"])
    for i in range(N_GEN):
        issue = cycle_pick(ISSUES, i)
        audience = cycle_pick(AUDIENCES, i)
        tone = cycle_pick(TONES, i)
        brief = brief_from_issue(issue)
        expanded = expand_text(brief, audience, tone)
        w.writerow([str(uuid.uuid4()), brief, expanded, audience, tone, issue])
