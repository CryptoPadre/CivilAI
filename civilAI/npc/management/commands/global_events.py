from django.core.management.base import BaseCommand
from django.db.models import F
from civilAI.npc.models import Npc
from civilAI.npc.utils import apply_npc_state_effects
import random


class Command(BaseCommand):
    help = "Global world events simulation"

    # -----------------------
    # LEADER ELECTION
    # -----------------------
    def leader_elections(self, npcs):
        Npc.objects.filter(is_leader=True).update(is_leader=False)

        def leadership_score(npc):
            score = 0

            # CORE SKILLS
            score += npc.charisma_level * 2
            score += npc.intelligence_level * 2
            score += npc.morality_level * 1

            # WEALTH
            score += npc.wealth * 0.01

            # JOB STATUS
            score += npc.job_level * 2

            high_status_jobs = [
                "CEO", "Politician", "Mayor", "Judge", "Bank Manager",
                "Military Officer", "Professor", "Scientist"
            ]

            if npc.occupation in high_status_jobs:
                score += 15

            # TRAITS
            traits = npc.personality_traits or []

            if "Brave" in traits:
                score += 2
            if "Honest" in traits:
                score += 3
            if "Friendly" in traits:
                score += 2
            if "Ambitious" in traits:
                score += 4
            if "Hardworking" in traits:
                score += 3
            if "Lazy" in traits:
                score -= 5

            # DEGENERATIVE CONDITIONS
            condition = npc.degenerative_condition

            if condition == "narcissist":
                score += 5
            elif condition == "sociopath":
                score += 4
            elif condition == "psychopath":
                score += 6
            elif condition == "paranoid":
                score -= 4

            return score

        if not npcs:
            return None

        sorted_npcs = sorted(npcs, key=leadership_score, reverse=True)

        leader = sorted_npcs[0]
        leader.is_leader = True
        leader.save(update_fields=["is_leader"])

        return leader

    # -----------------------
    # GLOBAL EVENTS (OPTIMIZED)
    # -----------------------

    def great_depression(self):
        Npc.objects.filter(is_alive=True).update(
            happiness_level=F("happiness_level") - 25,
            stress_level=F("stress_level") + 20,
            health_level=F("health_level") - 10,
        )

    def pandemic(self):
        # age-based logic must use conditional updates → split queries
        Npc.objects.filter(is_alive=True, age__lt=10).update(
            health_level=F("health_level") - 35,
            stress_level=F("stress_level") + 5,
        )

        Npc.objects.filter(is_alive=True, age__gte=10).update(
            health_level=F("health_level") - 20,
            stress_level=F("stress_level") + 5,
        )

    def golden_age(self):
        Npc.objects.filter(is_alive=True).update(
            happiness_level=F("happiness_level") + 15,
            stress_level=F("stress_level") - 10,
            health_level=F("health_level") + 5,
        )
    
    def natural_disaster(self):
        Npc.objects.filter(is_alive=True).update(
            health_level=F("health_level") - 30,
            happiness_level=F("happiness_level") - 20,
            stress_level=F("stress_level") + 25,
        )
        
    def run_global_event(self):
        events = [
            (self.golden_age, "Golden Age", 5),
            (self.pandemic, "Pandemic", 15),
            (self.great_depression, "Great Depression", 10),
            (self.natural_disaster, "Natural Disaster", 40),
        ]

        event = random.choices(
            events,
            weights=[w for _, _, w in events],
            k=1
        )[0]

        func, name, _ = event
        func()

        return name

    # -----------------------
    # MAIN HANDLE
    # -----------------------

    def handle(self, *args, **kwargs):
        npcs = list(Npc.objects.filter(is_alive=True, age__gte=20))

        if len(npcs) < 2:
            self.stdout.write("Not enough NPCs for election.")
            return

        leader = self.leader_elections(npcs)

        event_name = self.run_global_event()

        npcs = list(Npc.objects.filter(is_alive=True))

        for npc in npcs:
            apply_npc_state_effects(npc)
        
        Npc.objects.bulk_update(npcs,
        [
        "fitness_level", "intelligence_level", "aggression_level",
        "happiness_level", "stress_level", "charisma_level",
        "empathy_level", "morality_level", "health_level",
        "energy_level", "introversion_level", "creativity_level",
        ]
        )
        if leader:
            self.stdout.write(f"{leader.first_name} is leader")
        else:
            self.stdout.write("No leader selected")
        self.stdout.write(
            f"Global event: {event_name} occurred."
        )