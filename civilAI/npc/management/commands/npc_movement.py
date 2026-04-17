import random
from django.core.management.base import BaseCommand
from civilAI.npc.models import Npc


class Command(BaseCommand):
    help = "Move NPCs around the map"

    def handle(self, *args, **kwargs):
        npcs = list(
            Npc.objects.filter(is_alive=True, age__gte=0)
            .select_related("mother", "father")
            .prefetch_related(
                "children_from_mother",
                "children_from_father",
                "previous_partners"
            )
        )

        moved_ids = set()
        updated_npcs = []

        for npc in npcs:
            if npc.id in moved_ids:
                continue

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
            step = 0.001 if strongest.fitness_level > 7 and strongest.health_level > 60 else 0.0005

            move_chance = 1.0 if npc.energy_level >= 50 else npc.energy_level / 50

            if random.random() < move_chance:
                delta_lat = random.uniform(-step, step)
                delta_lon = random.uniform(-step, step)

                for member in family:
                    if member.id in moved_ids:
                        continue

                    # very small children stay very close to parent
                    if member.age <= 5:
                        parent = member.mother or member.father
                        if parent and parent in family:
                            member.latitude = parent.latitude + random.uniform(-0.00005, 0.00005)
                            member.longitude = parent.longitude + random.uniform(-0.00005, 0.00005)
                        else:
                            member.latitude += delta_lat * 0.1
                            member.longitude += delta_lon * 0.1

                    # older children move a little, but less than adults
                    elif member.age <= 12:
                        member.latitude += delta_lat * 0.3
                        member.longitude += delta_lon * 0.3

                    # teens move more freely
                    elif member.age <= 17:
                        member.latitude += delta_lat * 0.6
                        member.longitude += delta_lon * 0.6

                    # adults use full family move
                    else:
                        member.latitude += delta_lat
                        member.longitude += delta_lon

                    member.energy_level -= 5 if step > 0.0005 else 2
                    moved_ids.add(member.id)
                    updated_npcs.append(member)

            else:
                for member in family:
                    if member.id in moved_ids:
                        continue

                    member.energy_level += 10
                    moved_ids.add(member.id)
                    updated_npcs.append(member)

        Npc.objects.bulk_update(
            updated_npcs,
            [
                "latitude",
                "longitude",
                "energy_level",
            ]
        )

        self.stdout.write(f"Moved {len(updated_npcs)} NPCs")