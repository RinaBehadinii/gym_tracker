from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('', views.home, name='home'),
    path('users/<str:id>/', views.user_details, name='user_details'),
    path('users/', views.users, name='users'),

    path('create_workout/<str:id>', views.create_workout, name='create_workout'),
    path('update_workout/<str:id>', views.update_workout, name='update_workout'),
    path('delete_workout/<str:id>', views.delete_workout, name='delete_workout'),
]
