from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import random


class Npc(models.Model):
    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    FERTILITY_RATE = [
        ("H", "High"),
        ("N", "Normal"),
        ("L", "Low"),
    ]

    FERTILITY_WEIGHTS = {
        "H": 0.5,
        "N": 0.35,
        "L": 0.15,
    }

    ORIENTATION_CHOICES = [
        ("hetero", "Heterosexual"),
        ("gay", "Gay"),
        ("bi", "Bisexual"),
        ("other", "Other"),
    ]

    DEGENERATIVE_CHOICES = [
        ("none", "None"),
        ("sociopath", "Sociopath"),
        ("psychopath", "Psychopath"),
        ("paranoid", "Paranoid"),
        ("narcissist", "Narcissist"),
    ]

    SPAWN_LOCATIONS = [
        ("Warsaw, Poland", 52.2297, 21.0122),
        ("Krakow, Poland", 50.0647, 19.9450),
        ("Gdansk, Poland", 54.3520, 18.6466),

        ("Madrid, Spain", 40.4168, -3.7038),
        ("Barcelona, Spain", 41.3874, 2.1686),
        ("Valencia, Spain", 39.4699, -0.3763),

        ("Rome, Italy", 41.9028, 12.4964),
        ("Milan, Italy", 45.4642, 9.1900),
        ("Naples, Italy", 40.8518, 14.2681),

        ("London, UK", 51.5072, -0.1276),
        ("Manchester, UK", 53.4808, -2.2426),
        ("Edinburgh, UK", 55.9533, -3.1883),

        ("Reykjavik, Iceland", 64.1466, -21.9426),

        ("Los Angeles, USA", 34.0522, -118.2437),
        ("San Francisco, USA", 37.7749, -122.4194),
        ("Seattle, USA", 47.6062, -122.3321),

        ("New York, USA", 40.7128, -74.0060),
        ("Boston, USA", 42.3601, -71.0589),
        ("Miami, USA", 25.7617, -80.1918),

        ("Chicago, USA", 41.8781, -87.6298),
        ("Denver, USA", 39.7392, -104.9903),
        ("Kansas City, USA", 39.0997, -94.5786),

        ("Brasilia, Brazil", -15.7939, -47.8828),
        ("Sao Paulo, Brazil", -23.5505, -46.6333),
        ("Rio de Janeiro, Brazil", -22.9068, -43.1729),

        ("Buenos Aires, Argentina", -34.6037, -58.3816),
        ("Cordoba, Argentina", -31.4201, -64.1888),
        ("Rosario, Argentina", -32.9442, -60.6505),

        ("Mumbai, India", 19.0760, 72.8777),
        ("Chennai, India", 13.0827, 80.2707),
        ("Singapore", 1.3521, 103.8198),
        ("Bali, Indonesia", -8.3405, 115.0920),
        ("Tehran, Iran", 35.6892, 51.3890),
        ("Dubai, UAE", 25.2048, 55.2708),
        ("Tokyo, Japan", 35.6762, 139.6503),
        ("Sydney, Australia", -33.8688, 151.2093),
        ("Brisbane, Australia", -27.4698, 153.0251),
    ]

    MALE_FIRST_NAMES = [
        "Adam", "Mateusz", "Lukasz", "Jakub", "Kacper",
        "Piotr", "Tomasz", "Michal", "Jan", "Andrzej",
        "Marcin", "Marek", "Patryk", "Damian", "Sebastian",
        "Filip", "Szymon", "Matei", "Viktor", "Nikolas",
        "Dmitri", "Alexei", "Ivan", "Pavel", "Roman",
        "Bartosz", "Rafal", "Grzegorz", "Jozef", "Ladislav",
        "Kamil", "David", "Martin", "Vladimir", "Olek",
        "Jaroslav", "Tibor", "Gabor", "Zoltan", "Csaba",
        "Ruben", "Maxim", "Igor", "Konrad", "Milos",
        "Tadeusz", "Emil", "Anton", "Andrei", "Sergei",
        "Heinrich", "Friedrich", "Karl", "Ludwig", "Wilhelm",
        "Ernst", "Rudolf", "Gustav", "Dietrich", "Albrecht",
        "Johann", "Konrad", "Otto", "Hermann", "Wolfgang",
        "Manfred", "Siegfried", "Bernhard", "Axel", "Ulrich",
    ]

    FEMALE_FIRST_NAMES = [
        "Anna", "Katarzyna", "Magdalena", "Aleksandra", "Natalia",
        "Zuzanna", "Julia", "Maria", "Ewa", "Patrycja",
        "Monika", "Agnieszka", "Karolina", "Martyna", "Gabriela",
        "Helena", "Veronika", "Lucia", "Ivana", "Sofia",
        "Elena", "Anastasia", "Daria", "Viktoria", "Olga",
        "Milena", "Tereza", "Kristina", "Jana", "Michaela",
        "Simona", "Barbara", "Lea", "Nina", "Lidia",
        "Irena", "Tatiana", "Alina", "Beata", "Emilia",
        "Renata", "Sabina", "Viola", "Danica", "Marta",
        "Inna", "Raisa", "Zofia", "Clara", "Lana",
        "Greta", "Heidi", "Liselotte", "Katrin", "Brigitte",
        "Gisela", "Anneliese", "Ingrid", "Ursula", "Hannelore",
        "Marlene", "Sibylle", "Elke", "Renate", "Klara",
        "Franziska", "Angelika", "Lorelei", "Astrid", "Edith",
    ]

    LAST_NAMES = [
        "Kowalski", "Nowak", "Wisniewski", "Wojcik", "Kaminski",
        "Lewandowski", "Zielinski", "Szymanski", "Wozniak", "Dabrowski",
        "Kozlowski", "Jankowski", "Mazur", "Wojciechowski", "Kwiatkowski",
        "Krawczyk", "Kaczmarek", "Piotrowski", "Grabowski", "Pawlak",
        "Michalski", "Nowicki", "Adamczyk", "Wieczorek", "Majewski",
        "Ostrowski", "Jaworski", "Malinowski", "Gorski", "Rutkowski",
        "Toth", "Nagy", "Kovacs", "Horvath", "Szabo",
        "Novak", "Svoboda", "Dvorak", "Marek", "Urban",
        "Petrov", "Ivanov", "Smirnov", "Popov", "Sokolov",
        "Varga", "Farkas", "Balazs", "Jelen", "Mikulas",
        "Schneider", "Fischer", "Weber", "Muller", "Schmidt",
        "Kaiser", "Becker", "Hoffmann", "Schulz", "Zimmermann",
        "Braun", "Koch", "Richter", "Wolf", "Neumann",
        "Schwarz", "Bauer", "Hartmann", "Schreiber", "Vogel",
    ]

    PERSONALITY_GOOD = [
        "Honest", "Compassionate", "Loyal", "Brave", "Patient",
        "Generous", "Humble", "Optimistic", "Kind", "Responsible",
        "Respectful", "Trustworthy", "Courageous", "Friendly",
        "Forgiving", "Creative", "Reliable", "Empathetic", "Gentle",
        "Considerate", "Cheerful", "Modest", "Diligent", "Wise",
        "Supportive", "Fair", "Peaceful", "Sincere", "Curious",
        "Thoughtful", "Hardworking", "Attentive", "Grateful",
        "Adventurous", "Flexible", "Persevering", "Tolerant",
        "Protective", "Devoted", "Innovative", "Balanced",
        "Disciplined", "Practical", "Charitable", "Alert",
        "Caring", "Honorable", "Nurturing", "Observant",
    ]

    PERSONALITY_BAD = [
        "Deceitful", "Cruel", "Disloyal", "Cowardly", "Impatient",
        "Selfish", "Arrogant", "Pessimistic", "Mean", "Irresponsible",
        "Jealous", "Greedy", "Lazy", "Rude", "Vindictive", "Stubborn",
        "Dishonest", "Manipulative", "Impolite", "Narrow-minded",
        "Inconsiderate", "Spiteful", "Gossipy", "Short-tempered",
        "Unreliable", "Overcritical", "Unforgiving", "Boastful",
        "Reckless", "Overbearing", "Impulsive", "Indecisive",
        "Hasty", "Self-centered", "Untrustworthy", "Needy",
        "Cynical", "Resentful", "Careless", "Obnoxious",
        "Controlling", "Sullen", "Insensitive", "Harsh",
        "Pompous", "Loud",
    ]

    TRAIT_EFFECTS = {
        "Kind": {"empathy_level": 2, "morality_level": 1},
        "Cruel": {"empathy_level": -2, "aggression_level": 2},
        "Brave": {"aggression_level": 1},
        "Cowardly": {"aggression_level": -1},
        "Lazy": {"fitness_level": -2},
        "Hardworking": {"fitness_level": 2},
        "Generous": {"morality_level": 2},
        "Greedy": {"morality_level": -2},
        "Friendly": {"charisma_level": 2},
        "Rude": {"charisma_level": -2},
    }

    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    age = models.IntegerField(default=0)
    initial_age = models.IntegerField(null=True, blank=True)
    born_at = models.DateTimeField(default=timezone.now)

    is_alive = models.BooleanField(default=True)
    died_at = models.DateTimeField(null=True, blank=True)

    personality_traits = models.JSONField(default=list)

    is_adventurous = models.BooleanField(default=False)
    is_leader = models.BooleanField(default=False)

    fertility = models.CharField(
        max_length=6,
        choices=FERTILITY_RATE,
        blank=True,
    )

    previous_partners = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="partnered_with",
    )

    sexual_orientation = models.CharField(
        max_length=10,
        choices=ORIENTATION_CHOICES,
        default="hetero",
    )

    mother = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children_from_mother",
    )

    father = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children_from_father",
    )

    has_kids = models.BooleanField(default=False)

    degenerative_condition = models.CharField(
        max_length=20,
        choices=DEGENERATIVE_CHOICES,
        default="none",
    )

    fitness_level = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    intelligence_level = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    aggression_level = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    happiness_level = models.IntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])
    stress_level = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    charisma_level = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    empathy_level = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    morality_level = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    health_level = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    energy_level = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    introversion_level = models.IntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])
    creativity_level = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    occupation = models.CharField(max_length=50, default="Unemployed")
    wealth = models.IntegerField(default=0)
    job_level = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    salary = models.IntegerField(default=0)

    spawn_location = models.CharField(max_length=100, blank=True, default="")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def clamp_stat(self, value):
        return max(0, min(100, value))

    def assign_spawn_location(self):
        location_name, lat, lon = random.choice(self.SPAWN_LOCATIONS)
        self.spawn_location = location_name
        self.latitude = lat
        self.longitude = lon

    def save(self, *args, **kwargs):
        from civilAI.npc.work import assign_job_by_traits

        is_new = self.pk is None

        if not self.sex:
            self.sex = random.choice(["M", "F"])

        if not self.first_name:
            names = self.MALE_FIRST_NAMES if self.sex == "M" else self.FEMALE_FIRST_NAMES
            self.first_name = random.choice(names)

        if not self.last_name:
            self.last_name = random.choice(self.LAST_NAMES)

        if is_new and self.initial_age is None:
            self.initial_age = random.randint(10, 60)
            self.age = self.initial_age

        if is_new and not self.spawn_location:
            self.assign_spawn_location()

        if self.fitness_level == 0:
            self.fitness_level = random.randint(1, 10)

        if self.intelligence_level == 0:
            self.intelligence_level = random.randint(1, 10)

        if self.stress_level == 0:
            self.stress_level = random.randint(1, 10)

        if self.empathy_level == 0:
            self.empathy_level = random.randint(1, 10)

        if self.aggression_level == 0:
            self.aggression_level = random.randint(1, 10)

        if self.morality_level == 0:
            self.morality_level = random.randint(1, 10)

        if self.charisma_level == 0:
            self.charisma_level = random.randint(1, 10)

        if self.creativity_level == 0:
            self.creativity_level = random.randint(1, 10)

        if self.introversion_level == 50:
            self.introversion_level = random.randint(0, 100)

        if is_new:
            self.is_adventurous = random.random() < 0.2

        if not self.fertility:
            self.fertility = random.choices(
                population=["H", "N", "L"],
                weights=[
                    self.FERTILITY_WEIGHTS["H"],
                    self.FERTILITY_WEIGHTS["N"],
                    self.FERTILITY_WEIGHTS["L"],
                ],
                k=1,
            )[0]

        if self.mother and self.father and self.mother == self.father:
            self.father = None

        if is_new and self.degenerative_condition == "none":
            if random.random() < 0.01:
                self.degenerative_condition = random.choice(
                    [choice[0] for choice in self.DEGENERATIVE_CHOICES if choice[0] != "none"]
                )

        if not self.personality_traits:
            all_traits = self.PERSONALITY_GOOD + self.PERSONALITY_BAD
            self.personality_traits = random.sample(all_traits, k=random.randint(2, 3))

        if is_new:
            for trait in self.personality_traits:
                effects = self.TRAIT_EFFECTS.get(trait, {})

                for field, modifier in effects.items():
                    current_value = getattr(self, field)
                    setattr(self, field, self.clamp_stat(current_value + modifier))

            assign_job_by_traits(self)

        super().save(*args, **kwargs)

    @property
    def has_family(self):
        return (
            self.children_from_mother.exists()
            or self.children_from_father.exists()
        )

    def generate_personality_label(self):
        if not self.personality_traits:
            return "Neutral"

        return random.choice(self.personality_traits)

    def develop_personality(self):
        pass

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.spawn_location}"