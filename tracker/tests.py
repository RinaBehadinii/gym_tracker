from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import timedelta

from tracker.models import UserProfile, Workout, WorkoutDetail, Exercise


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.user_details_url = reverse('user_details', args=[1])
        self.create_workout_url = reverse('create_workout', args=[1])
        self.update_workout_url = reverse('update_workout', args=[1])
        self.delete_workout_url = reverse('delete_workout', args=[1])

        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user_profile = UserProfile.objects.create(user=self.user, name='Test User')
        self.group = Group.objects.create(name='gym_user')
        self.user.groups.add(self.group)

        self.exercise = Exercise.objects.create(name='Running', avg_cal_burned_per_min=10)
        self.workout = Workout.objects.create(user=self.user_profile, start_time=timezone.now())
        self.workout_detail = WorkoutDetail.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            duration=timedelta(minutes=30),
            calories_burned=300
        )

    def test_register_page_GET(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/register.html')

    def test_register_page_POST(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPassword123!',
            'password2': 'ComplexPassword123!'
        })
        if response.status_code != 302:
            print("POST response status code:", response.status_code)
            print("POST response context:", response.context)
            print("POST form errors:", response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_page_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/login.html')

    def test_login_page_POST(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

    def test_logout_user(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_home_GET(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/dashboard.html')

    def test_user_details_GET(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user_details', args=[self.user_profile.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/user_details.html')