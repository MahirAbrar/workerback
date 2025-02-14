from django.urls import path, include
from .views import (
    RegisterView, LoginView, ExerciseListView, 
    UserProfileView, WorkoutView, TemplateView, CustomExerciseView
)

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='rest_login'),
    # logout using a post method at 
    # /api/auth/logout
    path('auth/', include('dj_rest_auth.urls')),  #Automatically does the token handling, session management, pass reset
    path('auth/registration/', RegisterView.as_view(), name='rest_register'),
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('workouts/', WorkoutView.as_view(), name='workouts'),
    path('templates/', TemplateView.as_view(), name='templates'),
    path('templates/<int:template_id>/', TemplateView.as_view(), name='template-detail'),
    # path('custom-exercises/', CustomExerciseView.as_view(), name='custom-exercises'),
    # path('custom-exercises/<int:exercise_id>/', CustomExerciseView.as_view(), name='custom-exercise-detail'),
] 