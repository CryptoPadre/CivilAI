import random


# ----------------------------
# CORE TRAIT EFFECT HELPERS
# ----------------------------
def apply_trait_bias(npc, trait, strength=1.0):
    """
    Small stat drift based on traits.
    Keeps evolution subtle, not overpowering.
    """

    if trait == "Kind":
        npc.empathy_level += int(1 * strength)
        npc.morality_level += int(1 * strength)

    elif trait == "Cruel":
        npc.aggression_level += int(1 * strength)
        npc.empathy_level -= int(1 * strength)

    elif trait == "Lazy":
        npc.fitness_level -= int(1 * strength)
        npc.energy_level += 1

    elif trait == "Hardworking":
        npc.fitness_level += int(1 * strength)
        npc.intelligence_level += int(1 * strength)

    elif trait == "Brave":
        npc.aggression_level += int(1 * strength)

    elif trait == "Cowardly":
        npc.aggression_level -= int(1 * strength)

    elif trait == "Friendly":
        npc.charisma_level += int(1 * strength)

    elif trait == "Rude":
        npc.charisma_level -= int(1 * strength)


# ----------------------------
# AGE 0–5 (FORMATION PHASE)
# ----------------------------
def evolve_0_5(npc):
    """
    Highly plastic stage:
    - Strong parental imprint
    - Weak self identity
    """

    if not npc.personality_traits:
        return

    for trait in npc.personality_traits:
        apply_trait_bias(npc, trait, strength=0.6)

    # randomness (environmental noise)
    if random.random() < 0.1:
        npc.happiness_level += 1

    npc.stress_level += random.randint(0, 1)


# ----------------------------
# AGE 5–12 (SOCIAL FORMATION)
# ----------------------------
def evolve_5_12(npc):
    """
    Social learning phase:
    - peers start influencing personality
    - traits stabilize
    """

    if not npc.personality_traits:
        return

    for trait in npc.personality_traits:
        apply_trait_bias(npc, trait, strength=0.8)

    # school/social pressure effects
    if npc.introversion_level > 70:
        npc.stress_level += 1
    else:
        npc.charisma_level += 1

    # small chance of trait shift (learning environment)
    if random.random() < 0.03:
        npc.happiness_level += random.randint(-1, 2)


# ----------------------------
# AGE 12–18 (IDENTITY FORMATION)
# ----------------------------
def evolve_12_18(npc):
    """
    Identity formation:
    - traits start changing
    - emotional volatility
    """

    if not npc.personality_traits:
        return

    for trait in npc.personality_traits:
        apply_trait_bias(npc, trait, strength=1.0)

    # emotional instability
    npc.stress_level += random.randint(0, 2)
    npc.happiness_level += random.randint(-1, 1)

    # trait mutation (important!)
    if random.random() < 0.05 and len(npc.personality_traits) < 4:
        all_traits = getattr(npc, "PERSONALITY_GOOD", []) + getattr(npc, "PERSONALITY_BAD", [])
        if all_traits:
            npc.personality_traits.append(random.choice(all_traits))


# ----------------------------
# ADULT (18+ STABILITY + DRIFT)
# ----------------------------
def evolve_adult(npc):
    """
    Stable personality:
    - small drift only
    - life events matter more than genetics
    """

    if not npc.personality_traits:
        return

    for trait in npc.personality_traits:
        apply_trait_bias(npc, trait, strength=0.3)

    # slow decay / aging pressure
    npc.energy_level -= random.randint(0, 1)

    # rare personality drift
    if random.random() < 0.01:
        npc.happiness_level += random.randint(-2, 2)

    # midlife small change
    if random.random() < 0.005:
        npc.aggression_level += random.choice([-1, 1])