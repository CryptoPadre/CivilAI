from rest_framework import serializers
from .models import Npc


class NpcSerializer(serializers.ModelSerializer):
    sex = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    personality = serializers.ReadOnlyField()
    fertility =  serializers.ReadOnlyField()
    sexual_orientation =  serializers.ReadOnlyField()
    fitness_level =  serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    
    class Meta:
        model = Npc
        fields = [
            'sex', 'first_name', 'last_name', 'age', 'personality', 'fertility', 'sexual_orientation', 'fitness_level', 'created_at'
            ]