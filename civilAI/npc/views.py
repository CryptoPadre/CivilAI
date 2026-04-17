from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Npc
from .serializers import NpcSerializer


class NpcListView(generics.ListAPIView):
    serializer_class = NpcSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Npc.objects.all().order_by("id")

        # bounding box params
        min_lat = self.request.query_params.get("min_lat")
        max_lat = self.request.query_params.get("max_lat")
        min_lng = self.request.query_params.get("min_lng")
        max_lng = self.request.query_params.get("max_lng")

        # filter only visible map area
        if all([min_lat, max_lat, min_lng, max_lng]):
            qs = qs.filter(
                latitude__gte=float(min_lat),
                latitude__lte=float(max_lat),
                longitude__gte=float(min_lng),
                longitude__lte=float(max_lng),
            )

        #  limit results for performance
        return qs[:1000]

    # 🔥 custom response (no pagination, no clustering)
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        return Response([
            {
                "id": npc.id,
                "latitude": npc.latitude,
                "longitude": npc.longitude,
                "first_name": npc.first_name,
                "last_name": npc.last_name,
                # optional extras:
                # "age": npc.age,
                # "icon": npc.icon,
            }
            for npc in qs
        ])


class NpcDetailView(generics.RetrieveAPIView):
    queryset = Npc.objects.all()
    serializer_class = NpcSerializer
    permission_classes = [AllowAny] 