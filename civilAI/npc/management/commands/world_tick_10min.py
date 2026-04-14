from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from civilAI.npc.utils import process_death, clamp
from civilAI.npc.models import Npc


class Command(BaseCommand):
    help = "WORLD TICK - run in every 10 minutes - 2.5 days in simulation"

    def handle(self, *args, **kwargs):
        """
        # 1. DEGENERATIVE BEHAVIOR
        self.stdout.write("→ Running degenerative systems...")
        call_command("degenerative_npc")
        process_death()
        npcs = list(Npc.objects.filter(is_alive=True))
        for npc in npcs:
            clamp(npc)

        Npc.objects.bulk_update(
            npcs,
            [
                "fitness_level", "intelligence_level", "aggression_level",
                "happiness_level", "stress_level", "charisma_level",
                "empathy_level", "morality_level", "health_level",
                "energy_level", "introversion_level", "creativity_level",
            ]
        )
        """