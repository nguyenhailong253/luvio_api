# Generated by Django 4.1.4 on 2022-12-13 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('luvio_api', '0002_profiletype_alter_useraccount_options'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='useraccount',
            table='user_accounts',
        ),
    ]
