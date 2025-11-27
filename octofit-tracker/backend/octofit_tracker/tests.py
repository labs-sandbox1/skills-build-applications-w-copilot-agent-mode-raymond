from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import date


class UserModelTest(TestCase):
    """Test cases for User model."""

    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="password123"
        )

    def test_user_creation(self):
        """Test that a user can be created successfully."""
        self.assertEqual(self.user.name, "Test User")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertIsNotNone(self.user.created_at)

    def test_user_str(self):
        """Test the string representation of a user."""
        self.assertEqual(str(self.user), "Test User")


class TeamModelTest(TestCase):
    """Test cases for Team model."""

    def setUp(self):
        self.team = Team.objects.create(
            name="Test Team",
            description="A test team description"
        )

    def test_team_creation(self):
        """Test that a team can be created successfully."""
        self.assertEqual(self.team.name, "Test Team")
        self.assertEqual(self.team.description, "A test team description")
        self.assertIsNotNone(self.team.created_at)

    def test_team_str(self):
        """Test the string representation of a team."""
        self.assertEqual(str(self.team), "Test Team")


class ActivityModelTest(TestCase):
    """Test cases for Activity model."""

    def setUp(self):
        self.activity = Activity.objects.create(
            user_id="user123",
            activity_type="Running",
            duration=30,
            distance=5.0,
            calories=300,
            date=date.today()
        )

    def test_activity_creation(self):
        """Test that an activity can be created successfully."""
        self.assertEqual(self.activity.user_id, "user123")
        self.assertEqual(self.activity.activity_type, "Running")
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.distance, 5.0)
        self.assertEqual(self.activity.calories, 300)

    def test_activity_str(self):
        """Test the string representation of an activity."""
        self.assertEqual(str(self.activity), "Running - 30 mins")


class LeaderboardModelTest(TestCase):
    """Test cases for Leaderboard model."""

    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            user_id="user123",
            team_id="team456",
            total_points=1500,
            rank=1
        )

    def test_leaderboard_creation(self):
        """Test that a leaderboard entry can be created successfully."""
        self.assertEqual(self.leaderboard.user_id, "user123")
        self.assertEqual(self.leaderboard.team_id, "team456")
        self.assertEqual(self.leaderboard.total_points, 1500)
        self.assertEqual(self.leaderboard.rank, 1)

    def test_leaderboard_str(self):
        """Test the string representation of a leaderboard entry."""
        self.assertEqual(str(self.leaderboard), "Rank 1 - User user123")


class WorkoutModelTest(TestCase):
    """Test cases for Workout model."""

    def setUp(self):
        self.workout = Workout.objects.create(
            name="Morning Cardio",
            description="A high-intensity cardio workout",
            difficulty="intermediate",
            duration=45,
            category="Cardio"
        )

    def test_workout_creation(self):
        """Test that a workout can be created successfully."""
        self.assertEqual(self.workout.name, "Morning Cardio")
        self.assertEqual(self.workout.difficulty, "intermediate")
        self.assertEqual(self.workout.duration, 45)
        self.assertEqual(self.workout.category, "Cardio")

    def test_workout_str(self):
        """Test the string representation of a workout."""
        self.assertEqual(str(self.workout), "Morning Cardio")


class UserAPITest(APITestCase):
    """Test cases for User API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'name': 'API Test User',
            'email': 'apitest@example.com',
            'password': 'testpassword',
            'team_id': 'team123'
        }

    def test_create_user(self):
        """Test creating a user via API."""
        response = self.client.post(reverse('user-list'), self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'API Test User')

    def test_get_users_list(self):
        """Test retrieving list of users."""
        User.objects.create(**self.user_data)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.team_data = {
            'name': 'API Test Team',
            'description': 'A team created via API'
        }

    def test_create_team(self):
        """Test creating a team via API."""
        response = self.client.post(reverse('team-list'), self.team_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)

    def test_get_teams_list(self):
        """Test retrieving list of teams."""
        Team.objects.create(**self.team_data)
        response = self.client.get(reverse('team-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.activity_data = {
            'user_id': 'user123',
            'activity_type': 'Swimming',
            'duration': 60,
            'distance': 2.0,
            'calories': 500,
            'date': str(date.today())
        }

    def test_create_activity(self):
        """Test creating an activity via API."""
        response = self.client.post(reverse('activity-list'), self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)

    def test_get_activities_list(self):
        """Test retrieving list of activities."""
        Activity.objects.create(
            user_id='user123',
            activity_type='Swimming',
            duration=60,
            distance=2.0,
            calories=500,
            date=date.today()
        )
        response = self.client.get(reverse('activity-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    """Test cases for Leaderboard API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.leaderboard_data = {
            'user_id': 'user123',
            'team_id': 'team456',
            'total_points': 2000,
            'rank': 1
        }

    def test_create_leaderboard_entry(self):
        """Test creating a leaderboard entry via API."""
        response = self.client.post(reverse('leaderboard-list'), self.leaderboard_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_leaderboard_list(self):
        """Test retrieving leaderboard."""
        Leaderboard.objects.create(**self.leaderboard_data)
        response = self.client.get(reverse('leaderboard-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.workout_data = {
            'name': 'Evening Yoga',
            'description': 'Relaxing yoga session',
            'difficulty': 'beginner',
            'duration': 30,
            'category': 'Flexibility'
        }

    def test_create_workout(self):
        """Test creating a workout via API."""
        response = self.client.post(reverse('workout-list'), self.workout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)

    def test_get_workouts_list(self):
        """Test retrieving list of workouts."""
        Workout.objects.create(**self.workout_data)
        response = self.client.get(reverse('workout-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIRootTest(APITestCase):
    """Test cases for API root endpoint."""

    def test_api_root_accessible(self):
        """Test that the API root endpoint is accessible."""
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)
