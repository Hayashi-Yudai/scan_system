# Generated by Django 3.1.1 on 2021-08-13 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TDSData",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("measured_date", models.DateTimeField(auto_now_add=True)),
                ("start_position", models.PositiveIntegerField()),
                ("end_position", models.PositiveIntegerField()),
                ("step", models.PositiveIntegerField()),
                ("lockin_time", models.PositiveIntegerField()),
                ("position_data", models.TextField()),
                ("intensity_data", models.TextField()),
            ],
        ),
    ]
