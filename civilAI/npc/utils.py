from civilAI.npc.models import Npc
from django.utils import timezone

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
        
    if npc.energy_level > 100:
        npc.energy_level = 100
    if npc.energy_level < 0:
        npc.energy_level = 0
    if npc.introversion_level > 100:
        npc.introversion_level = 100
    if npc.introversion_level < 0:
        npc.introversion_level = 0