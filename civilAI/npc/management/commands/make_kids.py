from django.core.management.base import BaseCommand
from civilAI.npc.models import Npc
from civilAI.npc.utils import apply_npc_state_effects
import random
from math import radians, cos, sin, sqrt, atan2


class Command(BaseCommand):
    help = "Generate new NPCs as children of adults safely"

    def distance_km(self, lat1, lon1, lat2, lon2):
        R = 6371.0
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)

        a = (
            sin(dlat / 2) ** 2
            + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        )
        return 2 * R * atan2(sqrt(a), sqrt(1 - a))

    def handle(self, *args, **kwargs):

        MAX_DISTANCE_KM = 2

        FERTILITY_CHANCE = {"H": 0.6, "N": 0.3, "L": 0.1}

        adults = list(
            Npc.objects.filter(
                age__gte=15,
                age__lte=55,
                is_alive=True,
                sexual_orientation__in=["hetero", "bi"],
            ).only(
                "id", "sex", "age", "latitude", "longitude",
                "fertility", "last_name",
                "health_level", "energy_level", "happiness_level",
                "personality_traits",
            )
        )

        # preload relations (IMPORTANT)
        relations_map = {
            n.id: set(n.previous_partners.values_list("id", flat=True))
            for n in adults
        }

        new_children = []
        updated_parents = []
        relation_pairs = []

        for npc in adults:

            candidates = [
                p for p in adults
                if p.id != npc.id
                and p.sex != npc.sex
                and abs(p.age - npc.age) <= 20
                and self.distance_km(
                    npc.latitude, npc.longitude,
                    p.latitude, p.longitude
                ) <= MAX_DISTANCE_KM
            ]

            if not candidates:
                continue

            # avoid relatives
            candidates = [
                p for p in candidates
                if p.id not in relations_map[npc.id]
            ]

            if not candidates:
                continue

            partner = random.choice(candidates)

            npc_chance = FERTILITY_CHANCE.get(npc.fertility, 0.3)
            partner_chance = FERTILITY_CHANCE.get(partner.fertility, 0.3)

            if random.random() > (npc_chance + partner_chance) / 2:
                continue

            mother = npc if npc.sex == "F" else partner
            father = npc if npc.sex == "M" else partner

            child = Npc(
                sex=random.choice(["M", "F"]),
                first_name=random.choice(
                    Npc.MALE_FIRST_NAMES if random.random() < 0.5 else Npc.FEMALE_FIRST_NAMES
                ),
                last_name=father.last_name,
                age=0,
                fertility=random.choice(["H", "N", "L"]),
                sexual_orientation=random.choice([o[0] for o in Npc.ORIENTATION_CHOICES]),
                mother=mother,
                father=father,
                latitude=(mother.latitude + father.latitude) / 2,
                longitude=(mother.longitude + father.longitude) / 2,
                personality_traits=list(set(
                    (mother.personality_traits or []) + (father.personality_traits or [])
                ))[:3],
            )

            new_children.append(child)

            # side effects in memory only
            mother.energy_level -= 30
            father.energy_level -= 10
            mother.happiness_level += 40
            father.happiness_level += 30

            mother.has_kids = True
            father.has_kids = True

            updated_parents.extend([mother, father])

            relation_pairs.append((mother, father))

        # bulk operations
        Npc.objects.bulk_create(new_children)

        Npc.objects.bulk_update(
            updated_parents,
            ["energy_level", "happiness_level", "has_kids"]
        )
        
        # collect affected NPCs only
        affected_npcs = set(updated_parents)

        # include children (after bulk_create they now exist in DB)
        affected_npcs.update(new_children)

        # apply effects
        for npc in affected_npcs:
            apply_npc_state_effects(npc)

        Npc.objects.bulk_update(
            affected_npcs,
            [
                "fitness_level", "intelligence_level", "aggression_level",
                "happiness_level", "stress_level", "charisma_level",
                "empathy_level", "morality_level", "health_level",
                "energy_level", "introversion_level", "creativity_level",
            ]
)

        # relations (still unavoidable but minimized)
        for a, b in relation_pairs:
            a.previous_partners.add(b)

        self.stdout.write(f"Created {len(new_children)} children")