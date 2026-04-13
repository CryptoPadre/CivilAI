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

JOB_SALARY = {
    # Manual
    "Baker": 18,
    "Butcher": 20,
    "Farmer": 15,
    "Fisherman": 17,
    "Miner": 25,
    "Factory Worker": 22,
    "Construction Worker": 24,
    "Cleaner": 14,
    "Warehouse Worker": 20,
    "Delivery Driver": 21,

    # Service
    "Retail Worker": 18,
    "Cashier": 16,
    "Waiter": 17,
    "Barista": 16,
    "Receptionist": 19,
    "Security Guard": 22,
    "Janitor": 15,
    "Hairdresser": 23,
    "Taxi Driver": 24,
    "Cook": 22,

    # Skilled
    "Teacher": 35,
    "Nurse": 38,
    "Doctor": 70,
    "Engineer": 60,
    "Mechanic": 40,
    "Electrician": 42,
    "Plumber": 45,
    "Architect": 55,
    "Pharmacist": 50,
    "Accountant": 48,

    # Creative
    "Artist": 25,
    "Musician": 30,
    "Writer": 28,
    "Journalist": 32,
    "Photographer": 27,
    "Designer": 35,
    "Actor": 50,
    "Chef": 45,
    "Influencer": 40,
    "Game Developer": 55,

    # Government
    "Police Officer": 35,
    "Firefighter": 38,
    "Soldier": 30,
    "Military Officer": 50,
    "Judge": 80,
    "Lawyer": 75,
    "Politician": 85,
    "Mayor": 70,
    "Bank Manager": 65,

    # Top
    "CEO": 120,
    "Investor": 100,
    "Scientist": 70,
    "Professor": 65,
    "Researcher": 60,
    "Pilot": 90,
    "Air Traffic Controller": 85,
    "Detective": 55,
    "Psychologist": 50,
    "Economist": 60,

    # Illegal
    "Unemployed": 0,
    "Criminal": 10,
    "Thief": 15,
    "Hacker": 40,
    "Smuggler": 35,
    "Informant": 25,
    "Gang Member": 20,
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
  
    if npc.salary == 0 and npc.occupation != "Unemployed":
        base = JOB_SALARY.get(npc.occupation, 20)
        npc.salary = base * npc.job_level

    return npc