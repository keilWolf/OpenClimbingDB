# Generated by Django 3.1.4 on 2021-01-02 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ocdb", "0007_auto_20201229_1611"),
    ]

    operations = [
        migrations.AddField(
            model_name="sector",
            name="description",
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name="diary",
            name="description",
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
