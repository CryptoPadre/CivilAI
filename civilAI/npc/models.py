from django.db import models
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
    "Hardworking", "Attentive", "Grateful", "Adventurous", "Flexible", "Persevering", "Patient", "Tolerant", "Protective", "Devoted",
    "Innovative", "Balanced", "Disciplined", "Practical", "Charitable", "Alert", "Caring", "Friendly", "Generous", "Honorable",
    "Nurturing", "Observant"
    ]

    PERSONALITY_BAD = [
        "Deceitful", "Cruel", "Disloyal", "Cowardly", "Impatient", "Selfish", "Arrogant", "Pessimistic", "Mean", "Irresponsible",
        "Jealous", "Greedy", "Lazy", "Rude", "Vindictive", "Stubborn", "Dishonest", "Manipulative", "Impolite", "Narrow-minded",
        "Cowardly", "Inconsiderate", "Spiteful", "Gossipy", "Short-tempered", "Unreliable", "Overcritical", "Unforgiving", "Boastful", "Reckless",
        "Overbearing", "Impulsive", "Indecisive", "Hasty", "Self-centered", "Untrustworthy", "Needy", "Cynical", "Lazy", "Resentful",
        "Careless", "Irresponsible", "Obnoxious", "Greedy", "Controlling", "Sullen", "Insensitive", "Harsh", "Pompous", "Loud"
    ]

    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField(default=0) 
    personality = models.CharField(max_length=55) 
    born_at = models.DateTimeField(default=timezone.now)
    initial_age = models.IntegerField(null=True, blank=True) 
    is_alive = models.BooleanField(default=True)
    died_at = models.DateTimeField(null=True, blank=True)

    is_adventurous = models.BooleanField(default=False)

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

    fitness_level = models.IntegerField(default=0)
    intelligence_level = models.IntegerField(default=0)
    aggression_level = models.IntegerField(default=0)
    happiness_level = models.IntegerField(default=0)
    stress_level = models.IntegerField(default=0)
    charisma_level = models.IntegerField(default=0)
    empathy_level = models.IntegerField(default=0)
    morality_level = models.IntegerField(default=0)

    health_level = models.IntegerField(default=100)
    energy_level = models.IntegerField(default=100)
    introversion_level = models.IntegerField(default=50)

    latitude = models.FloatField(default=49.2992)
    longitude = models.FloatField(default=19.9496)

    def save(self, *args, **kwargs):
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

        # Personality
        if not self.personality:
            good_choice = random.choice(self.PERSONALITY_GOOD)
            bad_choice = random.choice(self.PERSONALITY_BAD)
            self.personality = random.choice([good_choice, bad_choice])
            
        # Initial age
        if not self.pk and self.initial_age is None:
            self.initial_age = random.randint(10, 60)
            self.age = self.initial_age

        # Age update (based on time)
        if self.born_at and self.initial_age is not None:
            delta = timezone.now() - self.born_at
            self.age = self.initial_age + int(delta.total_seconds() // 60)

        # Fitness default
        if self.fitness_level == 0:
            self.fitness_level = random.randint(1, 10)

        # Introversion default
        if self.introversion_level == 50:
            self.introversion_level = random.randint(0, 100)

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

        super().save(*args, **kwargs)

    @property
    def has_family(self):
        return self.children_from_mother.exists() or self.children_from_father.exists()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.personality})"