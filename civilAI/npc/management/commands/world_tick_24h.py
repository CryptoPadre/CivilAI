from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from civilAI.npc.utils import process_death, clamp
from civilAI.npc.models import Npc


class Command(BaseCommand):
    help = "WORLD TICK - run in every 24h - 1 year in simulation"

    def handle(self, *args, **kwargs):
        start_time = timezone.now()

        self.stdout.write("\n===== WORLD TICK START =====\n")

        try:
            # 1. AGE + DEATH (must ALWAYS be first)
            self.stdout.write("→ Running age & death system...")
            call_command("update_age")
            process_death()

            # 2. REPRODUCTION SYSTEM
            self.stdout.write("→ Running reproduction system...")
            call_command("make_kids")
            process_death()

            self.stdout.write("\n===== WORLD TICK END =====\n")

            for npc in Npc.objects.filter(is_alive=True):
                clamp(npc)
                npc.save()
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"World tick failed: {e}"))

        end_time = timezone.now()
        duration = (end_time - start_time).total_seconds()

        self.stdout.write(
            self.style.SUCCESS(
                f"World tick completed in {duration:.2f} seconds"
            )
        )