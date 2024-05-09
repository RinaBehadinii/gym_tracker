from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('user/', views.userPage, name='user'),
    path('users/<str:id>/', views.user_details, name='user_details'),
    path('users/', views.users, name='users'),

    path('create_workout/<str:id>', views.createWorkout, name='create_workout'),
    path('update_workout/<str:id>', views.updateWorkout, name='update_workout'),
    path('delete_workout/<str:id>', views.deleteWorkout, name='delete_workout'),
]
