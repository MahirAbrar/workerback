# Django imports
from django.shortcuts import render
from django.utils import timezone
from django.http import Http404

# Rest Framework imports
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

# Third party imports
from dj_rest_auth.registration.views import RegisterView as BaseRegisterView
from dj_rest_auth.views import LoginView as BaseLoginView

# Local imports
from .models import ExerciseList
from .serializers import (
    LoginSerializer, UserSerializer, ExerciseListSerializer,
    TemplateSerializer, WorkoutSerializer, CustomExerciseSerializer
)

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

class TemplateListPermission(BasePermission):
    """
    Custom permission for template list endpoint:
    - Allow GET and POST only
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Only allow GET and POST for template list
        if view.template_id is None:
            return request.method in ['GET', 'POST']
        return False

class TemplateDetailPermission(BasePermission):
    """
    Custom permission for template detail endpoint:
    - Allow GET, PUT, DELETE only
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Only allow GET, PUT, DELETE for template detail
        if view.template_id is not None:
            return request.method in ['GET', 'PUT', 'DELETE']
        return False

class TemplateView(APIView):
    def get_permissions(self):
        """
        Different permissions for list and detail endpoints
        """
        self.template_id = self.kwargs.get('template_id')
        if self.template_id is None:
            return [TemplateListPermission()]
        return [TemplateDetailPermission()]
    
    def get(self, request, template_id=None):
        """Get all templates or a specific template for the user"""
        if template_id is not None:
            templates = request.user.templates or []
            template = next((t for t in templates if t["id"] == template_id), None)
            if template is None:
                return Response({"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(template)
        return Response(request.user.templates or [])

    def post(self, request, template_id=None):
        """Create a new template"""
        if template_id is not None:
            return Response(
                {"error": "POST not allowed on individual template"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
            
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            template_data = {
                'id': len(request.user.templates or []) + 1,
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
            
            if request.user.templates is None:
                request.user.templates = []
            request.user.templates.append(template_data)
            request.user.save()
            return Response(template_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, template_id):
        """Update a template"""
        templates = request.user.templates or []
        template_index = next((index for (index, d) in enumerate(templates) 
                             if d["id"] == template_id), None)
        
        if template_index is None:
            return Response({"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            template_data = {
                'id': template_id,
                'name': serializer.validated_data['name'],
                'description': serializer.validated_data.get('description', ''),
                'updated_at': timezone.now().isoformat(),
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
            
            templates[template_index] = template_data
            request.user.templates = templates
            request.user.save()
            return Response(template_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, template_id):
        """Delete a template"""
        templates = request.user.templates or []
        template_index = next((index for (index, d) in enumerate(templates) 
                             if d["id"] == template_id), None)
        
        if template_index is None:
            return Response({"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND)

        templates.pop(template_index)
        request.user.templates = templates
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
                'distance_meters': exercise.get('distance_meters'),
                'volume': exercise.get('volume', 0),
                'one_rm': exercise.get('one_rm', 0),
                'total_volume': exercise.get('total_volume', 0),
                'total_duration': exercise.get('total_duration', 0)
            } for exercise in serializer.validated_data['exercises']]
        }
        
        if self.request.user.workouts is None:
            self.request.user.workouts = []

        # PERSONAL RECORDS
        # Update PERSONAL RECORDS for each exercise
        for exercise in serializer.validated_data['exercises']:
            self.request.user.update_personal_records(
                exercise['exercise'].id,
                {
                    'volume': exercise.get('volume', 0),
                    'one_rm': exercise.get('one_rm', 0),
                    'total_volume': exercise.get('total_volume', 0),
                    'total_duration': exercise.get('total_duration', 0),
                    'reps': exercise.get('reps', 0),
                    'weight': exercise.get('weight', 0),
                    'duration_minutes': exercise.get('duration_minutes', 0)
                }
            )
        
        self.request.user.workouts.append(workout_data)
        self.request.user.save()
        return workout_data

class CustomExerciseView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomExerciseSerializer

    def get_queryset(self):
        return self.request.user.custom_exercises or []

    def perform_create(self, serializer):
        exercise_data = {
            'id': len(self.request.user.custom_exercises or []) + 1,
            **serializer.validated_data,
            'created_at': timezone.now().isoformat(),
            'updated_at': timezone.now().isoformat()
        }
        
        if self.request.user.custom_exercises is None:
            self.request.user.custom_exercises = []
        
        self.request.user.custom_exercises.append(exercise_data)
        self.request.user.save()
        return exercise_data

class CustomExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomExerciseSerializer
    lookup_field = 'exercise_id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if 'exercise_id' in self.kwargs:
            context['exercise_id'] = int(self.kwargs['exercise_id'])
        return context

    def get_object(self):
        exercise_id = int(self.kwargs['exercise_id'])
        exercises = self.request.user.custom_exercises or []
        exercise = next((ex for ex in exercises if ex['id'] == exercise_id), None)
        if exercise is None:
            raise Http404("Exercise not found")
        return exercise

    def perform_update(self, serializer):
        exercise_id = int(self.kwargs['exercise_id'])
        exercises = self.request.user.custom_exercises or []
        exercise_index = next((index for (index, ex) in enumerate(exercises) 
                             if ex['id'] == exercise_id), None)
        
        if exercise_index is None:
            raise Http404("Exercise not found")

        # Keep the existing created_at and id, update the rest
        exercises[exercise_index].update({
            **serializer.validated_data,
            'updated_at': timezone.now().isoformat()
        })
        
        self.request.user.custom_exercises = exercises
        self.request.user.save()

    def perform_destroy(self, instance):
        exercise_id = int(self.kwargs['exercise_id'])
        exercises = self.request.user.custom_exercises or []
        exercise_index = next((index for (index, ex) in enumerate(exercises) 
                             if ex['id'] == exercise_id), None)
        
        if exercise_index is None:
            raise Http404("Exercise not found")

        exercises.pop(exercise_index)
        self.request.user.custom_exercises = exercises
        self.request.user.save()

# View for handling personal records endpoints
# This function is accessible in URLs.py API
class PersonalRecordsView(APIView):
    # Without this line, any user (even unauthenticated) could access personal records
    permission_classes = [IsAuthenticated]
    
    # Without this method, the view wouldn't handle GET requests
    def get(self, request):
        # Without this line, we wouldn't have access to the exercise names and types. Imported from models.py
        exercises = ExerciseList.objects.all()
        
        # Without this initialization, we'd get an error trying to add to records
        records = {}

        # Checks if the user has any personal records for each exercise
        for exercise in exercises:
            # Why convert to string?
            # Because JSON only accepts string keys and exercise.id is an integer
            str_exercise_id = str(exercise.id)

            # Without this check, we'd try to access non-existent records
            if str_exercise_id in request.user.personal_records:
                # Without these fields, the frontend wouldn't know which exercise the records belong to
                # exercise.name and exercise.exercise_type makes it easier to identify the exercise
                records[str_exercise_id] = {
                    'exercise_name': exercise.name,
                    'exercise_type': exercise.exercise_type,
                    # Showcase the actual PR data
                    **request.user.personal_records[str_exercise_id]
                }
        
        # Without Response(), Django wouldn't properly format the JSON response
        # because Response() is a function that returns a object 
        return Response(records)
