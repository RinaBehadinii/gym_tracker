# Gym Workout Tracker

## Project Overview

The Gym Workout Tracker is a sophisticated web-based application developed using Django. It is designed for gym-goers and facility administrators to log workouts, monitor progress, and manage user accounts effectively. The system offers robust security features and scalability, provided by Django, to handle different user roles and detailed workout statistics.

## Features

- **User Authentication:** Secure login, registration, and user management.
- **Workout Logging:** Users can record and track details of their workouts.
- **Real-Time Statistics:** Access to real-time statistics regarding workouts and user performance.
- **Role-Based Access Control:** Different access levels for regular users and administrators.

## Technology Stack

- **Backend:** Django
- **Database:** SQLite (development), PostgreSQL (production)
- **Frontend:** HTML, CSS
- **Deployment:** Recommended deployment on platforms like Heroku, AWS, or similar.

## Installation

```bash
# Clone the repository
git clone https://github.com/RinaBehadinii/gym_tracker
cd gym-workout-tracker

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver

```
## Post-Installation Steps

After creating the superuser, follow these steps to complete the setup:

### 1. Create Roles in the Group Table

1. Access the Django admin interface at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).
2. Navigate to the **Groups** section.
3. Create two new groups:
   - `admin`
   - `gym_user`

### 2. Assign the Admin Role to Your Superuser

1. Go to the **Users** section in the admin interface.
2. Select your superuser.
3. Assign the `admin` group to your superuser.

### 3. Create a UserProfile for Your Superuser

1. Navigate to the **UserProfiles** section.
2. Create a new UserProfile referencing your superuser.