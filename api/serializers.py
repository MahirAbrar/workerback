from rest_framework import serializers
from .models import User, ExerciseList, MUSCLE_CHOICES, EXERCISE_TYPE_CHOICES
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
    username = serializers.EmailField(required=True)
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
    exercise_id = serializers.IntegerField(
        help_text="ID of the exercise from the exercise list. Go to http://127.0.0.1:8000/api/exercises/ to get the list"
    )
    reps = serializers.IntegerField(
        required=False, 
        allow_null=True,
        help_text="Number of repetitions",
        min_value=0
    )
    weight = serializers.FloatField(
        required=False, 
        allow_null=True,
        help_text="Weight in kg",
        min_value=0
    )
    duration_minutes = serializers.FloatField(
        required=False, 
        allow_null=True,
        help_text="Duration in minutes (cardio/yoga exercises)",
        min_value=0
    )
    distance_meters = serializers.FloatField(
        required=False, 
        allow_null=True,
        help_text="Distance in meters (optional for cardio exercises)",
        min_value=0
    )
    volume = serializers.FloatField(read_only=True)
    one_rm = serializers.FloatField(read_only=True)

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
            
            # Calculate volume and one_rm for weight-based exercises
            if data.get('weight'):
                # Volume = reps × weight
                data['volume'] = float(data['reps']) * float(data['weight'])
                
                # Epley Formula for 1RM
                # 1RM = weight × (36 / (37 - reps))
                data['one_rm'] = float(data['weight']) * (36 / (37 - float(data['reps'])))
            else:
                data['volume'] = 0
                data['one_rm'] = 0

        elif exercise_type in ['Cardiovascular Exercise', 'Yoga and Flexibility Workouts']:
            if not data.get('duration_minutes'):
                raise serializers.ValidationError("Duration is required for this exercise type")
            data['volume'] = 0
            data['one_rm'] = 0
        elif exercise_type == 'Bodyweight Training':
            if not data.get('reps'):
                raise serializers.ValidationError("Reps are required for bodyweight exercises")
            # For bodyweight, volume is just the number of reps
            data['volume'] = float(data['reps'])
            data['one_rm'] = 0

        data['exercise'] = exercise
        return data

class WorkoutSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=100,
        help_text="Name of your workout"
    )
    description = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Optional description of your workout"
    )
    exercises = WorkoutExerciseSerializer(
        many=True,
        help_text="""List of exercises in your workout. Example format:
        [
            {
                "exercise_id": 1,
                "reps": 12,
                "weight": 20
            },
            {
                "exercise_id": 2,
                "duration_minutes": 10
            }
        ]"""
    )
    time_completed = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="Time of the workout (format: YYYY-MM-DDThh:mm:ssZ, e.g., 2024-03-20T14:30:00Z)"
    )

    workout_duration = serializers.DurationField(
        required=False,
        allow_null=True,
        help_text="Duration of the workout (format: PT1H20M30S, e.g., PT1H20M30S) which means 1 hour 20 minutes and 30 seconds"
    )

    workout_notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Notes about the workout"
    )
    

    def validate_exercises(self, exercises):
        exercise_sets = {}
        exercise_volumes = {}
        exercise_durations = {}
        processed_exercises = []

        for exercise in exercises:
            exercise_id = exercise['exercise_id']
            
            # Initialize tracking for new exercise
            if exercise_id not in exercise_sets:
                exercise_sets[exercise_id] = 1
                exercise_volumes[exercise_id] = 0
                exercise_durations[exercise_id] = 0
            else:
                exercise_sets[exercise_id] += 1

            # Add set number to exercise
            exercise['set_number'] = exercise_sets[exercise_id]
            
            # Add current set's volume to total if it exists
            if 'volume' in exercise and exercise['volume'] is not None:
                exercise_volumes[exercise_id] += exercise['volume']
            
            # Add current set's duration to total if it exists
            if 'duration_minutes' in exercise and exercise['duration_minutes'] is not None:
                exercise_durations[exercise_id] += exercise['duration_minutes']
            
            # Add total volume and duration for this exercise to each set
            exercise['total_volume'] = exercise_volumes[exercise_id]
            exercise['total_duration'] = exercise_durations[exercise_id]
            
            # Update personal records only for completed workouts
            request = self.context.get('request')
            if request and request.user:
                request.user.update_personal_records(exercise_id, exercise)
                request.user.save()
            
            processed_exercises.append(exercise)

        return processed_exercises

class TemplateExerciseSerializer(serializers.Serializer):
    exercise_id = serializers.IntegerField(
        help_text="ID of the exercise from the exercise list"
    )
    reps = serializers.IntegerField(
        required=False, 
        allow_null=True,
        help_text="Number of repetitions",
        min_value=0
    )
    weight = serializers.FloatField(
        required=False, 
        allow_null=True,
        help_text="Weight in kg",
        min_value=0
    )
    duration_minutes = serializers.FloatField(
        required=False, 
        allow_null=True,
        help_text="Duration in minutes (cardio/yoga exercises)",
        min_value=0
    )
    distance_meters = serializers.FloatField(
        required=False, 
        allow_null=True,
        help_text="Distance in meters (optional for cardio exercises)",
        min_value=0
    )
    #for 1 set
    volume = serializers.FloatField(read_only=True) #Read only means that the field is not required
    one_rm = serializers.FloatField(read_only=True) #Calculated automatically

    def validate(self, data):
        try:
            exercise = ExerciseList.objects.get(id=data['exercise_id'])
        except ExerciseList.DoesNotExist:
            raise serializers.ValidationError("Exercise not found")

        exercise_type = exercise.exercise_type
        if exercise_type in ['Dumbbell Exercises', 'Barbell Exercises', 'Machine-Based Workouts', 
                           'Kettlebell Workouts', 'Resistance Band Training', 'Cable Exercises']:
            if not data.get('reps'):
                raise serializers.ValidationError("Reps are required for this exercise type")
            
            # Calculate volume and one_rm for weight-based exercises
            if data.get('weight'):
                # Volume = reps × weight
                data['volume'] = float(data['reps']) * float(data['weight'])
                
                # TODO: Epley Formula for 1RM
                # 1RM = weight × (36 / (37 - reps))
                data['one_rm'] = float(data['weight']) * (36 / (37 - float(data['reps'])))
            else:
                data['volume'] = 0
                data['one_rm'] = 0

        elif exercise_type in ['Cardiovascular Exercise', 'Yoga and Flexibility Workouts']:
            if not data.get('duration_minutes'):
                raise serializers.ValidationError("Duration is required for this exercise type")
            data['volume'] = 0
            data['one_rm'] = 0
        elif exercise_type == 'Bodyweight Training':
            if not data.get('reps'):
                raise serializers.ValidationError("Reps are required for bodyweight exercises")
            # For bodyweight, volume is just the number of reps
            data['volume'] = float(data['reps'])
            data['one_rm'] = 0

        data['exercise'] = exercise
        return data

class TemplateSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=100,
        help_text="Name of your template"
    )
    description = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Optional description of your template"
    )
    exercises = TemplateExerciseSerializer(
        many=True,
        help_text="List of exercises in your template"
    )

    def validate_exercises(self, exercises):
        exercise_sets = {}  # Track sets per exercise
        exercise_volumes = {}  # Track total volume per exercise
        exercise_durations = {}  # Track total duration per exercise
        processed_exercises = []

        for exercise in exercises:
            exercise_id = exercise['exercise_id']
            
            # Initialize tracking for new exercise
            if exercise_id not in exercise_sets:
                exercise_sets[exercise_id] = 1
                exercise_volumes[exercise_id] = 0
                exercise_durations[exercise_id] = 0
            else:
                exercise_sets[exercise_id] += 1

            # Add set number to exercise
            exercise['set_number'] = exercise_sets[exercise_id]
            
            # Add current set's volume to total
            if 'volume' in exercise:
                exercise_volumes[exercise_id] += exercise['volume']
            
            # Add current set's duration to total
            if 'duration_minutes' in exercise:
                exercise_durations[exercise_id] += exercise['duration_minutes']
            
            # Add total volume and duration for this exercise to each set
            exercise['total_volume'] = exercise_volumes[exercise_id]
            exercise['total_duration'] = exercise_durations[exercise_id]
            
            processed_exercises.append(exercise)

        return processed_exercises
    
    
class CustomExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=100,
        help_text="Name of your custom exercise",
        style={'placeholder': 'Enter exercise name'}
    )
    description = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Description of your custom exercise",
        style={'placeholder': 'Enter exercise description'}
    )
    primary_muscle = serializers.ChoiceField(
        choices=MUSCLE_CHOICES,
        help_text="Primary muscle worked",
        style={'placeholder': 'Select primary muscle'}
    )
    secondary_muscle = serializers.ChoiceField(
        choices=MUSCLE_CHOICES,
        required=False,
        allow_null=True,
        help_text="Secondary muscle worked",
        style={'placeholder': 'Select secondary muscle'}
    )
    tertiary_muscle = serializers.ChoiceField(
        choices=MUSCLE_CHOICES,
        required=False,
        allow_null=True,
        help_text="Tertiary muscle worked",
        style={'placeholder': 'Select tertiary muscle'}
    )
    exercise_type = serializers.ChoiceField(
        choices=[(t, t) for t in EXERCISE_TYPE_CHOICES],
        help_text="Type of exercise",
        style={'placeholder': 'Select exercise type'}
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_name(self, value):
        """
        Check that the exercise name is unique for this user
        """
        request = self.context.get('request')
        exercise_id = self.context.get('exercise_id')  # This will now be available during PUT requests
        
        if request and request.user:
            existing_exercises = request.user.custom_exercises or []
            value = value.strip()
            
            # For new exercises (POST)
            if not exercise_id:
                if any(ex['name'].lower() == value.lower() for ex in existing_exercises):
                    raise serializers.ValidationError(
                        "You already have an exercise with this name"
                    )
            # For updates (PUT)
            else:
                if any(ex['name'].lower() == value.lower() and ex['id'] != exercise_id 
                      for ex in existing_exercises):
                    raise serializers.ValidationError(
                        "You already have an exercise with this name"
                    )
        return value

    def to_representation(self, instance):
        """
        Convert the exercise instance to a dictionary for response.
        """
        data = super().to_representation(instance)
        if isinstance(instance, dict):
            data['created_at'] = instance.get('created_at', '')
            data['updated_at'] = instance.get('updated_at', '')
        return data 