# Generated by Django 3.1.4 on 2021-03-04 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ocdb", "0016_auto_20210304_2101"),
    ]

    operations = [
        migrations.AddField(
            model_name="route",
            name="first_ascent_persons",
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.DeleteModel(
            name="FirstAscentionistRoute",
        ),
    ]
