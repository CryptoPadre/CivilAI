from django.urls import path
from .views import NpcMapView, NpcDetailView

urlpatterns = [
    path("npc/", NpcMapView.as_view(), name="npc-map"),
    path("npc/<int:pk>/", NpcDetailView.as_view(), name="npc-detail"),
]