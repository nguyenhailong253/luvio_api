# Generated by Django 4.1.4 on 2022-12-19 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luvio_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_email', models.EmailField(default='invalidemail', max_length=320, unique=True)),
                ('username', models.CharField(default='invalidemail', max_length=320, unique=True)),
                ('password', models.CharField(max_length=320)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='RegistrationTest',
        ),
    ]
