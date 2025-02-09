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
