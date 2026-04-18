from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Npc
from .serializers import NpcSerializer
from collections import defaultdict
from rest_framework.views import APIView

class NpcMapView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            min_lat = float(request.query_params.get("min_lat"))
            max_lat = float(request.query_params.get("max_lat"))
            min_lng = float(request.query_params.get("min_lng"))
            max_lng = float(request.query_params.get("max_lng"))
        except (TypeError, ValueError):
            return Response({"detail": "Invalid or missing bounds."}, status=400)

        latitude_delta = float(request.query_params.get("latitudeDelta", 1.0))
        longitude_delta = float(request.query_params.get("longitudeDelta", 1.0))

        qs = Npc.objects.filter(
            is_alive=True,
            latitude__gte=min_lat,
            latitude__lte=max_lat,
            longitude__gte=min_lng,
            longitude__lte=max_lng,
        )

        # Zoomed out -> return clusters
        if latitude_delta > 0.3 or longitude_delta > 0.3:
            return Response(self.build_clusters(qs, latitude_delta, longitude_delta))

        # Zoomed in -> return actual NPCs
        npcs = qs.only(
            "id", "latitude", "longitude", "first_name", "last_name"
        )[:2000]

        return Response([
            {
                "type": "npc",
                "id": npc.id,
                "latitude": npc.latitude,
                "longitude": npc.longitude,
                "first_name": npc.first_name,
                "last_name": npc.last_name,
            }
            for npc in npcs
        ])

    def build_clusters(self, qs, latitude_delta, longitude_delta):
        # Grid cell size based on zoom
        # Bigger cells when zoomed out
        cell_size_lat = max(latitude_delta / 12, 0.02)
        cell_size_lng = max(longitude_delta / 12, 0.02)

        buckets = defaultdict(lambda: {
            "count": 0,
            "lat_sum": 0.0,
            "lng_sum": 0.0,
        })

        for npc in qs.only("latitude", "longitude").iterator(chunk_size=5000):
            cell_lat = round(npc.latitude / cell_size_lat)
            cell_lng = round(npc.longitude / cell_size_lng)
            key = (cell_lat, cell_lng)

            buckets[key]["count"] += 1
            buckets[key]["lat_sum"] += npc.latitude
            buckets[key]["lng_sum"] += npc.longitude

        results = []
        for bucket in buckets.values():
            count = bucket["count"]
            results.append({
                "type": "cluster",
                "latitude": bucket["lat_sum"] / count,
                "longitude": bucket["lng_sum"] / count,
                "count": count,
            })

        return results


class NpcDetailView(generics.RetrieveAPIView):
    queryset = Npc.objects.all()
    serializer_class = NpcSerializer
    permission_classes = [AllowAny] 