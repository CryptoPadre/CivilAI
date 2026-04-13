import random
from civilAI.npc.models import Npc

# -------------------------
# JOB CATEGORIES
# -------------------------
JOBS = {
    "Manual Jobs": [
        "Baker", "Butcher", "Farmer", "Fisherman", "Miner",
        "Factory Worker", "Construction Worker", "Cleaner",
        "Warehouse Worker", "Delivery Driver",
    ],
    "Service Jobs": [
        "Retail Worker", "Cashier", "Waiter", "Barista",
        "Receptionist", "Security Guard", "Janitor",
        "Hairdresser", "Taxi Driver", "Cook"
    ],
    "Skilled Jobs": [
        "Teacher", "Nurse", "Doctor", "Engineer", "Mechanic",
        "Electrician", "Plumber", "Architect", "Pharmacist", "Accountant"
    ],
    "Creative Jobs": [
        "Artist", "Musician", "Writer", "Journalist", "Photographer",
        "Designer", "Actor", "Chef", "Influencer", "Game Developer"
    ],
    "Government Jobs": [
        "Police Officer", "Firefighter", "Soldier", "Military Officer",
        "Judge", "Lawyer", "Politician", "Mayor", "Bank Manager"
    ],
    "Top Jobs": [
        "CEO", "Investor", "Scientist", "Professor", "Researcher",
        "Pilot", "Air Traffic Controller", "Detective",
        "Psychologist", "Economist"
    ],
    "Illegal Jobs": [
        "Unemployed", "Criminal", "Thief", "Hacker",
        "Smuggler", "Informant", "Gang Member"
    ]
}

# -------------------------
# PERSONALITY → CATEGORY BIAS
# -------------------------
PERSONALITY_EFFECTS = {
    "Hardworking": ["Manual Jobs", "Service Jobs"],
    "Lazy": ["Illegal Jobs"],

    "Creative": ["Creative Jobs"],
    "Curious": ["Skilled Jobs", "Service Jobs"],

    "Brave": ["Government Jobs"],
    "Cowardly": ["Manual Jobs"],

    "Friendly": ["Service Jobs", "Skilled Jobs"],
    "Rude": ["Illegal Jobs", "Manual Jobs", "Government Jobs"],

    "Empathetic": ["Service Jobs", "Skilled Jobs"],
    "Cruel": ["Illegal Jobs", "Government Jobs"],

    "Greedy": ["Top Jobs", "Illegal Jobs", "Government Jobs"],
    "Honest": ["Manual Jobs", "Service Jobs", "Skilled Jobs", "Government Jobs", "Top Jobs"]
}

# -------------------------
# DEGENERATIVE CONDITIONS (SOFT BIAS, NOT LOCKS)
# -------------------------
DEGENERATIVE_EFFECTS = {
    "sociopath": ["Government Jobs", "Top Jobs", "Skilled Jobs"],
    "psychopath": ["Government Jobs", "Top Jobs", "Skilled Jobs", "Creative Jobs"],
    "narcissist": ["Top Jobs", "Government Jobs", "Creative Jobs"],
    "paranoid": ["Manual Jobs", "Service Jobs"],
    "pedophile": ["Manual Jobs", "Service Jobs"],
    "none": ["Manual Jobs", "Service Jobs", "Skilled Jobs", "Government Jobs", "Top Jobs", "Creative Jobs"]
}

# -------------------------
# MAIN FUNCTION
# -------------------------
def assign_job_by_traits(npc):
    # -------------------------
    # UNDERAGE RULE
    # -------------------------
    if npc.age < 18:
        npc.occupation = "Unemployed"
        return npc

    traits = npc.personality_traits or []
    condition = getattr(npc, "degenerative_condition", "none")

    # -------------------------
    # 1. DEGENERATIVE BIAS (WEIGHTED, NOT HARD OVERRIDE)
    # -------------------------
    category_scores = {}

    for c in DEGENERATIVE_EFFECTS.get(condition, []):
        category_scores[c] = category_scores.get(c, 0) + 2  # strong bias

    # -------------------------
    # 2. PERSONALITY BIAS
    # -------------------------
    for trait in traits:
        for category in PERSONALITY_EFFECTS.get(trait, []):
            category_scores[category] = category_scores.get(category, 0) + 1

    # -------------------------
    # 3. FALLBACK IF EMPTY
    # -------------------------
    if not category_scores:
        category_scores = {
            "Manual Jobs": 1,
            "Service Jobs": 1
        }

    # -------------------------
    # 4. SOFT SELECTION (MORE REALISTIC THAN HARD PICK)
    # -------------------------
    total = sum(category_scores.values())
    roll = random.uniform(0, total)

    cumulative = 0
    selected_category = None

    for cat, score in category_scores.items():
        cumulative += score
        if roll <= cumulative:
            selected_category = cat
            break

    # safety fallback
    if not selected_category:
        selected_category = random.choice(list(JOBS.keys()))

    # -------------------------
    # 5. FINAL JOB PICK
    # -------------------------
    npc.occupation = random.choice(JOBS[selected_category])

    return npc