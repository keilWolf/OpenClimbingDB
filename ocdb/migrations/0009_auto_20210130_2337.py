# Generated by Django 3.1.4 on 2021-01-30 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ocdb", "0008_auto_20210102_1050"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="sector",
            unique_together={("name", "fk_sector")},
        ),
    ]
