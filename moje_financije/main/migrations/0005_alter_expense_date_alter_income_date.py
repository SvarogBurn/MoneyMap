# Generated by Django 5.1.4 on 2025-03-03 21:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_rename_source_income_name_alter_expense_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 3, 3, 21, 12, 37, 330240, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="income",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 3, 3, 21, 12, 37, 330240, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
