import datetime

from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint


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

    def __str__(self):
        return f"{self.name}"


class Light(models.Model):
    """Sector ligth description."""

    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Orientation(models.Model):
    """Orientation description."""

    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class RockType(models.Model):
    """Rock types."""

    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class AscentStyle(models.Model):
    """Ascent style."""

    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Diary(models.Model):
    """Diary."""

    date = models.DateField(unique=True)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f"{self.date}"


class Person(models.Model):
    """Person."""

    name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=True)
    nick_name = models.CharField(max_length=100, blank=True, unique=True)

    def __str__(self):
        return f"{self.name} {self.last_name} [{self.nick_name}]"


class DiaryPerson(models.Model):
    """One diary can have different persons associated."""

    fk_person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="persons",
    )

    fk_diary = models.ForeignKey(
        Diary, on_delete=models.CASCADE, related_name="diaries"
    )


class SectorManager(models.Manager):
    def get_by_natural_key(self, name, fk_sector):
        """Get by natural key.
        https://docs.djangoproject.com/en/dev/topics/serialization/#natural-keys

        Filter by plain `fk_sector` will not work, because it's an integer.
        Use double underscore __ to compare with property.
        """
        search = self.filter(name=name).filter(fk_sector__name=fk_sector)
        return search.get()


class Sector(models.Model):
    """Sector which can be part of another sector.

    Example:
        Schrammsteine -> Torsteinkette -> Vorderer Torstein
    """

    name = models.CharField(max_length=1000, blank=False)
    name_alt = models.CharField(max_length=1000, blank=True)
    description = models.CharField(max_length=1000, blank=True)

    fk_sector = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.CASCADE,
        related_name="sectors",
    )

    fk_orientation = models.ForeignKey(
        Orientation,
        null=True,
        on_delete=models.CASCADE,
        related_name="orientations",
    )

    fk_light = models.ForeignKey(
        Light,
        null=True,
        on_delete=models.CASCADE,
        related_name="lights",
    )

    ascent_time_min = models.IntegerField(default=0)
    max_height_in_m = models.IntegerField(default=0)
    rain_protected = models.BooleanField(default=False)
    child_friendly = models.BooleanField(default=False)
    windy = models.BooleanField(default=False)
    ascent_description = models.CharField(max_length=1000, blank=True)
    descent_description = models.CharField(max_length=1000, blank=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    altitude = models.FloatField(default=0)
    sub_id_in_parent_sector = models.CharField(max_length=1000, blank=True)
    source = models.CharField(max_length=1000, blank=True)

    objects = SectorManager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        # https://stackoverflow.com/questions/33307892/django-unique-together-with-nullable-foreignkey
        constraints = [
            UniqueConstraint(
                fields=["name", "fk_sector"], name="unique_with_fk_sector"
            ),
            UniqueConstraint(
                fields=[
                    "name",
                ],
                condition=Q(fk_sector=None),
                name="unique_without_fk_sector",
            ),
        ]


class RouteManager(models.Manager):
    def get_by_natural_key(self, name, fk_sector):
        """Get by natural key.
        https://docs.djangoproject.com/en/dev/topics/serialization/#natural-keys

        Filter by plain `fk_sector` will not work, because it's an integer.
        Use double underscore __ to compare with property.
        """
        search = self.filter(name=name).filter(fk_sector__name=fk_sector)
        return search.get()


class Route(models.Model):

    fk_sector = models.ForeignKey(
        Sector, on_delete=models.CASCADE, related_name="route_sectors"
    )

    fk_rock_type = models.ForeignKey(
        RockType, on_delete=models.CASCADE, related_name="route_rock_types", null=True
    )

    name = models.CharField(max_length=100)
    name_alt = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    description_alt = models.CharField(max_length=1000, blank=True)
    length_in_m = models.IntegerField(default=0)
    protection = models.CharField(max_length=1000, blank=True)
    equipment = models.CharField(max_length=1000, blank=True)
    hints = models.CharField(max_length=1000, blank=True)
    source = models.CharField(max_length=1000, blank=True)

    first_ascent_date = models.DateField(default=datetime.date(9999, 9, 9), blank=True)
    first_ascent_persons = models.CharField(max_length=1000, blank=True)

    objects = RouteManager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = [["name", "fk_sector"]]


class RouteCharacters(models.Model):

    fk_route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="routes",
    )

    fk_route_character = models.ForeignKey(
        RouteCharacter,
        on_delete=models.CASCADE,
        related_name="route_characters",
    )

    class Meta:
        unique_together = (
            "fk_route",
            "fk_route_character",
        )


class RouteGrades(models.Model):

    fk_route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="grade_routes",
    )

    fk_ascent_style = models.ForeignKey(
        AscentStyle,
        on_delete=models.CASCADE,
        related_name="route_characters",
    )

    fk_grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name="routes",
    )

    class Meta:
        unique_together = (
            ("fk_route", "fk_ascent_style"),
            ("fk_ascent_style", "fk_grade"),
        )


class Ascent(models.Model):

    fk_diary = models.ForeignKey(
        Diary,
        on_delete=models.CASCADE,
        related_name="ascent_diaries",
    )

    fk_ascent_style = models.ForeignKey(
        AscentStyle,
        on_delete=models.CASCADE,
        related_name="ascent_styles",
    )

    fk_route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="ascent_routes",
    )

    description = models.CharField(max_length=1000)
    ascent_number = models.IntegerField(blank=True, validators=[MaxValueValidator(100)])


class RopeParty(models.Model):

    fk_ascent = models.ForeignKey(
        Ascent,
        on_delete=models.CASCADE,
        related_name="rope_party_ascents",
    )

    fk_person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="rope_party_persons",
    )

    class Meta:
        unique_together = (
            "fk_ascent",
            "fk_person",
        )
