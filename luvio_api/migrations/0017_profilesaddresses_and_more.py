# Generated by Django 4.1.4 on 2022-12-28 23:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "luvio_api",
            "0016_rename_end_date_landlordprofilesaddresses_ownership_end_date_and_more",
        ),
    ]

    operations = [
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
                ("move_in_date", models.DateField(blank=True, null=True)),
                ("move_out_date", models.DateField(blank=True, null=True)),
                ("management_start_date", models.DateField(blank=True, null=True)),
                ("management_end_date", models.DateField(blank=True, null=True)),
                ("ownership_start_date", models.DateField(blank=True, null=True)),
                ("ownership_end_date", models.DateField(blank=True, null=True)),
                ("is_current_residence", models.BooleanField(default=False)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="luvio_api.address",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="landlordprofilesaddresses",
            name="address",
        ),
        migrations.RemoveField(
            model_name="landlordprofilesaddresses",
            name="profile",
        ),
        migrations.RemoveField(
            model_name="tenantprofilesaddresses",
            name="address",
        ),
        migrations.RemoveField(
            model_name="tenantprofilesaddresses",
            name="profile",
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="avatar_link",
            field=models.CharField(
                blank=True, default=None, max_length=3000, null=True
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="date_created",
            field=models.DateField(default="2022-12-28"),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="profile_pitch",
            field=models.CharField(
                blank=True, default=None, max_length=3000, null=True
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="profile_url",
            field=models.CharField(
                blank=True, default=None, max_length=3000, null=True
            ),
        ),
        migrations.DeleteModel(
            name="AgentProfilesAddresses",
        ),
        migrations.DeleteModel(
            name="LandlordProfilesAddresses",
        ),
        migrations.DeleteModel(
            name="TenantProfilesAddresses",
        ),
        migrations.AddField(
            model_name="profilesaddresses",
            name="profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="luvio_api.userprofile"
            ),
        ),
        migrations.AddField(
            model_name="profilesaddresses",
            name="profile_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="luvio_api.profiletype"
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="addresses",
            field=models.ManyToManyField(
                through="luvio_api.ProfilesAddresses", to="luvio_api.address"
            ),
        ),
    ]
