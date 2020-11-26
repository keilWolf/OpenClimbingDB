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
