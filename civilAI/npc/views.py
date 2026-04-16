from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from collections import defaultdict
import math
from .serializers import NpcSerializer
from .models import Npc


class NpcListView(generics.ListAPIView):
    serializer_class = NpcSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Npc.objects.all().order_by("id")

        min_lat = self.request.query_params.get("min_lat")
        max_lat = self.request.query_params.get("max_lat")
        min_lng = self.request.query_params.get("min_lng")
        max_lng = self.request.query_params.get("max_lng")

        if all([min_lat, max_lat, min_lng, max_lng]):
            qs = qs.filter(
                latitude__gte=float(min_lat),
                latitude__lte=float(max_lat),
                longitude__gte=float(min_lng),
                longitude__lte=float(max_lng),
            )

        return qs[:300]

    
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        zoom = float(request.query_params.get("zoom", 10))

        # ----------------------------
        # ZOOMED IN → return real NPCs
        # ----------------------------
        if zoom < 5:
            return Response([
                {
                    "type": "npc",
                    "id": npc.id,
                    "latitude": npc.latitude,
                    "longitude": npc.longitude,
                    "first_name": npc.first_name,
                    "last_name": npc.last_name,
                }
                for npc in qs
            ])

        # ----------------------------
        # ZOOMED OUT → cluster
        # ----------------------------
        grid_size = 5 if zoom > 20 else 2

        clusters = defaultdict(list)

        for npc in qs:
            key = (
                math.floor(npc.latitude * grid_size),
                math.floor(npc.longitude * grid_size),
            )
            clusters[key].append(npc)

        results = []

        for items in clusters.values():
            lat = sum(n.latitude for n in items) / len(items)
            lng = sum(n.longitude for n in items) / len(items)

            results.append({
                "type": "cluster",
                "latitude": lat,
                "longitude": lng,
                "count": len(items),
            })

        return Response(results)
    
class NpcDetailView(generics.RetrieveAPIView):
    queryset = Npc.objects.all()
    serializer_class = NpcSerializer
    permission_classes = [AllowAny]