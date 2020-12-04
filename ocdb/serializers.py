from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ocdb import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "id", "username"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class GradeSystemTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.GradeSystemType
        fields = ["url", "name"]


class GradeSystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.GradeSystem
        fields = ["url", "name", "fk_grade_system_type"]


class GradeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Grade
        fields = ["url", "name", "weight", "fk_grade_system"]


class RouteCharacterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RouteCharacter
        fields = ["url", "name"]


class LightSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Light
        fields = ["url", "name"]


class OrientationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Orientation
        fields = ["url", "name"]


class RockTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RockType
        fields = ["url", "name"]


class AscentStyleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AscentStyle
        fields = ["url", "name"]


class DiarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Diary
        fields = ["url", "date", "description"]


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Person
        fields = ["url", "name", "last_name", "nick_name"]


class DiaryPersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.DiaryPerson
        fields = "__all__"


class SectorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Sector
        fields = "__all__"


class RouteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Route
        fields = "__all__"


class RouteCharactersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RouteCharacters
        fields = "__all__"


class RouteGradesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RouteGrades
        fields = "__all__"


class AscentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Ascent
        fields = "__all__"


class RopePartySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RopeParty
        fields = "__all__"


class FirstAscentionistsOfRouteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.FirstAscentionistRoute
        fields = "__all__"
