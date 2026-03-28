from .models import Npc


def create_random_npcs(count=20):
    for _ in range(count):
        Npc.objects.create()