from django.core.management.base import BaseCommand
from civilAI.npc.models import Npc
from civilAI.npc.utils import apply_npc_state_effects
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
        base_mother_death_chance = 0.001  # 0.1% base risk
        COMPLICATIONS_CHANCE = 0.01
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
            age__lte=55,
            is_alive=True,
            sexual_orientation__in=['hetero', 'bi']
        )

        for npc in adults:
            # Filter eligible partners
            potential_partners = Npc.objects.filter(
                sex='F' if npc.sex == 'M' else 'M',
                age__gte=15,
                age__lte=55,
                is_alive=True 
            ).exclude(id=npc.id)

            potential_partners = [
                p for p in potential_partners
                if (not is_related(npc, p) or npc.degenerative_condition == "pedophile") and
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
                longitude=(mother.longitude + father.longitude)/2,
                personality_traits=inherited_traits
                
            )
            mother.has_kids = True
            father.has_kids = True
            mother.energy_level -= 30
            father.energy_level -= 10
            mother.happiness_level += 40
            father.happiness_level += 30
            apply_npc_state_effects(mother)
            apply_npc_state_effects(father)
            # ----------------------------
            # COMPLICATION SYSTEM
            # ----------------------------
            if random.random() < COMPLICATIONS_CHANCE:

                # AGE-based risk factor
                age = mother.age

                if age < 20:
                    age_factor = 1.2
                elif age <= 34:
                    age_factor = 1.0
                elif age <= 39:
                    age_factor = 2.0
                else:
                    age_factor = 4.0

                mother_death_chance = base_mother_death_chance * age_factor

                # Mother death
                if random.random() < mother_death_chance:
                    mother.health_level -= 100  # triggers process_death from npc.utils later

                # Baby survival system (only if mother is at risk)
                baby_survival_chance = 0.8

                if age >= 35:
                    baby_survival_chance -= 0.2
                if age >= 40:
                    baby_survival_chance -= 0.3

                if random.random() > baby_survival_chance:
                    child.health_level = 0  # baby dies (will be processed later)
            mother.save(update_fields=["has_kids"])
            father.save(update_fields=["has_kids"])
            parent_traits = []

            if mother.personality_traits:
                parent_traits += mother.personality_traits

            if father.personality_traits:
                parent_traits += father.personality_traits

            inherited_traits = []

            for trait in parent_traits:
                if random.random() < 0.7:  # strong early inheritance
                    inherited_traits.append(trait)

            # Limit + uniqueness
            inherited_traits = list(set(inherited_traits))[:3]
            child.personality_traits = inherited_traits
            # Save partner relationship for future bonding
                
            npc.previous_partners.add(partner)
            partner.previous_partners.add(npc)

            self.stdout.write(
                f"New NPC {child.first_name} born from {mother.first_name} and {father.first_name} "
                f"(fertility {npc.fertility}/{partner.fertility})"
            )