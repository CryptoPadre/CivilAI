
from django.core.management.base import BaseCommand
from django.utils import timezone
from civilAI.npc.models import Npc


class Command(BaseCommand):
    help = 'Update NPC ages'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        for npc in Npc.objects.all():
            if npc.is_alive:
                delta = now - npc.born_at
                npc.age = npc.initial_age + int(delta.total_seconds() // 6)
                npc.health_level -= 1
                if npc.is_alive and npc.health_level <= 0:
                    npc.is_alive = False
                    npc.died_at = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                npc.save(update_fields=['age', 'health_level', 'is_alive', 'died_at'])

        self.stdout.write("NPC ages updated")
        

