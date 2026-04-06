
from django.core.management.base import BaseCommand
from django.utils import timezone
from civilAI.npc.models import Npc


class Command(BaseCommand):
    help = 'Update NPC ages'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        for npc in Npc.objects.all():
            delta = now - npc.created_at
            npc.age = npc.initial_age + int(delta.total_seconds() // 6)
            npc.save(update_fields=['age'])

        self.stdout.write("NPC ages updated")
        

