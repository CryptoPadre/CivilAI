import random
from django.core.management.base import BaseCommand
from global_land_mask import globe

from civilAI.npc.models import Npc


class Command(BaseCommand):
    help = "Move NPCs around the map without allowing movement onto water"

    MAX_MOVE_ATTEMPTS = 20

    def is_land(self, lat, lon):
        """
        Returns True if the position is on land.
        Prevents NPCs from moving into oceans/seas.
        """
        if lat is None or lon is None:
            return False

        if lat < -90 or lat > 90:
            return False

        if lon < -180 or lon > 180:
            return False

        return globe.is_land(lat, lon)

    def get_valid_position(self, old_lat, old_lon, delta_lat, delta_lon, move_multiplier):
        """
        Try several random movements until a land position is found.
        If none is valid, NPC stays in the old position.
        """
        for _ in range(self.MAX_MOVE_ATTEMPTS):
            new_lat = old_lat + (delta_lat * move_multiplier)
            new_lon = old_lon + (delta_lon * move_multiplier)

            if self.is_land(new_lat, new_lon):
                return new_lat, new_lon

            delta_lat = random.uniform(-abs(delta_lat), abs(delta_lat))
            delta_lon = random.uniform(-abs(delta_lon), abs(delta_lon))

        return old_lat, old_lon

    def handle(self, *args, **kwargs):
        npcs = list(
            Npc.objects.filter(is_alive=True, age__gte=0)
            .select_related("mother", "father")
            .prefetch_related(
                "children_from_mother",
                "children_from_father",
                "previous_partners",
            )
        )

        moved_ids = set()
        updated_npcs = []

        for npc in npcs:
            if npc.id in moved_ids:
                continue

            family = {npc}

            if npc.mother:
                family.add(npc.mother)

            if npc.father:
                family.add(npc.father)

            family.update(npc.children_from_mother.all())
            family.update(npc.children_from_father.all())
            family.update(npc.previous_partners.all())

            family = [member for member in family if member.is_alive]

            if not family:
                continue

            strongest = max(family, key=lambda x: x.fitness_level)

            step = 0.01 if strongest.fitness_level > 7 and strongest.health_level > 60 else 0.005

            move_chance = 1.0 if npc.energy_level >= 50 else npc.energy_level / 50

            if random.random() < move_chance:
                delta_lat = random.uniform(-step, step)
                delta_lon = random.uniform(-step, step)

                for member in family:
                    if member.id in moved_ids:
                        continue

                    if member.latitude is None or member.longitude is None:
                        moved_ids.add(member.id)
                        continue

                    if member.age <= 5:
                        parent = member.mother or member.father

                        if (
                            parent
                            and parent in family
                            and parent.latitude is not None
                            and parent.longitude is not None
                        ):
                            new_lat, new_lon = self.get_valid_position(
                                parent.latitude,
                                parent.longitude,
                                random.uniform(-0.00005, 0.00005),
                                random.uniform(-0.00005, 0.00005),
                                1,
                            )
                        else:
                            new_lat, new_lon = self.get_valid_position(
                                member.latitude,
                                member.longitude,
                                delta_lat,
                                delta_lon,
                                0.1,
                            )

                    elif member.age <= 12:
                        new_lat, new_lon = self.get_valid_position(
                            member.latitude,
                            member.longitude,
                            delta_lat,
                            delta_lon,
                            0.3,
                        )

                    elif member.age <= 17:
                        new_lat, new_lon = self.get_valid_position(
                            member.latitude,
                            member.longitude,
                            delta_lat,
                            delta_lon,
                            0.6,
                        )

                    else:
                        new_lat, new_lon = self.get_valid_position(
                            member.latitude,
                            member.longitude,
                            delta_lat,
                            delta_lon,
                            1,
                        )

                    member.latitude = new_lat
                    member.longitude = new_lon
                    member.energy_level = max(0, member.energy_level - 5)

                    moved_ids.add(member.id)
                    updated_npcs.append(member)

            else:
                for member in family:
                    if member.id in moved_ids:
                        continue

                    member.energy_level = min(100, member.energy_level + 10)

                    moved_ids.add(member.id)
                    updated_npcs.append(member)

        if updated_npcs:
            Npc.objects.bulk_update(
                updated_npcs,
                [
                    "latitude",
                    "longitude",
                    "energy_level",
                ],
            )

        self.stdout.write(
            self.style.SUCCESS(f"Updated {len(updated_npcs)} NPCs")
        )