# Generated by Django 4.1.4 on 2022-12-20 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luvio_api', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar_link',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pitch',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]