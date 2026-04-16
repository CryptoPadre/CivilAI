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
    queryset = Npc.objects.all()
    """
    search_fields = [
         'first_name',
         'last_name'
        ]
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    ]
    """
    def get_queryset(self):
        qs = Npc.objects.all().order_by("id")

        min_lat = self.request.query_params.get("min_lat")
        max_lat = self.request.query_params.get("max_lat")
        min_lng = self.request.query_params.get("min_lng")
        max_lng = self.request.query_params.get("max_lng")

        if all([min_lat, max_lat, min_lng, max_lng]):
            qs = qs.filter(
                latitude__gte=min_lat,
                latitude__lte=max_lat,
                longitude__gte=min_lng,
                longitude__lte=max_lng,
            )

        return qs[:300]
    
    
class NpcDetailView(generics.RetrieveAPIView):
    queryset = Npc.objects.all()
    permission_classes = [AllowAny]
    serializer_class = NpcSerializer