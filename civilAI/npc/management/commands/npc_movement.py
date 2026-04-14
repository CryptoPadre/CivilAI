from django.core.management.base import BaseCommand
from civilAI.npc.models import Npc
from civilAI.npc.utils import apply_npc_state_effects
import random


class Command(BaseCommand):
    help = "Move NPCs around the map"

    def handle(self, *args, **kwargs):

        npcs = list(
            Npc.objects.filter(is_alive=True, age__gte=15)
            .select_related("mother", "father")
            .prefetch_related("children_from_mother", "children_from_father", "previous_partners")
        )

        moved_ids = set()
        updated_npcs = []

        for npc in npcs:

            if npc.id in moved_ids:
                continue

            # build family in memory (no DB hits now)
            family = set([npc])

            if npc.mother:
                family.add(npc.mother)
            if npc.father:
                family.add(npc.father)

            family.update(npc.children_from_mother.all())
            family.update(npc.children_from_father.all())
            family.update(npc.previous_partners.all())

            family = [f for f in family if f.is_alive]

            strongest = max(family, key=lambda x: x.fitness_level)
            step = 0.2 if strongest.fitness_level > 7 and strongest.health_level > 60 else 0.1

            move_chance = 1.0 if npc.energy_level >= 50 else npc.energy_level / 50

            if random.random() < move_chance:
                delta_lat = random.uniform(-step, step)
                delta_lon = random.uniform(-step, step)

                for member in family:
                    if member.id in moved_ids:
                        continue

                    member.latitude += delta_lat
                    member.longitude += delta_lon
                    member.energy_level -= 5 if step > 0.1 else 10

                    # apply_npc_state_effects(member)

                    moved_ids.add(member.id)
                    updated_npcs.append(member)

            else:
                for member in family:
                    if member.id in moved_ids:
                        continue

                    member.energy_level += 20
                    # apply_npc_state_effects(member)

                    moved_ids.add(member.id)
                    updated_npcs.append(member)

        # single DB write
        Npc.objects.bulk_update(
            updated_npcs,
            [
                "latitude", "longitude", "energy_level",
                "fitness_level", "intelligence_level", "aggression_level",
                "happiness_level", "stress_level", "charisma_level",
                "empathy_level", "morality_level", "health_level",
                "energy_level", "introversion_level", "creativity_level",
            ]
        )

        self.stdout.write(f"Moved {len(updated_npcs)} NPCs")