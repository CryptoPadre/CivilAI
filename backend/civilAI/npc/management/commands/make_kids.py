from django.core.management.base import BaseCommand
from django.utils import timezone
from civilAI.npc.models import Npc
import random

class Command(BaseCommand):
    help = "Generate new NPCs as children of adults"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        for npc in Npc.objects.all():
            if npc.age >= 15 and npc.fertility == "H":
                # Example: 10% chance to have a child each run
                if random.random() < 0.7:
                    # Pick a partner randomly from eligible NPCs
                    potential_partners = Npc.objects.filter(
                        sex='F' if npc.sex == 'M' else 'M',
                        age__gte=15,
                    ).exclude(id=npc.id)

                    if potential_partners.exists():
                        partner = random.choice(list(potential_partners))
                        # Generate new NPC
                        child_sex = random.choice(['M', 'F'])
                        child = Npc.objects.create(
                            sex=child_sex,
                            first_name=random.choice(
                                Npc.MALE_FIRST_NAMES if child_sex == 'M' else Npc.FEMALE_FIRST_NAMES
                            ),
                            last_name=partner.last_name,  # inherit last name
                            age=0,
                            initial_age=0,
                            fertility=random.choice([f[0] for f in Npc.FERTILITY_RATE]),
                            sexual_orientation=random.choice([o[0] for o in Npc.ORIENTATION_CHOICES])
                        )
                        self.stdout.write(f"New NPC {child.first_name} born from {npc.first_name} and {partner.first_name}")