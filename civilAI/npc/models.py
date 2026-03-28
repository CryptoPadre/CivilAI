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
    created_at = models.DateTimeField(default=timezone.now)
    initial_age = models.IntegerField(default=0)  
    fertility = models.CharField(max_length=6, choices=FERTILITY_RATE)
    sexual_orientation = models.CharField(
        max_length=10,
        choices=ORIENTATION_CHOICES,
        default='hetero'
    )
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

        if not self.pk:  
            self.initial_age = random.randint(10, 60)
            self.age = self.initial_age

        if self.created_at:
            delta = timezone.now() - self.created_at
            self.age = self.initial_age + int(delta.total_seconds() // 60)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.personality})"