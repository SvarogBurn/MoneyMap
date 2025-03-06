# Generated by Django 5.1.2 on 2025-03-06 11:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_expense_date_alter_income_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='is_necssity',
            new_name='is_necessity',
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 6, 11, 56, 55, 145844, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 6, 11, 56, 55, 145844, tzinfo=datetime.timezone.utc)),
        ),
    ]
