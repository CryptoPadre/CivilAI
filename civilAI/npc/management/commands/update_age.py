from django.core.management.base import BaseCommand
from django.utils import timezone
from civilAI.npc.models import Npc


class Command(BaseCommand):
    help = 'Update NPC ages'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        for npc in Npc.objects.filter(is_alive=True):
            npc.age = npc.initial_age + (now - npc.born_at).days
            npc.health_level -= 1

            npc.save(update_fields=['age', 'health_level'])

        self.stdout.write("NPC ages updated")