from django.shortcuts import render
import django_filters.rest_framework
from rest_framework import permissions, generics, filters
from .serializers import NpcSerializer
from .models import Npc
from rest_framework.permissions import AllowAny

# Create your views here.


class  NpcListView(generics.ListCreateAPIView):
    serializer_class = NpcSerializer
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
    serializer_class = NpcSerializer