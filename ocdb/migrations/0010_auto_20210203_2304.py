# Generated by Django 3.1.4 on 2021-02-03 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ocdb", "0009_auto_20210130_2337"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="route",
            unique_together={("name", "fk_sector")},
        ),
    ]
