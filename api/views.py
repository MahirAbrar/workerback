from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView as BaseRegisterView
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.views import LoginView as BaseLoginView
from .serializers import LoginSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import ExerciseList
from .serializers import ExerciseListSerializer
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.utils import timezone
from .serializers import WorkoutSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import schema

# Create your views here.

# Will accept both username, email, password1 and password2
# Will also accept username, email, password and confirm_password
class RegisterView(BaseRegisterView):
    def create(self, request, *args, **kwargs):
        # Rename the password fields in the request data
        data = request.data.copy()
        if 'password' in data:
            data['password1'] = data.pop('password')
        if 'confirm_password' in data:
            data['password2'] = data.pop('confirm_password')
        request._full_data = data
        return super().create(request, *args, **kwargs)

class LoginView(BaseLoginView):
    serializer_class = LoginSerializer

# Custom permission to check if user is admin
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow GET requests for authenticated users
        if request.method in ['GET']:
            return request.user and request.user.is_authenticated
        # Allow POST, PUT, DELETE only for admin users
        return request.user and request.user.is_authenticated and request.user.is_staff

class ExerciseListView(generics.ListCreateAPIView):
    queryset = ExerciseList.objects.all()
    serializer_class = ExerciseListSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        # Add any additional logic before saving
        serializer.save()

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class WorkoutView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        return self.request.user.workouts or []

    def perform_create(self, serializer):
        workout_data = {
            'id': len(self.request.user.workouts or []) + 1,
            'name': serializer.validated_data['name'],
            'description': serializer.validated_data.get('description', ''),
            'created_at': timezone.now().isoformat(),
            'exercises': [{
                'exercise_id': exercise['exercise'].id,
                'name': exercise['exercise'].name,
                'set_number': exercise['set_number'],
                'reps': exercise.get('reps'),
                'weight': exercise.get('weight'),
                'duration_minutes': exercise.get('duration_minutes'),
                'distance_meters': exercise.get('distance_meters')
            } for exercise in serializer.validated_data['exercises']]
        }
        
        if self.request.user.workouts is None:
            self.request.user.workouts = []
        self.request.user.workouts.append(workout_data)
        self.request.user.save()
        return workout_data
