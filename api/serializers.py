from rest_framework import serializers
from .models import User, ExerciseList
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer as BaseLoginSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'custom_exercises', 
                 'workouts', 'templates', 'created_at')
        read_only_fields = ('id', 'created_at')


# TODO: Be able to verify emails!
class RegisterSerializer(RegisterSerializer):
    # Override the password fields to change their labels/help_text
    # Note, JSON data will be sent as password1 and password2
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        label='Password',
        help_text='Your password',
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label='Confirm Password',
        help_text='Enter the same password as before',
        style={'input_type': 'password'}
    )

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        } 

class LoginSerializer(BaseLoginSerializer):
    username = None  # Remove username field
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        attrs['username'] = attrs.get('email')  # Use email as username
        return super().validate(attrs) 

class ExerciseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseList
        fields = ('id', 'name', 'description', 'primary_muscle', 
                 'secondary_muscle', 'tertiary_muscle', 'exercise_type') 

class WorkoutExerciseSerializer(serializers.Serializer):
    exercise_id = serializers.IntegerField()
    reps = serializers.IntegerField(required=False, allow_null=True)
    weight = serializers.FloatField(required=False, allow_null=True)
    duration_minutes = serializers.IntegerField(required=False, allow_null=True)
    distance_meters = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, data):
        try:
            exercise = ExerciseList.objects.get(id=data['exercise_id'])
        except ExerciseList.DoesNotExist:
            raise serializers.ValidationError("Exercise not found")

        # TODO: Deal with type in the frontend
        # Validate based on exercise type
        exercise_type = exercise.exercise_type
        if exercise_type in ['Dumbbell Exercises', 'Barbell Exercises', 'Machine-Based Workouts', 
                           'Kettlebell Workouts', 'Resistance Band Training', 'Cable Exercises']:
            if not data.get('reps'):
                raise serializers.ValidationError("Reps are required for this exercise type")
            if not data.get('weight'):
                raise serializers.ValidationError("Weight is required for this exercise type")
        elif exercise_type == 'Cardiovascular Exercise':
            if not data.get('duration_minutes'):
                raise serializers.ValidationError("Duration is required for cardiovascular exercises")
        elif exercise_type in ['Yoga and Flexibility Workouts', 'Core Stability Training', 'Agility Drills']:
            if not data.get('duration_minutes'):
                raise serializers.ValidationError("Duration is required for this exercise type")

        data['exercise'] = exercise
        return data

class WorkoutSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    exercises = WorkoutExerciseSerializer(many=True)

    def validate_exercises(self, exercises):
        # Group exercises by exercise_id and add set numbers
        exercise_sets = {}
        processed_exercises = []

        for exercise in exercises:
            exercise_id = exercise['exercise_id']
            if exercise_id not in exercise_sets:
                exercise_sets[exercise_id] = 1
            else:
                exercise_sets[exercise_id] += 1
            
            exercise['set_number'] = exercise_sets[exercise_id]
            processed_exercises.append(exercise)

        return processed_exercises 