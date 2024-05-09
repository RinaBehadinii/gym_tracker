from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as AuthUser

from .models import Workout, UserProfile


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = []


class CreateUserForm(UserCreationForm):
    name = forms.CharField(max_length=200, required=False)
    age = forms.IntegerField(required=False)
    phone = forms.CharField(max_length=200, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = AuthUser
        fields = ('username', 'email', 'password1', 'password2', 'name', 'age', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = UserProfile(user=user, name=self.cleaned_data['name'], age=self.cleaned_data['age'],
                                       phone=self.cleaned_data['phone'])
            user_profile.save()
        return user
