# Generated by Django 3.1.4 on 2021-03-03 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ocdb", "0011_auto_20210207_1353"),
    ]

    operations = [
        migrations.AddField(
            model_name="sector",
            name="name_alt",
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
