from django.core.management.base import BaseCommand
from civilAI.npc.models import Npc
from django.db.models import F


class Command(BaseCommand):
    help = 'Update NPC ages'

    def handle(self, *args, **kwargs):
        updated = Npc.objects.filter(is_alive=True).update(
            age=F("age") + 1,
            health_level=F("health_level") - 1,
        )

        self.stdout.write(f"{updated} NPC ages updated")