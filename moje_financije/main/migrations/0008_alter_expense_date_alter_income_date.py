# Generated by Django 5.1.2 on 2025-03-06 12:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_rename_savinggoal_goal_alter_expense_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
