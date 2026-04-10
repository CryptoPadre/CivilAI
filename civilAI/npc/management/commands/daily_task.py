from django.core.management.base import BaseCommand
from civilAI.npc.models import Npc
import random


class Command(BaseCommand):
    help = "Run daily NPC simulation tasks"

    TOLERANCE = 0.00001

    # ----------------------------
    # Personality behavior weights
    # ----------------------------
    PERSONALITY_EFFECTS = {
        "Honest": {"help": 1.3, "attack": 0.7},
        "Compassionate": {"help": 1.6, "attack": 0.4},
        "Kind": {"help": 1.5},
        "Brave": {"attack": 1.2},
        "Friendly": {"social": 1.3, "help": 1.2},

        "Cruel": {"attack": 1.6, "help": 0.4},
        "Selfish": {"help": 0.5},
        "Lazy": {"work": 0.5},
        "Aggressive": {"attack": 1.4},
        "Impatient": {"attack": 1.1},
    }

    def get_effect(self, npc, action, default=1.0):
        return self.PERSONALITY_EFFECTS.get(npc.personality, {}).get(action, default)

    def same_location(self, a, b):
        return (
            abs(a.latitude - b.latitude) < self.TOLERANCE and
            abs(a.longitude - b.longitude) < self.TOLERANCE
        )

    # ----------------------------
    # Actions
    # ----------------------------
    def attack(self, npc, target):
        attack_chance = (npc.aggression_level / 10) * self.get_effect(npc, "attack")

        if random.random() > attack_chance:
            return

        damage = 10

        if npc.aggression_level > 7:
            damage += 10

        if npc.morality_level < 3:
            damage += 10

        if target.age < 14:
            damage += 50

        if npc.fitness_level > target.fitness_level:
            target.health_level -= damage
            target.energy_level -= 20
            print(f"⚔️ {npc.first_name} attacked {target.first_name} (-{damage} HP)")
        else:
            npc.morality_level += 1
            print(f"🛡️ {target.first_name} defended against {npc.first_name}")

        npc.energy_level -= 20

    def help_each_other(self, npc, other):
        help_chance = 0.3 * self.get_effect(npc, "help")

        if random.random() > help_chance:
            return

        npc.happiness_level += 1
        other.happiness_level += 1

        npc.morality_level += 1
        other.morality_level += 1

        npc.energy_level -= 5
        other.energy_level -= 5

        print(f"🤝 {npc.first_name} helped {other.first_name}")

    def social(self, npc, other):
        social_chance = 0.4 * self.get_effect(npc, "social")

        if random.random() < social_chance:
            npc.charisma_level += 1
            other.charisma_level += 1

        print(f"💬 {npc.first_name} talked with {other.first_name}")

    def work(self, npc):
        work_chance = 0.4 * self.get_effect(npc, "work")

        if random.random() > work_chance:
            print(f"😴 {npc.first_name} skipped work")
            return

        npc.energy_level -= 10
        npc.fitness_level += 1
        npc.intelligence_level += 1

        print(f"💼 {npc.first_name} was working")

    # ----------------------------
    # Main loop
    # ----------------------------
    def handle(self, *args, **kwargs):
        npcs = list(Npc.objects.filter(is_alive=True, age__gte=15))

        print("\n===== DAILY NPC ACTIVITY =====\n")

        # 1. individual behavior
        for npc in npcs:
            if random.random() < 0.4:
                self.work(npc)
            else:
                print(f"😴 {npc.first_name} is resting")

        # 2. interactions
        for npc in npcs:
            for other in npcs:
                if npc.id == other.id:
                    continue

                if not self.same_location(npc, other):
                    continue

                action = random.random()

                if action < 0.3:
                    self.attack(npc, other)
                elif action < 0.6:
                    self.help_each_other(npc, other)
                else:
                    self.social(npc, other)

        # 3. save all changes
        for npc in npcs:
            npc.save()

        print("\n===== END OF DAY =====\n")