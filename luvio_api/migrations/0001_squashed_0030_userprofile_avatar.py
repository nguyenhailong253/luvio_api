# Generated by Django 4.1.5 on 2023-01-08 02:09

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfileType",
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
                ("profile_type", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="UserAccount",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("email", models.EmailField(max_length=320, unique=True)),
                ("username", models.CharField(max_length=320, unique=True)),
                ("password", models.CharField(max_length=320)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                (
                    "date_of_birth",
                    models.DateField(blank=True, default=None, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
                (
                    "mobile",
                    models.CharField(
                        blank=True, default=None, max_length=10, null=True
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
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
                (
                    "avatar_link",
                    models.CharField(
                        blank=True, default=None, max_length=3000, null=True
                    ),
                ),
                (
                    "profile_pitch",
                    models.CharField(
                        blank=True, default=None, max_length=3000, null=True
                    ),
                ),
                (
                    "profile_url",
                    models.CharField(
                        blank=True, default=None, max_length=3000, null=True
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "profile_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="luvio_api.profiletype",
                    ),
                ),
                ("date_created", models.DateField(default="2022-12-28")),
            ],
        ),
        migrations.CreateModel(
            name="StateAndTerritory",
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
                ("state_code", models.CharField(max_length=5)),
                ("name", models.CharField(max_length=50)),
                ("country", models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name="Suburb",
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
                ("name", models.CharField(max_length=50)),
                ("postcode", models.CharField(max_length=10)),
                (
                    "state_and_territory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="luvio_api.stateandterritory",
                    ),
                ),
            ],
        ),
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
                (
                    "unit_number",
                    models.CharField(
                        blank=True, default=None, max_length=10, null=True
                    ),
                ),
                ("street_number", models.CharField(max_length=20)),
                ("street_name", models.CharField(max_length=100)),
                (
                    "street_type",
                    models.CharField(
                        blank=True, default=None, max_length=50, null=True
                    ),
                ),
                (
                    "street_type_abbrev",
                    models.CharField(
                        blank=True, default=None, max_length=10, null=True
                    ),
                ),
                (
                    "suburb",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="luvio_api.suburb",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProfilesAddresses",
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
                ("move_in_date", models.DateField(blank=True, default=None, null=True)),
                (
                    "move_out_date",
                    models.DateField(blank=True, default=None, null=True),
                ),
                (
                    "management_start_date",
                    models.DateField(blank=True, default=None, null=True),
                ),
                (
                    "management_end_date",
                    models.DateField(blank=True, default=None, null=True),
                ),
                (
                    "ownership_start_date",
                    models.DateField(blank=True, default=None, null=True),
                ),
                (
                    "ownership_end_date",
                    models.DateField(blank=True, default=None, null=True),
                ),
                ("is_current_residence", models.BooleanField(default=False)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="luvio_api.address",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="luvio_api.userprofile",
                    ),
                ),
                (
                    "profile_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="luvio_api.profiletype",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="userprofile",
            name="addresses",
            field=models.ManyToManyField(
                through="luvio_api.ProfilesAddresses", to="luvio_api.address"
            ),
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="profile_url",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="avatar_link",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="profile_url",
            field=models.CharField(
                blank=True, default=None, max_length=3000, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="date_created",
            field=models.DateField(default="2022-12-29"),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="date_created",
            field=models.DateField(default="2022-12-30"),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="date_created",
            field=models.DateField(default="2023-01-07"),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="avatar",
            field=models.ImageField(
                blank=True, default="avatars/default.jpg", upload_to="avatars/"
            ),
        ),
    ]
