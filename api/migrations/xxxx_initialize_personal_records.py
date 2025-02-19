from django.db import migrations

def initialize_personal_records(apps, schema_editor):
    User = apps.get_model('api', 'User')
    for user in User.objects.all():
        if user.personal_records is None:
            user.personal_records = {}
            user.save()

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0003_exerciselist_exercise_type_and_more'),  # Replace with your previous migration
    ]

    operations = [
        migrations.RunPython(initialize_personal_records),
    ] 