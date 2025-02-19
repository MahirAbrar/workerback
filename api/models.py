from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    google_id = models.CharField(max_length=255, null=True, blank=True)
    custom_exercises = models.JSONField(default=list, blank=True)
    workouts = models.JSONField(default=list, blank=True)
    templates = models.JSONField(default=list, blank=True)
    personal_records = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    # Make email the required field instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def update_personal_records(self, exercise_id, exercise_data):
        """
        Update personal records for a given exercise if any records are broken
        """
        if self.personal_records is None:
            self.personal_records = {}
            
        str_exercise_id = str(exercise_id)  # JSON keys must be strings
        current_records = self.personal_records.get(str_exercise_id, {
            'max_volume_total': 0,
            'max_volume_single_set': 0,
            'max_one_rm': 0,
            'max_duration_single_set': 0,
            'max_duration_total': 0,
            'max_reps_single_set': 0,
            'max_weight': 0,
        })

        # Update records if broken, handling None values
        total_volume = exercise_data.get('total_volume', 0) or 0
        single_volume = exercise_data.get('volume', 0) or 0
        one_rm = exercise_data.get('one_rm', 0) or 0
        duration = exercise_data.get('duration_minutes', 0) or 0
        reps = exercise_data.get('reps', 0) or 0
        weight = exercise_data.get('weight', 0) or 0

        if total_volume > current_records['max_volume_total']:
            current_records['max_volume_total'] = total_volume
            
        if single_volume > current_records['max_volume_single_set']:
            current_records['max_volume_single_set'] = single_volume
            
        if one_rm > current_records['max_one_rm']:
            current_records['max_one_rm'] = one_rm
            
        if duration > current_records['max_duration_single_set']:
            current_records['max_duration_single_set'] = duration
            
        if reps > current_records['max_reps_single_set']:
            current_records['max_reps_single_set'] = reps
            
        if weight > current_records['max_weight']:
            current_records['max_weight'] = weight

        # Update the records in the dictionary
        self.personal_records[str_exercise_id] = current_records

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

EXERCISE_TYPE_CHOICES = ["Dumbbell Exercises", "Barbell Exercises", "Machine-Based Workouts", "Bodyweight Training", "Kettlebell Workouts", "Resistance Band Training", "Cable Exercises", "Cardiovascular Exercise", "Yoga and Flexibility Workouts"]


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
