from rest_framework import serializers
from .models import Npc


class NpcSerializer(serializers.ModelSerializer):
    previous_partners = serializers.StringRelatedField(many=True)  # Serializes ManyToMany
    mother = serializers.StringRelatedField()  # FK
    father = serializers.StringRelatedField()
    
    
    class Meta:
        model = Npc
        fields = [
            'sex', 'first_name', 'last_name', 'age', 'personality_traits', 'fertility', 'sexual_orientation', 'previous_partners', 'fitness_level', 
            'is_adventurous', 'born_at', 'mother', 'father', 'intelligence_level','aggression_level','happiness_level','stress_level','charisma_level',
            'empathy_level', 'morality_level', 'health_level', 'energy_level','introversion_level', 'latitude', 'longitude', 'occupation', 'job_level','wealth', 'personality_traits'
            ]
        read_only_fields = fields