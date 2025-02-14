from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView as BaseRegisterView
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.views import LoginView as BaseLoginView
from .serializers import LoginSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from .models import ExerciseList
from .serializers import ExerciseListSerializer
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.utils import timezone
from .serializers import WorkoutSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import schema
from .serializers import TemplateSerializer
# from .serializers import CustomExerciseSerializer

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
                'distance_meters': exercise.get('distance_meters')
            } for exercise in serializer.validated_data['exercises']]
        }
        
        if self.request.user.workouts is None:
            self.request.user.workouts = []
        self.request.user.workouts.append(workout_data)
        self.request.user.save()
        return workout_data

# class CustomExerciseView(APIView):
#     permission_classes = [IsAuthenticated]
#     
#     def get(self, request, exercise_id=None):
#         """Get all custom exercises or a specific one"""
#         if exercise_id is not None:
#             exercises = request.user.custom_exercises or []
#             exercise = next((ex for ex in exercises if ex["id"] == exercise_id), None)
#             if exercise is None:
#                 return Response(
#                     {"error": "Exercise not found"}, 
#                     status=status.HTTP_404_NOT_FOUND
#                 )
#             serializer = CustomExerciseSerializer(exercise)
#             return Response(serializer.data)
#         
#         exercises = request.user.custom_exercises or []
#         serializer = CustomExerciseSerializer(exercises, many=True)
#         return Response(serializer.data)
# 
#     def post(self, request, exercise_id=None):
#         """Create a new custom exercise"""
#         if exercise_id is not None:
#             return Response(
#                 {"error": "Cannot POST to a specific exercise ID. Use PUT for updates."},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED
#             )
# 
#         serializer = CustomExerciseSerializer(
#             data=request.data,
#             context={'request': request}
#         )
#         if serializer.is_valid():
#             exercise_data = {
#                 'id': len(request.user.custom_exercises or []) + 1,
#                 **serializer.validated_data,
#                 'created_at': timezone.now().isoformat(),
#                 'updated_at': timezone.now().isoformat()
#             }
#             
#             if request.user.custom_exercises is None:
#                 request.user.custom_exercises = []
#             request.user.custom_exercises.append(exercise_data)
#             request.user.save()
#             
#             return Response(
#                 CustomExerciseSerializer(exercise_data).data, 
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
#     def put(self, request, exercise_id):
#         """Update a custom exercise"""
#         if exercise_id is None:
#             return Response(
#                 {"error": "Exercise ID is required for updates"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
# 
#         exercises = request.user.custom_exercises or []
#         exercise_index = next(
#             (index for (index, d) in enumerate(exercises) if d["id"] == exercise_id), 
#             None
#         )
#         
#         if exercise_index is None:
#             return Response(
#                 {"error": "Exercise not found"}, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
# 
#         serializer = CustomExerciseSerializer(
#             exercises[exercise_index],
#             data=request.data,
#             context={'request': request, 'exercise_id': exercise_id}
#         )
#         if serializer.is_valid():
#             exercise_data = {
#                 'id': exercise_id,
#                 **serializer.validated_data,
#                 'created_at': exercises[exercise_index].get('created_at'),
#                 'updated_at': timezone.now().isoformat()
#             }
#             
#             exercises[exercise_index] = exercise_data
#             request.user.custom_exercises = exercises
#             request.user.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
#     def delete(self, request, exercise_id):
#         """Delete a custom exercise"""
#         if exercise_id is None:
#             return Response(
#                 {"error": "Exercise ID is required for deletion"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
# 
#         exercises = request.user.custom_exercises or []
#         exercise_index = next(
#             (index for (index, d) in enumerate(exercises) if d["id"] == exercise_id), 
#             None
#         )
#         
#         if exercise_index is None:
#             return Response(
#                 {"error": "Exercise not found"}, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
# 
#         exercises.pop(exercise_index)
#         request.user.custom_exercises = exercises
#         request.user.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)
