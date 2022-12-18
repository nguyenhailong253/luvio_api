# Generated by Django 4.1.4 on 2022-12-13 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luvio_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_type', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'profile_types',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='useraccount',
            options={'managed': False},
        ),
    ]