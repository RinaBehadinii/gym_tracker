from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models.functions import Now
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from tracker.models import Workout, WorkoutDetail, Exercise, UserProfile
from django.db.models import Sum, Count, Avg, Min, ExpressionWrapper, fields, Q

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import WorkoutForm, CreateUserForm

from django.contrib import messages
from django.http import HttpResponse


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            group = Group.objects.get(name='gym_user')
            user.groups.add(group)

            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user)

            messages.success(request, f'Account created for {username}')
            return redirect('login')

    context = {'form': form}
    return render(request, 'tracker/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect.')
    context = {}
    return render(request, 'tracker/login.html', context)


def userPage(request):
    context = {}
    return render(request, 'tracker/user.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'gym_user'])
def home(request):
    # Today statistics
    today = timezone.now().date()

    workouts_today = Workout.objects.filter(start_time__date=today)
    users_today = UserProfile.objects.filter(workout__in=workouts_today).distinct()
    total_users_today = users_today.count()
    total_workouts_today = workouts_today.count()
    total_exercises = Exercise.objects.filter(workoutdetail__workout__in=workouts_today).distinct().count()
    total_calories = \
        WorkoutDetail.objects.filter(workout__in=workouts_today).aggregate(total_calories=Sum('calories_burned'))[
            'total_calories']

    if total_calories is None:
        total_calories = 0

    # UserProfile statistics
    total_users = UserProfile.objects.count()
    average_age = UserProfile.objects.aggregate(Avg('age'))['age__avg']
    # Calculate average membership duration in days in one step
    average_membership_duration = UserProfile.objects.annotate(
        duration_days=ExpressionWrapper(
            (Now() - Min('date_created')),
            output_field=fields.DurationField()
        )
    ).aggregate(
        average_duration_days=Avg('duration_days')
    )['average_duration_days']

    # Convert result to integer days
    average_membership_duration_days = int(average_membership_duration.days) if average_membership_duration else 0

    # Workout statistics
    total_workouts = Workout.objects.count()
    average_duration = WorkoutDetail.objects.aggregate(average_duration=Avg('duration'))['average_duration']
    average_calories_per_workout = WorkoutDetail.objects.aggregate(average_calories=Avg('calories_burned'))[
        'average_calories']
    most_popular_exercise = Exercise.objects.annotate(num_used=Count('workoutdetail')).order_by('-num_used').first()

    average_workouts_per_user = total_workouts / total_users if total_users else 0

    context = {
        'total_users_today': total_users_today,
        'total_workouts_today': total_workouts_today,
        'total_exercises': total_exercises,
        'total_calories': total_calories,
        'total_users': total_users,
        'average_age': average_age,
        'average_membership_duration': average_membership_duration_days,
        'total_workouts': total_workouts,
        'average_duration': average_duration,
        'average_calories_per_workout': average_calories_per_workout,
        'most_popular_exercise': most_popular_exercise,
        'average_workouts_per_user': average_workouts_per_user,
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required(login_url='login')
def user_details(request, id):
    try:
        user_profile = UserProfile.objects.get(id=id)
    except UserProfile.DoesNotExist:
        return HttpResponse("User profile does not exist.", status=404)

    if request.user != user_profile.user and not request.user.groups.filter(name='admin').exists():
        return HttpResponseForbidden("You are not authorized to view this page.")

    workouts = Workout.objects.filter(user=user_profile)
    total_workouts = workouts.count()

    total_calories = 0
    for workout in workouts:
        total_calories += WorkoutDetail.objects.filter(workout=workout).aggregate(Sum('calories_burned'))[
                              'calories_burned__sum'] or 0

    all_workout_details = workouts.annotate(
        total_duration=Sum('workoutdetail__duration'),
        total_exercises=Count('workoutdetail__exercise', distinct=True),
        total_calories=Sum('workoutdetail__calories_burned')
    ).values(
        'id', 'start_time', 'total_duration', 'total_exercises', 'total_calories'
    )

    return render(request, 'tracker/user_details.html', {
        'user': user_profile, 'workouts': workouts, 'total_calories': total_calories,
        "total_workouts": total_workouts, 'all_workout_details': all_workout_details
    })


@login_required(login_url='login')
@admin_only
def users(request):
    query = request.GET.get('query', '')
    if query:
        users = UserProfile.objects.filter(Q(name__icontains=query))
    else:
        users = UserProfile.objects.all()

    return render(request, 'tracker/users.html', {'users': users})


@login_required(login_url='login')
def createWorkout(request, id):
    WorkoutDetailFormSet = inlineformset_factory(
        Workout, WorkoutDetail,
        fields=('exercise', 'duration', 'calories_burned'),
        extra=1,
        can_delete=False
    )
    user = UserProfile.objects.get(id=id)
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            created_workout = form.save(commit=False)
            created_workout.user = user
            formset = WorkoutDetailFormSet(request.POST, instance=created_workout)
            if formset.is_valid():
                created_workout.save()
                formset.save()
                return redirect(reverse('user_details', kwargs={'id': id}))
    else:
        form = WorkoutForm()
        formset = WorkoutDetailFormSet(instance=Workout())

    context = {'form': form, 'formset': formset, 'user': user}
    return render(request, 'tracker/create_workout.html', context)


@login_required(login_url='login')
def updateWorkout(request, id):
    WorkoutDetailFormSet = inlineformset_factory(
        Workout, WorkoutDetail,
        fields=('exercise', 'duration', 'calories_burned'),
        extra=0,
        can_delete=False
    )
    workout = Workout.objects.get(id=id)
    form = WorkoutForm(request.POST or None, instance=workout)
    formset = WorkoutDetailFormSet(request.POST or None, instance=workout)

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('user_details', id=workout.user.id)

    context = {'form': form, 'formset': formset}
    return render(request, 'tracker/create_workout.html', context)


@login_required(login_url='login')
def deleteWorkout(request, id):
    workout = Workout.objects.get(id=id)

    if (request.method == 'POST'):
        workout.delete()
        return redirect(reverse('user_details', kwargs={'id': workout.user.id}))

    context = {'item': workout}
    return render(request, 'tracker/delete_workout.html', context)
