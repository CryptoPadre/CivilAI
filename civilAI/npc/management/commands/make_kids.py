from django.core.management.base import BaseCommand
from django.utils import timezone
from civilAI.npc.models import Npc
import random
from math import radians, cos, sin, sqrt, atan2


class Command(BaseCommand):
    help = "Generate new NPCs as children of adults safely"

    # Haversine distance helper
    def distance_km(self, lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1_rad, lon1_rad = radians(lat1), radians(lon1)
        lat2_rad, lon2_rad = radians(lat2), radians(lon2)
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def handle(self, *args, **kwargs):
        MAX_DISTANCE_KM = 2

        # Fertility → probability
        FERTILITY_CHANCE = {
            'H': 0.6,
            'N': 0.3,
            'L': 0.1
        }

        def is_related(npc1, npc2):
            return (
                npc1.id == npc2.mother_id or
                npc1.id == npc2.father_id or
                npc2.id == npc1.mother_id or
                npc2.id == npc1.father_id
            )

        adults = Npc.objects.filter(
            age__gte=15,
            is_alive=True,
            sexual_orientation__in=['hetero', 'bi']
        )

        for npc in adults:
            # Filter eligible partners
            potential_partners = Npc.objects.filter(
                sex='F' if npc.sex == 'M' else 'M',
                age__gte=15,
                is_alive=True
            ).exclude(id=npc.id)

            potential_partners = [
                p for p in potential_partners
                if not is_related(npc, p) and
                self.distance_km(npc.latitude, npc.longitude, p.latitude, p.longitude) <= MAX_DISTANCE_KM
            ]

            if not potential_partners:
                continue

            # Prefer previous partners (~70%) if available
            prev_partners = [p for p in potential_partners if p in npc.previous_partners.all()]
            if prev_partners and random.random() < 0.7:
                partner = random.choice(prev_partners)
            else:
                partner = random.choice(potential_partners)

            # Fertility chance
            npc_chance = FERTILITY_CHANCE.get(npc.fertility, 0.3)
            partner_chance = FERTILITY_CHANCE.get(partner.fertility, 0.3)
            combined_chance = (npc_chance + partner_chance) / 2
            if random.random() > combined_chance:
                continue

            # Determine mother/father
            mother = npc if npc.sex == 'F' else partner
            father = npc if npc.sex == 'M' else partner

            # Create child
            child_sex = random.choice(['M', 'F'])
            child = Npc.objects.create(
                sex=child_sex,
                first_name=random.choice(
                    Npc.MALE_FIRST_NAMES if child_sex == 'M' else Npc.FEMALE_FIRST_NAMES
                ),
                last_name=father.last_name,
                age=0,
                initial_age=0,
                fertility=random.choices(
                    population=['H','N','L'],
                    weights=[0.5,0.35,0.15],
                    k=1
                )[0],
                sexual_orientation=random.choice([o[0] for o in Npc.ORIENTATION_CHOICES]),
                mother=mother,
                father=father,
                latitude=(mother.latitude + father.latitude)/2,
                longitude=(mother.longitude + father.longitude)/2
            )

            # Save partner relationship for future bonding
                
            npc.previous_partners.add(partner)
            partner.previous_partners.add(npc)

            self.stdout.write(
                f"New NPC {child.first_name} born from {mother.first_name} and {father.first_name} "
                f"(fertility {npc.fertility}/{partner.fertility})"
            )