# Generated by Django 4.1.4 on 2022-12-28 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("luvio_api", "0020_remove_userprofile_avatar_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="avatar_link",
            field=models.CharField(
                blank=True, default=None, max_length=3000, null=True
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="profile_url",
            field=models.CharField(
                blank=True, default=None, max_length=3000, null=True, unique=True
            ),
        ),
    ]