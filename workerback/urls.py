from django.contrib import admin
from django.urls import path, include
from api.views import RegisterView, LoginView, ExerciseListView, UserProfileView, WorkoutView, TemplateView, CustomExerciseView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', LoginView.as_view(), name='rest_login'),  # Custom login view
    path('api/auth/', include('dj_rest_auth.urls')),  # Other auth endpoints
    path('api/auth/registration/', RegisterView.as_view(), name='rest_register'),
    path('accounts/', include('allauth.urls')),
    path('api/exercises/', ExerciseListView.as_view(), name='exercise-list'),  # New URL
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),  # New endpoint
    path('api/workouts/', WorkoutView.as_view(), name='workouts'),
    path('api/templates/', TemplateView.as_view(), name='templates'),
    path('api/templates/<int:template_id>/', TemplateView.as_view(), name='template-detail'),
    path('api/custom-exercises/', CustomExerciseView.as_view(), name='custom-exercises'),
    # path('api/custom-exercises/<int:exercise_id>/', CustomExerciseView.as_view(), name='custom-exercise-detail'),
]