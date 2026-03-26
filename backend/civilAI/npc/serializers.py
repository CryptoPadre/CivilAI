from rest_framework import serializers
from .models import Npc


class NpcSerializer(serializers.ModelSerializer):
    sex = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    personality = serializers.ReadOnlyField()
    
    class Meta:
        model = Npc
        fields = [
            'sex', 'first_name', 'last_name', 'age', 'personality','created_at'
            ]