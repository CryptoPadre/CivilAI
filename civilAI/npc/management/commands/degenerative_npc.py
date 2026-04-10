from django.core.management.base import BaseCommand
from civilAI.npc.models import Npc
from npc.utils import apply_npc_state_effects

class Command(BaseCommand):
    help = "Apply degenerative NPC behavior effects"

    TOLERANCE = 0.0001
    
    def same_location(self, a, b):
         return (
            abs(a.latitude - b.latitude) < self.TOLERANCE and
            abs(a.longitude - b.longitude) < self.TOLERANCE
        )
    
    def handle(self, *args, **kwargs):
        npcs = Npc.objects.filter(is_alive=True, age__gte=12)
        print("\n=== DEGENERATIVE CYCLE START ===\n")

        for npc in npcs:
            if npc.degenerative_condition == 'none':
                continue

            print(f"🧠 {npc.first_name} has {npc.degenerative_condition}")

            # 1. NPC ALWAYS changes (independent of location)
            if npc.degenerative_condition == 'psychopath':
                npc.aggression_level += 2
                npc.empathy_level -= 2
                npc.intelligence_level += 1
                npc.charisma_level += 2

            elif npc.degenerative_condition == 'sociopath':
                npc.morality_level -= 2
                npc.stress_level += 1
                npc.intelligence_level += 1
                npc.charisma_level += 2

            elif npc.degenerative_condition == 'narcissist':
                npc.charisma_level += 1
                npc.empathy_level -= 1
                npc.charisma_level += 1

            elif npc.degenerative_condition == 'paranoid':
                npc.stress_level += 2
                npc.introversion_level += 2
                npc.health_level -= 2

            elif npc.degenerative_condition == 'pedophile':
                npc.charisma_level += 2
                npc.aggression_level += 1

            # save NPC changes first (or at end, either is fine)
            npc.save()

            # 2. TARGET EFFECTS ONLY IF SAME LOCATION
            if npc.degenerative_condition in [c[0] for c in npc.DEGENERATIVE_CHOICES]:

                potential_targets = Npc.objects.filter(is_alive=True).exclude(id=npc.id)

                for target in potential_targets:
                    if not self.same_location(npc, target):
                        continue

                    if npc.degenerative_condition == 'psychopath':
                        target.is_alive = False

                    elif npc.degenerative_condition == 'sociopath':
                        target.stress_level += 3
                        target.introversion_level += 5

                    elif npc.degenerative_condition == 'narcissist':
                        target.happiness_level -= 3
                        target.introversion_level += 10

                    elif npc.degenerative_condition == 'paranoid':
                        target.stress_level -= 2
                        target.morality_level -= 2
                        target.introversion_level +=5

                    elif npc.degenerative_condition == 'pedophile':
                        target.empathy_level -= 4
                        target.introversion_level += 15

                    target.save()

        print("\n=== DEGENERATIVE CYCLE END ===\n")