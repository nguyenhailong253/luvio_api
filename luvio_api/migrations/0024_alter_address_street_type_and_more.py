# Generated by Django 4.1.4 on 2022-12-28 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("luvio_api", "0023_useraccount_mobile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="street_type",
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="address",
            name="street_type_abbrev",
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="address",
            name="unit_number",
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]