from civilAI.npc.models import Npc
from django.utils import timezone

def create_random_npcs(count=150000):
    created = 0

    for i in range(1, count + 1):
        Npc.objects.create()
        created += 1

        if i % 1000 == 0:
            print(f"{created} NPCs created so far...")

    print(f"Finished. Total NPCs created: {created}")
        
        
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
    npc.introversion_level = max(0, min(100, npc.introversion_level))
    npc.aggression_level = max(0, min(100, npc.aggression_level))
    npc.stress_level = max(0, min(100, npc.stress_level))
    npc.happiness_level = max(0, min(100, npc.happiness_level))
    npc.energy_level = max(0, min(100, npc.energy_level))
    npc.job_level = max(1, min(10, npc.job_level))
