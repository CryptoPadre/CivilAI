from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from civilAI.npc.utils import process_death, clamp, assign_job, JOBS
from civilAI.npc.models import Npc

class Command(BaseCommand):
    help = "WORLD TICK - run in every 5min - 1.25 day in simulation"

    def handle(self, *args, **kwargs):
        
        
        # 1. NPC MOVEMENT
        self.stdout.write("→ Running movement system...")
        call_command("npc_movement")
        # 2. DAILY INTERACTIONS (attack / help / social / work)
        self.stdout.write("→ Running daily behavior...")
        call_command("daily_task")
        process_death()
        npcs = list(Npc.objects.filter(is_alive=True))

        for npc in npcs:
            clamp(npc)

            if npc.occupation == "Unemployed":
                assign_job(npc, JOBS)

        Npc.objects.bulk_update(
            npcs,
            [
                "fitness_level", "intelligence_level", "aggression_level",
                "happiness_level", "stress_level", "charisma_level",
                "empathy_level", "morality_level", "health_level",
                "energy_level", "introversion_level", "creativity_level",
                "occupation", "job_level", "salary",
            ]
        )
        