from django.core.management.base import BaseCommand
from civilAI.npc.models import Npc
from civilAI.npc.inheritance import (
    evolve_0_5,
    evolve_5_12,
    evolve_12_18,
    evolve_adult
)
import random


class Command(BaseCommand):
    help = "Run daily NPC simulation tasks"

    # ----------------------------
    # CONFIG (life rules)
    # ----------------------------
    MIN_INTERACTION_AGE = 12
    MIN_WORK_AGE = 14
    MIN_ATTACK_AGE = 15

    TOLERANCE = 0.00001

    # ----------------------------
    # Personality behavior weights (NOW TRAIT-BASED)
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

    # ----------------------------
    # Helpers
    # ----------------------------
    def get_effect(self, npc, action, default=1.0):
        """
        Trait-based multiplier instead of single personality string.
        """
        multiplier = 1.0

        for trait in (npc.personality_traits or []):
            effects = self.PERSONALITY_EFFECTS.get(trait, {})
            multiplier *= effects.get(action, 1.0)

        return multiplier

    def same_location(self, a, b):
        return (
            abs(a.latitude - b.latitude) < self.TOLERANCE and
            abs(a.longitude - b.longitude) < self.TOLERANCE
        )

    # ----------------------------
    # ACTIONS (SAFE)
    # ----------------------------
    def attack(self, npc, target):
        if npc.age < self.MIN_ATTACK_AGE or target.age < self.MIN_ATTACK_AGE:
            return

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
        if npc.age < self.MIN_INTERACTION_AGE or other.age < self.MIN_INTERACTION_AGE:
            return

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
        if npc.age < self.MIN_INTERACTION_AGE or other.age < self.MIN_INTERACTION_AGE:
            return

        social_chance = 0.4 * (
            self.get_effect(npc, "social") +
            self.get_effect(other, "social")
        ) / 2

        if random.random() < social_chance:
            npc.charisma_level += 1
            other.charisma_level += 1

        print(f"💬 {npc.first_name} talked with {other.first_name}")

    def work(self, npc):
        if npc.age < self.MIN_WORK_AGE:
            return

        work_chance = 0.4 * self.get_effect(npc, "work")

        if random.random() > work_chance:
            print(f"😴 {npc.first_name} skipped work")
            return

        # ----------------------------
        # BASE WORK EFFECTS
        # ----------------------------
        npc.energy_level -= 10
        npc.fitness_level += 1
        npc.intelligence_level += 1
        npc.stress_level += 1

        print(f"💼 {npc.first_name} was working")

        # ----------------------------
        # PROMOTION SYSTEM
        # ----------------------------

        trait_bonus = 0
        leadership_bonus = 0

        traits = npc.personality_traits or []

        # Positive promotion traits
        if "Hardworking" in traits:
            trait_bonus += 2
        if "Intelligent" in traits or "Smart" in traits:
            trait_bonus += 2
        if "Disciplined" in traits:
            trait_bonus += 2
        if "Charismatic" in traits or "Friendly" in traits:
            leadership_bonus += 2
        if "Ambitious" in traits:
            trait_bonus += 3
            leadership_bonus += 1

        # Negative traits reduce promotion chance
        if "Lazy" in traits:
            trait_bonus -= 3
        if "Incompetent" in traits:
            trait_bonus -= 2

        # ----------------------------
        # DEGENERATIVE CONDITION EFFECTS
        # ----------------------------
        condition = getattr(npc, "degenerative_condition", "none")

        if condition in ["narcissist", "sociopath"]:
            leadership_bonus += 3
            trait_bonus += 1  # they still climb socially

        if condition == "psychopath":
            leadership_bonus += 4  # very high manipulation success
            trait_bonus -= 1      # unstable performance

        # ----------------------------
        # PROMOTION CHECK
        # ----------------------------
        promotion_score = (
            npc.intelligence_level * 0.3 +
            npc.charisma_level * 0.3 +
            npc.fitness_level * 0.1 +
            trait_bonus * 2 +
            npc.job_level * 0.2
        )

        # Leadership override chance
        leadership_chance = 0.02 + (leadership_bonus * 0.02)

        # Promote job level
        if random.random() < leadership_chance:
            npc.job_level += 2
            print(f"⬆️ {npc.first_name} jumped into leadership position")
        elif promotion_score > 20 and random.random() < 0.3:
            npc.job_level += 1
            print(f"📈 {npc.first_name} got promoted")

        # Salary scaling
        npc.salary += npc.job_level * 5

    # ----------------------------
    # MAIN LOOP
    # ----------------------------
    def handle(self, *args, **kwargs):
        npcs = list(
            Npc.objects.filter(
                is_alive=True,
                age__gte=self.MIN_INTERACTION_AGE
            )
        )

        print("\n===== DAILY NPC ACTIVITY =====\n")

        # 1. EVOLUTION FIRST (important)
        for npc in npcs:
            if npc.age <= 5:
                evolve_0_5(npc)
            elif npc.age <= 12:
                evolve_5_12(npc)
            elif npc.age <= 18:
                evolve_12_18(npc)
            else:
                evolve_adult(npc)

        # 2. individual behavior
        for npc in npcs:
            if npc.age >= self.MIN_WORK_AGE and random.random() < 0.4:
                self.work(npc)
            else:
                print(f"😴 {npc.first_name} is resting")

        # 3. interactions
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

        # 4. SAVE ONCE
        for npc in npcs:
            npc.save()

        print("\n===== END OF DAY =====\n")