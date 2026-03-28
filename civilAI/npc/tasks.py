from celery import shared_task
from django.utils import timezone
from .models import Npc

@shared_task
def update_npc_ages():
    now = timezone.now()
    for npc in Npc.objects.all():
        delta = now - npc.created_at
        npc.age = npc.initial_age + int(delta.total_seconds() // 6)
        npc.save(update_fields=['age'])
    print("NPC ages updated")