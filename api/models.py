from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    google_id = models.CharField(max_length=255, null=True, blank=True)
    custom_exercises = models.JSONField(default=list, blank=True)
    workouts = models.JSONField(default=list, blank=True)
    templates = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    # Make email the required field instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

MUSCLE_CHOICES = [
    ('Upper Chest', 'Upper Chest'),
    ('Middle Chest', 'Middle Chest'),
    ('Lower Chest', 'Lower Chest'),
    ('Front Delts', 'Front Delts'),
    ('Side Delts', 'Side Delts'),
    ('Rear Delts', 'Rear Delts'),
    ('Traps', 'Traps'),
    ('Lats', 'Lats'),
    ('Rhomboids', 'Rhomboids'),
    ('Erector Spinae', 'Erector Spinae'),
    ('Long Head of Triceps', 'Long Head of Triceps'),
    ('Lateral Head of Triceps', 'Lateral Head of Triceps'),
    ('Medial Head of Triceps', 'Medial Head of Triceps'),
    ('Long Head of Biceps', 'Long Head of Biceps'),
    ('Short Head of Biceps', 'Short Head of Biceps'),
    ('Forearms', 'Forearms'),
    ('Abs', 'Abs'),
    ('Obliques', 'Obliques'),
    ('Hamstrings', 'Hamstrings'),
    ('Quadriceps', 'Quadriceps'),
    ('Calves', 'Calves'),
    ('Glutes', 'Glutes'),
    ('Hip Flexors', 'Hip Flexors'),
    ('Adductors', 'Adductors'),
    ('Abductors', 'Abductors'),
    ('Serratus Anterior', 'Serratus Anterior'),
    ('Transverse Abdominis', 'Transverse Abdominis'),
]

EXERCISE_TYPE_CHOICES = ["Dumbbell Exercises", "Barbell Exercises", "Machine-Based Workouts", "Bodyweight Training", "Kettlebell Workouts", "Resistance Band Training", "Cable Exercises", "Cardiovascular Exercise", "High-Intensity Interval Training", "Functional Movement Training", "Plyometric Exercises", "Yoga and Flexibility Workouts", "Core Stability Training", "Endurance Training", "Agility Drills", "Balance and Stability Exercises", "Powerlifting", "Olympic Lifting", "Calisthenics", "Aquatic Fitness", "Outdoor Adventure Fitness"]


class ExerciseList(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    primary_muscle = models.CharField(max_length=50, choices=MUSCLE_CHOICES)
    secondary_muscle = models.CharField(max_length=50, choices=MUSCLE_CHOICES, blank=True, null=True)
    tertiary_muscle = models.CharField(max_length=50, choices=MUSCLE_CHOICES, blank=True, null=True)
    exercise_type = models.CharField(
        max_length=100, 
        choices=[(t, t) for t in EXERCISE_TYPE_CHOICES],
        default='Dumbbell Exercises'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'

    def __str__(self):
        return self.name
