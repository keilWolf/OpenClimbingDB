from django.db import models


class GradeSystemType(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return "%s" % (self.name)


class GradeSystem(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    fk_grade_system_type = models.ForeignKey(
        GradeSystemType,
        on_delete=models.CASCADE,
        related_name="grade_system_types",
    )

    def __str__(self):
        return "%s" % (self.name)


class Grade(models.Model):
    name = models.CharField(max_length=100, blank=False)
    weight = models.IntegerField()
    fk_grade_system = models.ForeignKey(
        GradeSystem,
        on_delete=models.CASCADE,
        related_name="grade_systems",
    )

    def __str__(self):
        return "%s" % (self.name)


class RouteCharacter(models.Model):
    """Route character representation."""

    name = models.CharField(max_length=100, blank=False, unique=True)


class Light(models.Model):
    """Sector ligth description."""

    name = models.CharField(max_length=100, blank=False, unique=True)


class Orientation(models.Model):
    """Orientation description."""

    name = models.CharField(max_length=100, blank=False, unique=True)


class RockType(models.Model):
    """Rock types."""

    name = models.CharField(max_length=100, blank=False, unique=True)


class AscentStyle(models.Model):
    """Ascent style."""

    name = models.CharField(max_length=100, blank=False, unique=True)
