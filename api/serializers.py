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