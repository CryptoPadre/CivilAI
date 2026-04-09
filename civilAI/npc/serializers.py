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
    is_adventurous = serializers.ReadOnlyField()
    born_at = serializers.ReadOnlyField()
    mother = serializers.ReadOnlyField()
    father = serializers.ReadOnlyField()
    intelligence_level = serializers.ReadOnlyField()
    aggression_level = serializers.ReadOnlyField()
    happiness_level = serializers.ReadOnlyField()
    stress_level = serializers.ReadOnlyField()
    charisma_level = serializers.ReadOnlyField()
    empathy_level = serializers.ReadOnlyField()
    morality_level = serializers.ReadOnlyField()
    health_level = serializers.ReadOnlyField()
    energy_level = serializers.ReadOnlyField()
    introversion_level = serializers.ReadOnlyField()
    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()
    
    
    class Meta:
        model = Npc
        fields = [
            'sex', 'first_name', 'last_name', 'age', 'personality', 'fertility', 'sexual_orientation', 'fitness_level', 
            'is_adventurous', 'born_at', 'mother', 'father', 'intelligence_level','aggression_level','happiness_level','stress_level','charisma_level',
            'empathy_level', 'morality_level', 'health_level', 'energy_level','introversion_level', 'latitude', 'longitude'
            ]