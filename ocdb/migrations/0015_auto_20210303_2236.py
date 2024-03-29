# Generated by Django 3.1.4 on 2021-03-03 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ocdb", "0014_route_name_alt"),
    ]

    operations = [
        migrations.AddField(
            model_name="route",
            name="description_alt",
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name="route",
            name="source",
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name="route",
            name="fk_rock_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="route_rock_types",
                to="ocdb.rocktype",
            ),
        ),
    ]
