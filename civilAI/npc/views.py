from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Npc
from .serializers import NpcSerializer


class NpcListView(generics.ListAPIView):
    serializer_class = NpcSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Npc.objects.only("id", "latitude", "longitude").order_by("id")

        min_lat = self.request.query_params.get("min_lat")
        max_lat = self.request.query_params.get("max_lat")
        min_lng = self.request.query_params.get("min_lng")
        max_lng = self.request.query_params.get("max_lng")

        if all([min_lat, max_lat, min_lng, max_lng]):
            try:
                qs = qs.filter(
                    latitude__gte=float(min_lat),
                    latitude__lte=float(max_lat),
                    longitude__gte=float(min_lng),
                    longitude__lte=float(max_lng),
                )
            except ValueError:
                return Npc.objects.none()

        return qs[:500]

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        return Response([
            {
                "id": npc.id,
                "latitude": npc.latitude,
                "longitude": npc.longitude,
            }
            for npc in qs
        ])


class NpcDetailView(generics.RetrieveAPIView):
    queryset = Npc.objects.all()
    serializer_class = NpcSerializer
    permission_classes = [AllowAny]