from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'team_id', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'activity_type', 'duration', 'distance', 'calories', 'date', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'team_id', 'total_points', 'rank', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'difficulty', 'duration', 'category', 'created_at']
