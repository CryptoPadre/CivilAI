from django.db import models
import random
from django.utils import timezone


class Npc(models.Model):
    SEX_CHOICES = [('M','Male'),('F','Female')]
    
    FERTILITY_RATE = [('H',"High"), ('N',"Normal"), ('L',"Low")]
    
    ORIENTATION_CHOICES = [
        ('hetero', 'Heterosexual'),
        ('gay', 'Gay'),
        ('bi', 'Bisexual'),
        ('other', 'Other'),
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
        "Tadeusz", "Emil", "Anton", "Andrei", "Sergei"
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
        "Inna", "Raisa", "Zofia", "Clara", "Lana"
    ]

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
        "Varga", "Farkas", "Balázs", "Jelen", "Mikuláš"
    ]

    PERSONALITY_GOOD = [
        "Honest", "Compassionate", "Loyal", "Brave", "Patient",
        "Generous", "Humble", "Optimistic", "Kind", "Responsible"
    ]

    PERSONALITY_BAD = [
        "Deceitful", "Cruel", "Disloyal", "Cowardly", "Impatient",
        "Selfish", "Arrogant", "Pessimistic", "Mean", "Irresponsible"
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
    fertility = models.CharField(max_length=6, choices=FERTILITY_RATE)
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
    introversion_level = models.IntegerField(default=0)
    latitude = models.FloatField(default=49.2992)
    longitude = models.FloatField(default=19.9496)

    def save(self, *args, **kwargs):
        # assign random initial values if missing
        if not self.sex:
            self.sex = random.choice(['M', 'F'])

        if not self.first_name:
            self.first_name = random.choice(
                self.MALE_FIRST_NAMES if self.sex == 'M' else self.FEMALE_FIRST_NAMES
            )

        if not self.last_name:
            self.last_name = random.choice(self.LAST_NAMES)

        if not self.personality:
            idx = random.randint(0, len(self.PERSONALITY_GOOD) - 1)
            self.personality = random.choice([
                self.PERSONALITY_GOOD[idx],
                self.PERSONALITY_BAD[idx]
            ])

        if not self.pk and self.initial_age is None:
            self.initial_age = random.randint(10, 60)
            self.age = self.initial_age

        if self.fitness_level is None:
            self.fitness_level = random.randint(0, 11)
        
        if self.born_at:
            delta = timezone.now() - self.born_at
            self.age = self.initial_age + int(delta.total_seconds() // 60)
        
        if self.mother and self.father and self.mother == self.father:
            self.father = None
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.personality})"