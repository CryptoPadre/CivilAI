from django.shortcuts import render
from rest_framework import permissions, generics, filters
from .serializers import NpcSerializer
from .models import Npc

# Create your views here.


class  NpcListView(generics.ListCreateAPIView):
    serializer_class = NpcSerializer
    queryset = Npc.objects.all().order_by('-created_at')
     
    search_fields = [
         'first_name',
         'last_name'
        ]

class NpcDetailView(generics.RetrieveAPIView):
    queryset = Npc.objects.all()
    serializer_class = NpcSerializer