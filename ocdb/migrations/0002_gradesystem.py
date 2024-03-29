# Generated by Django 3.1.3 on 2020-11-26 21:31

from django.db import migrations, models
import django.db.models.deletion

from ocdb.util.custom_migration_operation import LoadFixture


class Migration(migrations.Migration):

    dependencies = [
        ("ocdb", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GradeSystem",
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
                ("name", models.CharField(blank=True, default="", max_length=100)),
                (
                    "fk_grade_system_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="grade_system_types",
                        to="ocdb.gradesystemtype",
                    ),
                ),
            ],
        ),
        LoadFixture("GradeSystem", "grade_system_fixture"),
    ]
