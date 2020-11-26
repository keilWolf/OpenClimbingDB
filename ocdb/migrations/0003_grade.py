# Generated by Django 3.1.3 on 2020-11-26 21:45

from django.db import migrations, models
import django.db.models.deletion

from ocdb.util.custom_migration_operation import LoadFixture


class Migration(migrations.Migration):

    dependencies = [
        ("ocdb", "0002_gradesystem"),
    ]

    operations = [
        migrations.CreateModel(
            name="Grade",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("weight", models.IntegerField()),
                (
                    "fk_grade_system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="grade_systems",
                        to="ocdb.gradesystem",
                    ),
                ),
            ],
        ),
        LoadFixture("Grade", "grade_fixture"),
    ]
