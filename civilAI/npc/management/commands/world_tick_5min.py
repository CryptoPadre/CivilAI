from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from civilAI.npc.utils import process_death

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