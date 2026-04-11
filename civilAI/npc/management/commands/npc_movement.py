from django.core.management.base import BaseCommand
from civilAI.npc.models import Npc
from civilAI.npc.utils import apply_npc_state_effects
import random

class Command(BaseCommand):
    help = "Move NPCs around the map"

    def handle(self, *args, **kwargs):
        for npc in Npc.objects.filter(is_alive=True, age__gte=15):
            # Only move if not already moved in this cycle
            if getattr(npc, "_moved", False):
                continue

            # Build family group
            family = set()
            family.add(npc)
            if npc.mother:
                family.add(npc.mother)
            if npc.father:
                family.add(npc.father)
            family.update(npc.children_from_mother.all())
            family.update(npc.children_from_father.all())
            
            # Include partner if you want them sticking together
            family.update(npc.previous_partners.all())

            # Filter alive members
            family = [f for f in family if f.is_alive]

            # Determine group step based on strongest NPC
            strongest = max(family, key=lambda x: x.fitness_level)
            step = 0.01 if strongest.fitness_level > 7 and strongest.health_level > 60 else 0.005

            # Check move chance for the main NPC
            move_chance = 1.0 if npc.energy_level >= 50 else npc.energy_level / 50
            if random.random() < move_chance:
                delta_lat = random.uniform(-step, step)
                delta_lon = random.uniform(-step, step)
                
                # Move all family members together
                for member in family:
                    member.latitude += delta_lat
                    member.longitude += delta_lon
                    # Reduce energy individually
                    member.energy_level -= 5 if step > 0.005 else 10
                    member._moved = True  # mark as moved
                    apply_npc_state_effects(member)
                    member.save()
                
                print(f"{npc.first_name} moved with family ({len(family)} members)")
            else:
                # Restore some energy if no movement
                for member in family:
                    member.energy_level += 1
                    apply_npc_state_effects(member)
                    member.save()
                print(f"{npc.first_name} and family stayed in place")