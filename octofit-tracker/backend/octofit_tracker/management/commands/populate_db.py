from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random
from pymongo import MongoClient


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Connect to MongoDB directly
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel_result = db.teams.insert_one({
            'name': 'Team Marvel',
            'description': 'Earth\'s Mightiest Heroes unite for fitness supremacy!',
            'created_at': datetime.now()
        })
        team_marvel_id = team_marvel_result.inserted_id

        team_dc_result = db.teams.insert_one({
            'name': 'Team DC',
            'description': 'Justice League members competing for ultimate strength!',
            'created_at': datetime.now()
        })
        team_dc_id = team_dc_result.inserted_id

        # Create Users (Superheroes)
        self.stdout.write('Creating users...')
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'password': 'stark123'},
            {'name': 'Captain America', 'email': 'captainamerica@marvel.com', 'password': 'shield123'},
            {'name': 'Thor', 'email': 'thor@marvel.com', 'password': 'hammer123'},
            {'name': 'Black Widow', 'email': 'blackwidow@marvel.com', 'password': 'spy123'},
            {'name': 'Hulk', 'email': 'hulk@marvel.com', 'password': 'smash123'},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'password': 'web123'},
        ]

        dc_heroes = [
            {'name': 'Superman', 'email': 'superman@dc.com', 'password': 'krypton123'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'password': 'gotham123'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'password': 'amazon123'},
            {'name': 'The Flash', 'email': 'flash@dc.com', 'password': 'speed123'},
            {'name': 'Aquaman', 'email': 'aquaman@dc.com', 'password': 'ocean123'},
            {'name': 'Green Lantern', 'email': 'greenlantern@dc.com', 'password': 'willpower123'},
        ]

        marvel_user_ids = []
        for hero in marvel_heroes:
            result = db.users.insert_one({
                'name': hero['name'],
                'email': hero['email'],
                'password': hero['password'],
                'team_id': str(team_marvel_id),
                'created_at': datetime.now()
            })
            marvel_user_ids.append(result.inserted_id)

        dc_user_ids = []
        for hero in dc_heroes:
            result = db.users.insert_one({
                'name': hero['name'],
                'email': hero['email'],
                'password': hero['password'],
                'team_id': str(team_dc_id),
                'created_at': datetime.now()
            })
            dc_user_ids.append(result.inserted_id)

        all_user_ids = marvel_user_ids + dc_user_ids

        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'CrossFit']
        
        for user_id in all_user_ids:
            # Create 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                distance = round(random.uniform(2.0, 20.0), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                calories = duration * random.randint(5, 10)
                days_ago = random.randint(0, 30)
                activity_date = datetime.now() - timedelta(days=days_ago)
                
                db.activities.insert_one({
                    'user_id': str(user_id),
                    'activity_type': activity_type,
                    'duration': duration,
                    'distance': distance,
                    'calories': calories,
                    'date': activity_date,
                    'created_at': datetime.now()
                })

        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard...')
        leaderboard_data = []
        for user_id in all_user_ids:
            user = db.users.find_one({'_id': user_id})
            activities = list(db.activities.find({'user_id': str(user_id)}))
            total_points = sum(activity['calories'] for activity in activities)
            
            leaderboard_data.append({
                'user_id': str(user_id),
                'team_id': user['team_id'],
                'total_points': total_points,
                'rank': 0,  # Will update after sorting
                'updated_at': datetime.now()
            })

        # Sort by total points and assign ranks
        leaderboard_data.sort(key=lambda x: x['total_points'], reverse=True)
        for idx, entry in enumerate(leaderboard_data):
            entry['rank'] = idx + 1
            db.leaderboard.insert_one(entry)

        # Create Workouts
        self.stdout.write('Creating workouts...')
        workouts = [
            {
                'name': 'Superhero Strength Training',
                'description': 'Build power like Thor with compound lifts and explosive movements.',
                'difficulty': 'advanced',
                'duration': 60,
                'category': 'Strength'
            },
            {
                'name': 'Spider-Sense Cardio',
                'description': 'Enhance your agility and endurance with interval training.',
                'difficulty': 'intermediate',
                'duration': 45,
                'category': 'Cardio'
            },
            {
                'name': 'Black Widow Flexibility Flow',
                'description': 'Master flexibility and balance through dynamic stretching.',
                'difficulty': 'beginner',
                'duration': 30,
                'category': 'Flexibility'
            },
            {
                'name': 'Captain America Circuit',
                'description': 'Full-body workout combining strength and cardio.',
                'difficulty': 'intermediate',
                'duration': 50,
                'category': 'Circuit Training'
            },
            {
                'name': 'Flash Speed Training',
                'description': 'Sprint intervals and plyometrics for explosive speed.',
                'difficulty': 'advanced',
                'duration': 40,
                'category': 'Speed'
            },
            {
                'name': 'Hulk Smash Heavy Lifting',
                'description': 'Maximum strength development with heavy compound movements.',
                'difficulty': 'advanced',
                'duration': 70,
                'category': 'Strength'
            },
            {
                'name': 'Wonder Woman Warrior Workout',
                'description': 'Combat-inspired training for functional fitness.',
                'difficulty': 'intermediate',
                'duration': 55,
                'category': 'Functional'
            },
            {
                'name': 'Aquaman Swim Session',
                'description': 'Pool-based cardio and resistance training.',
                'difficulty': 'beginner',
                'duration': 45,
                'category': 'Swimming'
            },
            {
                'name': 'Batman Dark Knight Conditioning',
                'description': 'Mixed martial arts and tactical fitness training.',
                'difficulty': 'advanced',
                'duration': 60,
                'category': 'MMA'
            },
            {
                'name': 'Green Lantern Willpower Core',
                'description': 'Core strengthening and mental focus exercises.',
                'difficulty': 'beginner',
                'duration': 35,
                'category': 'Core'
            },
        ]

        for workout_data in workouts:
            workout_data['created_at'] = datetime.now()
            db.workouts.insert_one(workout_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully populated database!'))
        self.stdout.write(self.style.SUCCESS(f'Created:'))
        self.stdout.write(f'  - {db.teams.count_documents({})} teams')
        self.stdout.write(f'  - {db.users.count_documents({})} users')
        self.stdout.write(f'  - {db.activities.count_documents({})} activities')
        self.stdout.write(f'  - {db.leaderboard.count_documents({})} leaderboard entries')
        self.stdout.write(f'  - {db.workouts.count_documents({})} workouts')
        
        # Close MongoDB connection
        client.close()
