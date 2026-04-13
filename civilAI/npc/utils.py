from civilAI.npc.models import Npc
from django.utils import timezone
import random

def create_random_npcs(count=50):
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
       

def clamp(npc):
    npc.fitness_level = max(0, min(100, npc.fitness_level))
    npc.intelligence_level = max(0, min(100, npc.intelligence_level))
    npc.charisma_level = max(0, min(100, npc.charisma_level))
    npc.creativity_level = max(0, min(100, npc.creativity_level))
    npc.empathy_level = max(0, min(100, npc.empathy_level))
    npc.morality_level = max(0, min(100, npc.morality_level))

    npc.aggression_level = max(0, min(100, npc.aggression_level))
    npc.stress_level = max(0, min(100, npc.stress_level))
    npc.happiness_level = max(0, min(100, npc.happiness_level))
    npc.energy_level = max(0, min(100, npc.energy_level))


def score_job(npc, requirements):
    score = 0

    # base stats vs job requirements
    for stat, weight in requirements.items():
        value = getattr(npc, f"{stat}_level", 0)
        score += value * weight

    # personality effects
    for trait in npc.personality_traits:
        effects = PERSONALITY_EFFECTS.get(trait, {})
        for stat, bonus in effects.items():
            score += bonus

    # degenerative condition effects (NEW)
    effects = DEGENERATIVE_EFFECTS.get(npc.degenerative_condition, {})
    for stat, bonus in effects.items():
        score += bonus

    # randomness (keeps diversity)
    score += random.uniform(0, 5)

    return score
       
        
def assign_job(npc, JOBS):

    if npc.age <= 18:
        npc.occupation = "Unemployed"
        npc.job_level = 1
        npc.salary = 0
        return npc

    best_job = None
    best_score = -1

    for job, reqs in JOBS.items():
        score = score_job(npc, reqs)
        score += random.uniform(0, 0.5)

        if score > best_score:
            best_score = score
            best_job = job

    npc.occupation = best_job
    npc.job_level = 1
    npc.salary = int(100 + best_score * 3 + random.randint(0, 50))

    return npc