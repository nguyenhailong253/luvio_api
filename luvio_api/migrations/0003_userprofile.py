# Generated by Django 4.1.4 on 2022-12-20 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('luvio_api', '0002_alter_useraccount_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar_link', models.CharField(max_length=3000)),
                ('profile_pitch', models.CharField(max_length=3000)),
                ('profile_url', models.CharField(max_length=3000)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('profile_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luvio_api.profiletype')),
            ],
        ),
    ]