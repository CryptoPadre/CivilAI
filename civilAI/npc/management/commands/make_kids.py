from django.core.management.base import BaseCommand
from django.utils import timezone
from civilAI.npc.models import Npc
import random

class Command(BaseCommand):
    help = "Generate new NPCs as children of adults safely"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Helper to check family relationships
        def is_related(npc1, npc2):
            # Same parents (siblings)
            if npc1.mother and npc1.mother == npc2.mother:
                return True
            if npc1.father and npc1.father == npc2.father:
                return True
            # Parent-child
            if npc1 == npc2.mother or npc1 == npc2.father:
                return True
            if npc2 == npc1.mother or npc2 == npc1.father:
                return True
            return False

        adults = Npc.objects.filter(age__gte=15, is_alive=True)

        for npc in adults:
            # Chance to have a child
            if random.random() < 0.7:
                # Eligible partners
                potential_partners = Npc.objects.filter(
                    sex='F' if npc.sex == 'M' else 'M',
                    age__gte=15,
                    is_alive=True
                ).exclude(id=npc.id)

                # Filter out family
                potential_partners = [p for p in potential_partners if not is_related(npc, p)]

                if potential_partners:
                    partner = random.choice(potential_partners)

                    # Determine mother and father
                    mother = npc if npc.sex == 'F' else partner
                    father = npc if npc.sex == 'M' else partner

                    # Create child
                    child_sex = random.choice(['M', 'F'])
                    child = Npc.objects.create(
                        sex=child_sex,
                        first_name=random.choice(
                            Npc.MALE_FIRST_NAMES if child_sex == 'M' else Npc.FEMALE_FIRST_NAMES
                        ),
                        last_name=father.last_name,  # inherit father's last name
                        age=0,
                        initial_age=0,
                        fertility=random.choice([f[0] for f in Npc.FERTILITY_RATE]),
                        sexual_orientation=random.choice([o[0] for o in Npc.ORIENTATION_CHOICES]),
                        mother=mother,
                        father=father
                    )

                    self.stdout.write(
                        f"New NPC {child.first_name} born from {mother.first_name} and {father.first_name}"
                    )