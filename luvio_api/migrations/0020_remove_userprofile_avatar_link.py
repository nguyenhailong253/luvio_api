# Generated by Django 4.1.4 on 2022-12-28 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("luvio_api", "0019_remove_userprofile_profile_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="avatar_link",
        ),
    ]