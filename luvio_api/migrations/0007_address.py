# Generated by Django 4.1.4 on 2022-12-25 03:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("luvio_api", "0006_stateandterritory_suburb"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("display_address", models.CharField(max_length=320)),
                ("unit_number", models.CharField(max_length=10)),
                ("street_number", models.CharField(max_length=20)),
                ("street_name", models.CharField(max_length=100)),
                ("street_type", models.CharField(max_length=50)),
                ("street_type_abbrev", models.CharField(max_length=10)),
                (
                    "suburb",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="luvio_api.suburb",
                    ),
                ),
            ],
        ),
    ]
