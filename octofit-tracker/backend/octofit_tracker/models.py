from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    team_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    user_id = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    distance = models.FloatField(null=True, blank=True)  # in km
    calories = models.IntegerField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activities'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.activity_type} - {self.duration} mins"


class Leaderboard(models.Model):
    user_id = models.CharField(max_length=100)
    team_id = models.CharField(max_length=100)
    total_points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'

    def __str__(self):
        return f"Rank {self.rank} - User {self.user_id}"


class Workout(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)  # beginner, intermediate, advanced
    duration = models.IntegerField()  # in minutes
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name
