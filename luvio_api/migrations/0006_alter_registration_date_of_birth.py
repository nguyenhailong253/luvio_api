# Generated by Django 4.1.4 on 2022-12-18 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luvio_api', '0005_alter_registration_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]
