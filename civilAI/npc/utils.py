from civilAI.npc.models import Npc

def create_random_npcs(count=50):
    for _ in range(count):
        Npc.objects.create()