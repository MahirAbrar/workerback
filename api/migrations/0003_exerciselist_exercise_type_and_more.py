# Generated by Django 5.1.3 on 2025-02-10 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_exerciselist"),
    ]

    operations = [
        migrations.AddField(
            model_name="exerciselist",
            name="exercise_type",
            field=models.CharField(
                choices=[
                    ("Dumbbell Exercises", "Dumbbell Exercises"),
                    ("Barbell Exercises", "Barbell Exercises"),
                    ("Machine-Based Workouts", "Machine-Based Workouts"),
                    ("Bodyweight Training", "Bodyweight Training"),
                    ("Kettlebell Workouts", "Kettlebell Workouts"),
                    ("Resistance Band Training", "Resistance Band Training"),
                    ("Cardiovascular Exercise", "Cardiovascular Exercise"),
                    (
                        "High-Intensity Interval Training",
                        "High-Intensity Interval Training",
                    ),
                    ("Functional Movement Training", "Functional Movement Training"),
                    ("Plyometric Exercises", "Plyometric Exercises"),
                    ("Yoga and Flexibility Workouts", "Yoga and Flexibility Workouts"),
                    ("Core Stability Training", "Core Stability Training"),
                    ("Endurance Training", "Endurance Training"),
                    ("Agility Drills", "Agility Drills"),
                    (
                        "Balance and Stability Exercises",
                        "Balance and Stability Exercises",
                    ),
                    ("Powerlifting", "Powerlifting"),
                    ("Olympic Lifting", "Olympic Lifting"),
                    ("Calisthenics", "Calisthenics"),
                    ("Aquatic Fitness", "Aquatic Fitness"),
                    ("Outdoor Adventure Fitness", "Outdoor Adventure Fitness"),
                ],
                default="Dumbbell Exercises",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="exerciselist",
            name="primary_muscle",
            field=models.CharField(
                choices=[
                    ("Upper Chest", "Upper Chest"),
                    ("Middle Chest", "Middle Chest"),
                    ("Lower Chest", "Lower Chest"),
                    ("Front Delts", "Front Delts"),
                    ("Side Delts", "Side Delts"),
                    ("Rear Delts", "Rear Delts"),
                    ("Traps", "Traps"),
                    ("Lats", "Lats"),
                    ("Rhomboids", "Rhomboids"),
                    ("Erector Spinae", "Erector Spinae"),
                    ("Long Head of Triceps", "Long Head of Triceps"),
                    ("Lateral Head of Triceps", "Lateral Head of Triceps"),
                    ("Medial Head of Triceps", "Medial Head of Triceps"),
                    ("Long Head of Biceps", "Long Head of Biceps"),
                    ("Short Head of Biceps", "Short Head of Biceps"),
                    ("Forearms", "Forearms"),
                    ("Abs", "Abs"),
                    ("Obliques", "Obliques"),
                    ("Hamstrings", "Hamstrings"),
                    ("Quadriceps", "Quadriceps"),
                    ("Calves", "Calves"),
                    ("Glutes", "Glutes"),
                    ("Hip Flexors", "Hip Flexors"),
                    ("Adductors", "Adductors"),
                    ("Abductors", "Abductors"),
                    ("Serratus Anterior", "Serratus Anterior"),
                    ("Transverse Abdominis", "Transverse Abdominis"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="exerciselist",
            name="secondary_muscle",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Upper Chest", "Upper Chest"),
                    ("Middle Chest", "Middle Chest"),
                    ("Lower Chest", "Lower Chest"),
                    ("Front Delts", "Front Delts"),
                    ("Side Delts", "Side Delts"),
                    ("Rear Delts", "Rear Delts"),
                    ("Traps", "Traps"),
                    ("Lats", "Lats"),
                    ("Rhomboids", "Rhomboids"),
                    ("Erector Spinae", "Erector Spinae"),
                    ("Long Head of Triceps", "Long Head of Triceps"),
                    ("Lateral Head of Triceps", "Lateral Head of Triceps"),
                    ("Medial Head of Triceps", "Medial Head of Triceps"),
                    ("Long Head of Biceps", "Long Head of Biceps"),
                    ("Short Head of Biceps", "Short Head of Biceps"),
                    ("Forearms", "Forearms"),
                    ("Abs", "Abs"),
                    ("Obliques", "Obliques"),
                    ("Hamstrings", "Hamstrings"),
                    ("Quadriceps", "Quadriceps"),
                    ("Calves", "Calves"),
                    ("Glutes", "Glutes"),
                    ("Hip Flexors", "Hip Flexors"),
                    ("Adductors", "Adductors"),
                    ("Abductors", "Abductors"),
                    ("Serratus Anterior", "Serratus Anterior"),
                    ("Transverse Abdominis", "Transverse Abdominis"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="exerciselist",
            name="tertiary_muscle",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Upper Chest", "Upper Chest"),
                    ("Middle Chest", "Middle Chest"),
                    ("Lower Chest", "Lower Chest"),
                    ("Front Delts", "Front Delts"),
                    ("Side Delts", "Side Delts"),
                    ("Rear Delts", "Rear Delts"),
                    ("Traps", "Traps"),
                    ("Lats", "Lats"),
                    ("Rhomboids", "Rhomboids"),
                    ("Erector Spinae", "Erector Spinae"),
                    ("Long Head of Triceps", "Long Head of Triceps"),
                    ("Lateral Head of Triceps", "Lateral Head of Triceps"),
                    ("Medial Head of Triceps", "Medial Head of Triceps"),
                    ("Long Head of Biceps", "Long Head of Biceps"),
                    ("Short Head of Biceps", "Short Head of Biceps"),
                    ("Forearms", "Forearms"),
                    ("Abs", "Abs"),
                    ("Obliques", "Obliques"),
                    ("Hamstrings", "Hamstrings"),
                    ("Quadriceps", "Quadriceps"),
                    ("Calves", "Calves"),
                    ("Glutes", "Glutes"),
                    ("Hip Flexors", "Hip Flexors"),
                    ("Adductors", "Adductors"),
                    ("Abductors", "Abductors"),
                    ("Serratus Anterior", "Serratus Anterior"),
                    ("Transverse Abdominis", "Transverse Abdominis"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
