from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import random
from django.utils import timezone


class Npc(models.Model):
    SEX_CHOICES = [('M','Male'),('F','Female')]
    
    FERTILITY_RATE = [('H',"High"), ('N',"Normal"), ('L',"Low")]
    
    FERTILITY_WEIGHTS = {
        'H': 0.5,   # 50% of population
        'N': 0.35,  # 35%
        'L': 0.15   # 15%
    }

    ORIENTATION_CHOICES = [
        ('hetero', 'Heterosexual'),
        ('gay', 'Gay'),
        ('bi', 'Bisexual'),
        ('other', 'Other'),
    ]

    # Male First Names
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
        # Germanic additions
        "Heinrich", "Friedrich", "Karl", "Ludwig", "Wilhelm",
        "Ernst", "Rudolf", "Gustav", "Dietrich", "Albrecht",
        "Johann", "Konrad", "Otto", "Hermann", "Wolfgang",
        "Manfred", "Siegfried", "Bernhard", "Axel", "Ulrich"
    ]

    # Female First Names
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
        # Germanic additions
        "Greta", "Heidi", "Liselotte", "Katrin", "Brigitte",
        "Gisela", "Anneliese", "Ingrid", "Ursula", "Hannelore",
        "Marlene", "Sibylle", "Elke", "Renate", "Klara",
        "Franziska", "Angelika", "Lorelei", "Astrid", "Edith"
    ]

    # Last Names
    LAST_NAMES = [
        "Kowalski", "Nowak", "Wiśniewski", "Wójcik", "Kamiński",
        "Lewandowski", "Zieliński", "Szymański", "Woźniak", "Dąbrowski",
        "Kozłowski", "Jankowski", "Mazur", "Wojciechowski", "Kwiatkowski",
        "Krawczyk", "Kaczmarek", "Piotrowski", "Grabowski", "Pawlak",
        "Michalski", "Nowicki", "Adamczyk", "Wieczorek", "Majewski",
        "Ostrowski", "Jaworski", "Malinowski", "Górski", "Rutkowski",
        "Tóth", "Nagy", "Kovács", "Horváth", "Szabó",
        "Novák", "Svoboda", "Dvořák", "Marek", "Urban",
        "Petrov", "Ivanov", "Smirnov", "Popov", "Sokolov",
        "Varga", "Farkas", "Balázs", "Jelen", "Mikuláš",
        # Germanic additions
        "Schneider", "Fischer", "Weber", "Müller", "Schmidt",
        "Kaiser", "Becker", "Hoffmann", "Schulz", "Zimmermann",
        "Braun", "Koch", "Richter", "Wolf", "Neumann",
        "Schwarz", "Bauer", "Hartmann", "Schreiber", "Vogel"
    ]
    PERSONALITY_GOOD = [
    "Honest", "Compassionate", "Loyal", "Brave", "Patient", "Generous", "Humble", "Optimistic", "Kind", "Responsible",
    "Respectful", "Trustworthy", "Courageous", "Friendly", "Forgiving", "Creative", "Reliable", "Empathetic", "Gentle", "Considerate",
    "Cheerful", "Modest", "Diligent", "Wise", "Supportive", "Fair", "Peaceful", "Sincere", "Curious", "Thoughtful",
    "Hardworking", "Attentive", "Grateful", "Adventurous", "Flexible", "Persevering", "Tolerant", "Protective", "Devoted",
    "Innovative", "Balanced", "Disciplined", "Practical", "Charitable", "Alert", "Caring", "Honorable",
    "Nurturing", "Observant"
]

    PERSONALITY_BAD = [
    "Deceitful", "Cruel", "Disloyal", "Cowardly", "Impatient", "Selfish", "Arrogant", "Pessimistic", "Mean", "Irresponsible",
    "Jealous", "Greedy", "Lazy", "Rude", "Vindictive", "Stubborn", "Dishonest", "Manipulative", "Impolite", "Narrow-minded",
    "Inconsiderate", "Spiteful", "Gossipy", "Short-tempered", "Unreliable", "Overcritical", "Unforgiving", "Boastful", "Reckless",
    "Overbearing", "Impulsive", "Indecisive", "Hasty", "Self-centered", "Untrustworthy", "Needy", "Cynical", "Resentful",
    "Careless", "Obnoxious", "Controlling", "Sullen", "Insensitive", "Harsh", "Pompous", "Loud"
]
    
    DEGENERATIVE_CHOICES = [
    ('none', 'None'),
    ('sociopath', 'Sociopath'),
    ('psychopath', 'Psychopath'),
    ('pedophile', 'Pedophile'),
    ('paranoid', 'Paranoid'),
    ('narcissist', 'Narcissist'),
]
    TRAIT_EFFECTS = {
    "Kind": {"empathy_level": +2, "morality_level": +1},
    "Cruel": {"empathy_level": -2, "aggression_level": +2},
    "Brave": {"aggression_level": +1},
    "Cowardly": {"aggression_level": -1},
    "Lazy": {"fitness_level": -2},
    "Hardworking": {"fitness_level": +2},
    "Generous": {"morality_level": +2},
    "Greedy": {"morality_level": -2},
    "Friendly": {"charisma_level": +2},
    "Rude": {"charisma_level": -2},
}

    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField(default=0) 
    personality_traits = models.JSONField(default=list)
    born_at = models.DateTimeField(default=timezone.now)
    initial_age = models.IntegerField(null=True, blank=True) 
    is_alive = models.BooleanField(default=True)
    died_at = models.DateTimeField(null=True, blank=True)

    is_adventurous = models.BooleanField(default=False)
    is_leader = models.BooleanField(default=False)

    fertility = models.CharField(max_length=6, choices=FERTILITY_RATE)
    previous_partners = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name='partnered_with')
    sexual_orientation = models.CharField(
        max_length=10,
        choices=ORIENTATION_CHOICES,
        default='hetero'
    )

    mother = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children_from_mother'
    )

    father = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children_from_father'
    )
    has_kids = models.BooleanField(default=False)
    degenerative_condition = models.CharField(
        max_length=20,
        choices=DEGENERATIVE_CHOICES,
        default='none'
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
    latitude = models.FloatField(default=49.2992, db_index=True)
    longitude = models.FloatField(default=19.9496, db_index=True)

    def save(self, *args, **kwargs):
        from civilAI.npc.work import assign_job_by_traits
        # Sex
        if not self.sex:
            self.sex = random.choice(['M', 'F'])

        # Names
        if not self.first_name:
            self.first_name = random.choice(
                self.MALE_FIRST_NAMES if self.sex == 'M' else self.FEMALE_FIRST_NAMES
            )

        if not self.last_name:
            self.last_name = random.choice(self.LAST_NAMES)
            
        # Initial age
        if not self.pk and self.initial_age is None:
            self.initial_age = random.randint(10, 60)
            self.age = self.initial_age
        
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

        # Introversion default
        if self.introversion_level == 50:
            self.introversion_level = random.randint(0, 100)
            
        if self.creativity_level == 0:
            self.creativity_level = random.randint(1, 10)
        # Adventurous trait (random ~20%)
        if not self.pk:
            self.is_adventurous = random.random() < 0.2

        # Fertility assignment (weighted)
        if not self.fertility:
            self.fertility = random.choices(
                population=['H', 'N', 'L'],
                weights=[
                    self.FERTILITY_WEIGHTS['H'],
                    self.FERTILITY_WEIGHTS['N'],
                    self.FERTILITY_WEIGHTS['L']
                ],
                k=1
            )[0]

        # Prevent same parent
        if self.mother and self.father and self.mother == self.father:
            self.father = None
            
        if not self.pk and self.degenerative_condition == 'none':
            if random.random() < 0.01:  # 1% chance
                self.degenerative_condition = random.choice(
                    [c[0] for c in self.DEGENERATIVE_CHOICES if c[0] != 'none']
                )
        if not self.pk and not self.personality_traits:
            all_traits = self.PERSONALITY_GOOD + self.PERSONALITY_BAD
            self.personality_traits = random.sample(all_traits, k=random.randint(2, 3))

        # -------------------------
        # ENSURE TRAITS
        # -------------------------
        if not self.personality_traits:
            all_traits = self.PERSONALITY_GOOD + self.PERSONALITY_BAD
            self.personality_traits = random.sample(all_traits, k=random.randint(2, 3))

        # -------------------------
        # APPLY TRAIT EFFECTS (ONLY ON CREATE)
        # -------------------------
        if not self.pk:
            for trait in self.personality_traits:
                effects = self.TRAIT_EFFECTS.get(trait, {})
                for field, value in effects.items():
                    current = getattr(self, field)
                    setattr(self, field, max(0, current + value))

        # -------------------------
        # ASSIGN JOB (ONLY ON CREATE)
        # -------------------------
        if not self.pk:
            assign_job_by_traits(self)
        
        super().save(*args, **kwargs)

    @property
    def has_family(self):
        return self.children_from_mother.exists() or self.children_from_father.exists()
    
    def generate_personality_label(self):
        if not self.personality_traits:
            return "Neutral"
        return random.choice(self.personality_traits)
    
    def develop_personality(self):
        pass

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.generate_personality_label()})"