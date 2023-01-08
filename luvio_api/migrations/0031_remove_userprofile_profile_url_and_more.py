# Generated by Django 4.1.5 on 2023-01-08 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("luvio_api", "0001_squashed_0030_userprofile_avatar"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="profile_url",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="profile_uri",
            field=models.CharField(
                blank=True, default=None, max_length=100, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="date_created",
            field=models.DateField(default="2023-01-08"),
        ),
    ]
