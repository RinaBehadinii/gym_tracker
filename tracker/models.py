from django.db import models
from django.contrib.auth.models import User as AuthUser


class User(models.Model):
    # user = models.OneToOneField(AuthUser, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True)  # Changed to IntegerField
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField(auto_now_add=True, null=True)  # Changed to DateTimeField
    end_time = models.DateTimeField(auto_now_add=True, null=True)  # Changed to DateTimeField

    def __str__(self):
        return f"{self.user.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Exercise(models.Model):
    name = models.CharField(max_length=200, null=True)
    avg_cal_burned_per_min = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class WorkoutDetail(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, null=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True)
    duration = models.DurationField(null=True)
    calories_burned = models.IntegerField(null=True)
