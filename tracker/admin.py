from django.contrib import admin

from .models import User, Workout, Exercise, WorkoutDetail

# Register your models here.


admin.site.register(User)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(WorkoutDetail)
