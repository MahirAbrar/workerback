from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ExerciseList

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'created_at', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)
    
    # Add custom fields to fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('custom_exercises', 'workouts', 'templates', 'created_at')}),
    )
    
    # Add custom fields to add form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('email', 'custom_exercises', 'workouts', 'templates')}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(ExerciseList)
class ExerciseListAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_muscle', 'secondary_muscle', 'tertiary_muscle')
    search_fields = ('name', 'primary_muscle')
    list_filter = ('primary_muscle', 'secondary_muscle', 'tertiary_muscle')
