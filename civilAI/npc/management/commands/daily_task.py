from django.core.management.base import BaseCommand
from civilAI.npc.models import Npc
from civilAI.npc.inheritance import (
    evolve_0_5,
    evolve_5_12,
    evolve_12_18,
    evolve_adult
)
import random
from collections import defaultdict


class Command(BaseCommand):
    help = "Run daily NPC simulation tasks"

    MIN_INTERACTION_AGE = 12
    MIN_WORK_AGE = 14
    MIN_ATTACK_AGE = 15

    # ----------------------------
    # PERSONALITY EFFECTS
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
    def get_effect(self, npc, action):
        multiplier = 1.0
        for trait in (npc.personality_traits or []):
            multiplier *= self.PERSONALITY_EFFECTS.get(trait, {}).get(action, 1.0)
        return multiplier

    # ----------------------------
    # ACTIONS
    # ----------------------------
    def attack(self, npc, target):
        if npc.age < self.MIN_ATTACK_AGE or target.age < self.MIN_ATTACK_AGE:
            return

        chance = (npc.aggression_level / 10) * self.get_effect(npc, "attack")

        if random.random() > chance:
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
        else:
            npc.morality_level += 1

        npc.energy_level -= 20

    def help_each_other(self, npc, other):
        if npc.age < self.MIN_INTERACTION_AGE or other.age < self.MIN_INTERACTION_AGE:
            return

        if random.random() > 0.3 * self.get_effect(npc, "help"):
            return

        npc.happiness_level += 10
        other.happiness_level += 10
        npc.morality_level += 10
        other.morality_level += 10
        npc.aggression_level -= 10
        other.aggression_level -= 10
        npc.energy_level -= 5
        other.energy_level -= 5

    def social(self, npc, other):
        if npc.age < self.MIN_INTERACTION_AGE or other.age < self.MIN_INTERACTION_AGE:
            return

        chance = 0.4 * (
            self.get_effect(npc, "social") +
            self.get_effect(other, "social")
        ) / 2

        if random.random() < chance:
            npc.charisma_level += 1
            other.charisma_level += 1
            npc.happiness_level += 10
            other.happiness_level += 10
            npc.morality_level += 10
            other.morality_level += 10
            npc.aggression_level -= 10
            other.aggression_level -= 10

    def work(self, npc):
        if npc.age < self.MIN_WORK_AGE:
            return

        if random.random() > 0.4 * self.get_effect(npc, "work"):
            return

        npc.energy_level -= 10
        npc.fitness_level += 1
        npc.intelligence_level += 1
        npc.stress_level += 1
        npc.introversion_level -= 10

        trait_bonus = 0
        leadership_bonus = 0
        traits = npc.personality_traits or []

        if "Hardworking" in traits:
            trait_bonus += 1
        if "Ambitious" in traits:
            trait_bonus += 3
            leadership_bonus += 1
        if "Lazy" in traits:
            trait_bonus -= 3

        condition = getattr(npc, "degenerative_condition", "none")

        if condition in ["narcissist", "sociopath"]:
            leadership_bonus += 3
        elif condition == "psychopath":
            leadership_bonus += 4
            trait_bonus -= 1

        promotion_score = (
            npc.intelligence_level * 0.3 +
            npc.charisma_level * 0.3 +
            npc.fitness_level * 0.1 +
            trait_bonus * 2 +
            npc.job_level * 0.2
        )

        leadership_chance = 0.02 + (leadership_bonus * 0.02)

        if random.random() < leadership_chance:
            npc.job_level += 2
            npc.happiness_level += 10
            npc.stress_level -= 10
        elif promotion_score > 20 and random.random() < 0.3:
            npc.job_level += 1
            npc.happiness_level += 5
            npc.stress_level -= 5

        npc.salary += npc.job_level * 2
        npc.wealth += npc.salary
        if npc.wealth > npc.salary * 24:
            npc.happiness_level += 15
            npc.stress_level -= 15
            npc.introuversion_level -= 15
            

    # ----------------------------
    # MAIN
    # ----------------------------
    def handle(self, *args, **kwargs):

        npcs = list(
            Npc.objects.filter(
                is_alive=True,
                age__gte=self.MIN_INTERACTION_AGE
            )
        )

        # ----------------------------
        # 1. EVOLUTION
        # ----------------------------
        for npc in npcs:
            if npc.age <= 5:
                evolve_0_5(npc)
            elif npc.age <= 12:
                evolve_5_12(npc)
            elif npc.age <= 18:
                evolve_12_18(npc)
            else:
                evolve_adult(npc)

        # ----------------------------
        # 2. WORK / REST
        # ----------------------------
        for npc in npcs:
            if npc.age >= self.MIN_WORK_AGE:
                self.work(npc)

        # ----------------------------
        # 3. GROUP BY LOCATION (KEY OPTIMIZATION)
        # ----------------------------
        location_groups = defaultdict(list)

        for npc in npcs:
            key = (round(npc.latitude, 4), round(npc.longitude, 4))
            location_groups[key].append(npc)

        # ----------------------------
        # 4. INTERACTIONS (REDUCED)
        # ----------------------------
        for group in location_groups.values():
            size = len(group)

            for i in range(size):
                for j in range(i + 1, size):

                    if random.random() > 0.3:  # limit interactions
                        continue

                    npc = group[i]
                    other = group[j]

                    action = random.random()

                    if action < 0.3:
                        self.attack(npc, other)
                    elif action < 0.6:
                        self.help_each_other(npc, other)
                    else:
                        self.social(npc, other)

        # ----------------------------
        # 5. SAVE (SINGLE DB HIT)
        # ----------------------------
        Npc.objects.bulk_update(
            npcs,
            [
                "fitness_level", "intelligence_level", "aggression_level",
                "happiness_level", "stress_level", "charisma_level",
                "empathy_level", "morality_level", "health_level",
                "energy_level", "introversion_level", "creativity_level",
                "job_level", "salary", "wealth",
            ]
        )

        self.stdout.write(f"Processed {len(npcs)} NPCs")