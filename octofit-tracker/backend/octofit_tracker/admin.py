from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model."""
    list_display = ('id', 'name', 'email', 'team_id', 'created_at')
    list_filter = ('team_id', 'created_at')
    search_fields = ('name', 'email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model."""
    list_display = ('id', 'name', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model."""
    list_display = ('id', 'user_id', 'activity_type', 'duration', 'distance', 'calories', 'date', 'created_at')
    list_filter = ('activity_type', 'date', 'created_at')
    search_fields = ('user_id', 'activity_type')
    ordering = ('-date', '-created_at')
    readonly_fields = ('created_at',)
    date_hierarchy = 'date'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model."""
    list_display = ('id', 'user_id', 'team_id', 'total_points', 'rank', 'updated_at')
    list_filter = ('rank', 'team_id', 'updated_at')
    search_fields = ('user_id', 'team_id')
    ordering = ('rank', '-total_points')
    readonly_fields = ('updated_at',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model."""
    list_display = ('id', 'name', 'difficulty', 'duration', 'category', 'created_at')
    list_filter = ('difficulty', 'category', 'created_at')
    search_fields = ('name', 'description', 'category')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
