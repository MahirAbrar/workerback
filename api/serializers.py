from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'custom_exercises', 
                 'workouts', 'templates', 'created_at')
        read_only_fields = ('id', 'created_at') 