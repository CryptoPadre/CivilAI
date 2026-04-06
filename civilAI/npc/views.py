from django.shortcuts import render
import django_filters.rest_framework
from rest_framework import permissions, generics, filters
from .serializers import NpcSerializer
from .models import Npc

# Create your views here.


class  NpcListView(generics.ListCreateAPIView):
    serializer_class = NpcSerializer
    queryset = Npc.objects.all().order_by('-born_at')
     
    search_fields = [
         'first_name',
         'last_name'
        ]
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    ]
    
    
class NpcDetailView(generics.RetrieveAPIView):
    queryset = Npc.objects.all()
    serializer_class = NpcSerializer