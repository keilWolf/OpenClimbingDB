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