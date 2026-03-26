from django.db import models
import random


class Npc(models.Model):
    SEX_CHOICES = [('M','Male'),('F','Female')]

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
    age = models.IntegerField()
    personality = models.CharField(max_length=55)  # either good or bad trait

    def save(self, *args, **kwargs):
        if not self.age:
            self.age = random.randint(18, 60)
        if not self.sex:
            self.sex = random.choice(['M', 'F'])
        if self.sex == 'M':
            self.first_name = random.choice(self.MALE_FIRST_NAMES)
        else:
            self.first_name = random.choice(self.FEMALE_FIRST_NAMES)
        self.last_name = random.choice(self.LAST_NAMES)

        # Pick a personality: choose an index, then pick good or bad
        idx = random.randint(0, len(self.PERSONALITY_GOOD)-1)
        self.personality = random.choice([self.PERSONALITY_GOOD[idx], self.PERSONALITY_BAD[idx]])

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.personality})"