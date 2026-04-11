from civilAI.npc.models import Npc
from django.utils import timezone
import random

JOBS = {
    # -------------------------
    # BASIC / MANUAL LABOR
    # -------------------------
    "Baker": {"intelligence": 1, "fitness": 1},
    "Butcher": {"fitness": 2},
    "Farmer": {"fitness": 2, "intelligence": 1},
    "Fisherman": {"fitness": 2},
    "Miner": {"fitness": 3},
    "Factory Worker": {"fitness": 2, "intelligence": 1},
    "Construction Worker": {"fitness": 3, "aggression": 1},
    "Cleaner": {},
    "Warehouse Worker": {"fitness": 2},
    "Delivery Driver": {"fitness": 1, "intelligence": 1},

    # -------------------------
    # SERVICE JOBS
    # -------------------------
    "Retail Worker": {"charisma": 1},
    "Cashier": {"intelligence": 1},
    "Waiter": {"charisma": 2, "empathy": 1},
    "Barista": {"charisma": 1},
    "Receptionist": {"charisma": 2},
    "Security Guard": {"fitness": 2, "aggression": 1},
    "Janitor": {},
    "Hairdresser": {"charisma": 2, "creativity": 1},
    "Taxi Driver": {"intelligence": 1, "charisma": 1},
    "Cook": {"intelligence": 1, "creativity": 1},

    # -------------------------
    # SKILLED PROFESSIONS
    # -------------------------
    "Teacher": {"intelligence": 3, "empathy": 2, "charisma": 1},
    "Nurse": {"empathy": 3, "intelligence": 2},
    "Doctor": {"intelligence": 3, "empathy": 3},
    "Engineer": {"intelligence": 3},
    "Mechanic": {"intelligence": 2, "fitness": 1},
    "Electrician": {"intelligence": 2},
    "Plumber": {"fitness": 1},
    "Architect": {"intelligence": 3, "creativity": 2},
    "Pharmacist": {"intelligence": 3},
    "Accountant": {"intelligence": 3},

    # -------------------------
    # CREATIVE / MEDIA
    # -------------------------
    "Artist": {"creativity": 3},
    "Musician": {"creativity": 3, "charisma": 2},
    "Writer": {"creativity": 3, "intelligence": 2},
    "Journalist": {"intelligence": 2, "charisma": 2},
    "Photographer": {"creativity": 2},
    "Designer": {"creativity": 3, "intelligence": 1},
    "Actor": {"charisma": 3, "creativity": 2},
    "Chef": {"creativity": 2, "intelligence": 1},
    "Influencer": {"charisma": 3},
    "Game Developer": {"intelligence": 3, "creativity": 2},

    # -------------------------
    # AUTHORITY / LAW / MILITARY
    # -------------------------
    "Police Officer": {"fitness": 3, "aggression": 2},
    "Firefighter": {"fitness": 3},
    "Soldier": {"fitness": 3, "aggression": 2},
    "Military Officer": {"intelligence": 2, "fitness": 2, "aggression": 1},
    "Judge": {"intelligence": 3, "morality": 3},
    "Lawyer": {"intelligence": 3, "charisma": 2},
    "Politician": {"charisma": 3, "intelligence": 2},
    "Mayor": {"charisma": 3, "intelligence": 2},
    "Bank Manager": {"intelligence": 3, "charisma": 2},
    "Business Owner": {"charisma": 2, "intelligence": 2},

    # -------------------------
    # HIGH-LEVEL CAREERS
    # -------------------------
    "CEO": {"charisma": 3, "intelligence": 3},
    "Investor": {"intelligence": 3},
    "Scientist": {"intelligence": 3},
    "Professor": {"intelligence": 3, "empathy": 1},
    "Researcher": {"intelligence": 3},
    "Pilot": {"intelligence": 2, "fitness": 2},
    "Air Traffic Controller": {"intelligence": 3},
    "Detective": {"intelligence": 2, "charisma": 1},
    "Psychologist": {"empathy": 3, "intelligence": 2},
    "Economist": {"intelligence": 3},

    # -------------------------
    # DEFAULT / EDGE CASES
    # -------------------------
    "Unemployed": {},
    "Criminal": {"aggression": 2},
    "Thief": {"aggression": 2, "fitness": 1},
    "Hacker": {"intelligence": 3},
    "Smuggler": {"fitness": 2, "aggression": 1},
    "Informant": {"charisma": 2},
    "Gang Member": {"aggression": 2, "fitness": 2},
}

def create_random_npcs(count=200):
    for _ in range(count):
        Npc.objects.create()
        
        
def process_death():
    return Npc.objects.filter(
        is_alive=True,
        health_level__lte=0
    ).update(
        is_alive=False,
        died_at=timezone.now()
    )

def apply_npc_state_effects(npc):
    """
    Applies passive consequences based on current stats.
    Runs after any system tick.
    """

    # ENERGY EFFECTS
    if npc.energy_level < 20:
        npc.stress_level += 3
        npc.introversion_level += 2
        npc.morality_level -= 2

    elif npc.energy_level < 40:
        npc.stress_level += 1

    # HIGH ENERGY BONUS
    if npc.energy_level > 80:
        npc.happiness_level += 1

    # STRESS EFFECTS
    if npc.stress_level > 70:
        npc.introversion_level += 2
        npc.aggression_level += 1

    # HEALTH EFFECTS
    if npc.health_level < 30:
        npc.energy_level -= 2
        npc.happiness_level -= 1
        npc.morality_level += 2
       
# Related to jobs
def clamp(npc):
    npc.fitness_level = max(0, npc.fitness_level)
    npc.intelligence_level = max(0, npc.intelligence_level)
    npc.charisma_level = max(0, npc.charisma_level)
    npc.creativity_level = max(0, npc.creativity_level)
    npc.empathy_level = max(0, npc.empathy_level)
    npc.morality_level = max(0, npc.morality_level)

    npc.aggression_level = max(0, npc.aggression_level)
    npc.stress_level = max(0, npc.stress_level)
    npc.happiness_level = max(0, npc.happiness_level)

    npc.energy_level = max(0, min(100, npc.energy_level))


def score_job(npc, requirements):
    score = 0

    for stat, weight in requirements.items():
        value = getattr(npc, f"{stat}_level", 0)
        score += value * weight

    return score
       
        
def apply_condition_modifier(npc, job, score):
    condition = npc.degenerative_condition

    if condition == "narcissist" and job in ["CEO", "Politician", "Manager"]:
        score *= 1.3

    if condition == "sociopath" and job in ["Soldier", "Police Officer", "Gang Member"]:
        score *= 1.4

    if condition == "psychopath":
        score *= 1.2  

    if condition == "paranoid":
        score *= 0.9

    if condition == "pedophile":
        score *= 0.5
    
    return score
       
        
def assign_job(npc, JOBS):
    best_job = None
    best_score = -1

    for job, reqs in JOBS.items():
        # 1. base score first
        score = score_job(npc, reqs)

        # 2. apply condition modifier
        score = apply_condition_modifier(npc, job, score)

        # 3. pick best job
        if score > best_score:
            best_score = score
            best_job = job
    if best_job is None:
        best_job = "Unemployed"
    npc.occupation = best_job
    npc.job_level = 1
    npc.salary = random.randint(50, 200) + int(best_score * 10)

    return npc