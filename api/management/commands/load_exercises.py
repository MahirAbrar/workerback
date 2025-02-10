from django.core.management.base import BaseCommand
from api.models import ExerciseList

class Command(BaseCommand):
    help = 'Load predefined exercises into the database'

    def handle(self, *args, **kwargs):
      exercises = [
          {
              "name": "Incline Dumbbell Press",
              "description": "A dumbbell press performed on an incline bench to target the upper portion of the chest.",
              "primary_muscle": "Upper Chest",
              "secondary_muscle": "Front Delts",
              "tertiary_muscle": "Long Head of Triceps",
              "exercise_type": "Dumbbell Exercises"
          },
          {
              "name": "Flat Barbell Bench Press",
              "description": "A classic barbell exercise that targets the middle part of the chest.",
              "primary_muscle": "Middle Chest",
              "secondary_muscle": "Lateral Head of Triceps",
              "tertiary_muscle": "Front Delts",
              "exercise_type": "Barbell Exercises"
          },
          {
              "name": "Decline Machine Press",
              "description": "A machine-based press performed on a decline bench to focus on the lower chest.",
              "primary_muscle": "Lower Chest",
              "secondary_muscle": "Medial Head of Triceps",
              "tertiary_muscle": "Front Delts",
              "exercise_type": "Machine-Based Workouts"
          },
          {
              "name": "Push-Ups",
              "description": "A bodyweight exercise that targets the entire chest, with emphasis on the middle chest.",
              "primary_muscle": "Middle Chest",
              "secondary_muscle": "Lateral Head of Triceps",
              "tertiary_muscle": "Front Delts",
              "exercise_type": "Bodyweight Training"
          },
          {
              "name": "Chest Fly (Dumbbell)",
              "description": "A dumbbell fly movement to isolate and stretch the chest muscles.",
              "primary_muscle": "Middle Chest",
              "secondary_muscle": "Front Delts",
              "tertiary_muscle": "Serratus Anterior",
              "exercise_type": "Dumbbell Exercises"
          },
          {
              "name": "Pull-Ups",
              "description": "A bodyweight exercise that targets the lats and other back muscles.",
              "primary_muscle": "Lats",
              "secondary_muscle": "Short Head of Biceps",
              "tertiary_muscle": "Rhomboids",
              "exercise_type": "Bodyweight Training"
          },
          {
              "name": "Bent-Over Barbell Row",
              "description": "A barbell row performed in a bent-over position to target the upper and middle back.",
              "primary_muscle": "Lats",
              "secondary_muscle": "Rhomboids",
              "tertiary_muscle": "Rear Delts",
              "exercise_type": "Barbell Exercises"
          },
          {
              "name": "Lat Pulldown (Machine)",
              "description": "A machine-based exercise where you pull a bar down to target the lats.",
              "primary_muscle": "Lats",
              "secondary_muscle": "Short Head of Biceps",
              "tertiary_muscle": "Rear Delts",
              "exercise_type": "Machine-Based Workouts"
          },
          {
              "name": "Seated Cable Row",
              "description": "A cable-based rowing exercise to target the middle back and lats.",
              "primary_muscle": "Lats",
              "secondary_muscle": "Rhomboids",
              "tertiary_muscle": "Rear Delts",
              "exercise_type": "Machine-Based Workouts"
          },
          {
              "name": "Deadlift (Barbell)",
              "description": "A compound barbell exercise that targets the entire posterior chain, including the back.",
              "primary_muscle": "Erector Spinae",
              "secondary_muscle": "Lats",
              "tertiary_muscle": "Glutes",
              "exercise_type": "Barbell Exercises"
          },
          {
              "name": "Face Pulls (Cable)",
              "description": "A cable-based exercise that targets the rear delts and upper back.",
              "primary_muscle": "Rear Delts",
              "secondary_muscle": "Traps",
              "tertiary_muscle": "Rhomboids",
              "exercise_type": "Machine-Based Workouts"
          },
          {
              "name": "Shrugs (Dumbbell)",
              "description": "A dumbbell exercise to target the traps by lifting the shoulders.",
              "primary_muscle": "Traps",
              "secondary_muscle": "Rhomboids",
              "tertiary_muscle": "Rear Delts",
              "exercise_type": "Dumbbell Exercises"
          },
          {
              "name": "Reverse Fly (Dumbbell)",
              "description": "A dumbbell exercise to target the rear delts and upper back.",
              "primary_muscle": "Rear Delts",
              "secondary_muscle": "Rhomboids",
              "tertiary_muscle": "Traps",
              "exercise_type": "Dumbbell Exercises"
          }
      ]

      for exercise_data in exercises:
          ExerciseList.objects.get_or_create(
              name=exercise_data['name'],
              defaults=exercise_data
          )
          self.stdout.write(f"Added exercise: {exercise_data['name']}") 