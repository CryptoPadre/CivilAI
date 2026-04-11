from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from civilAI.npc.utils import process_death, clamp
from civilAI.npc.models import Npc

class Command(BaseCommand):
    help = "WORLD TICK - run in every 96h - 4 years in simulation"

    def handle(self, *args, **kwargs):
        # 6. GLOBAL EVENTS (world state changes)
        self.stdout.write("→ Running global events...")
        call_command("global_events")
        process_death()
        for npc in Npc.objects.filter(is_alive=True):
            clamp(npc)
            npc.save()