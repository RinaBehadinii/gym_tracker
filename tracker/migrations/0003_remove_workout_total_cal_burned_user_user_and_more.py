# Generated by Django 5.0.4 on 2024-05-09 20:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_rename_workoutdetails_workoutdetail'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='total_cal_burned',
        ),
        migrations.AddField(
            model_name='user',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workoutdetail',
            name='exercise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.exercise'),
        ),
        migrations.AlterField(
            model_name='workoutdetail',
            name='workout',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.workout'),
        ),
    ]
