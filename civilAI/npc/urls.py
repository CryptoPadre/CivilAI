from django.urls import path
from . import views

urlpatterns = [
    path('npc/', views.NpcListView.as_view()),
    path('npc/<int:pk>', views.NpcDetailView.as_view())
   
]