from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from npc.utils import process_death


class Command(BaseCommand):
    help = "WORLD TICK - run in every 10 minutes - 2.5 days in simulation"

    def handle(self, *args, **kwargs):
        
        # 1. DEGENERATIVE BEHAVIOR
        self.stdout.write("→ Running degenerative systems...")
        call_command("degenerative_npc")
        process_death()