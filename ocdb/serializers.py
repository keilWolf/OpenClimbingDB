from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ocdb.models import GradeSystemType, GradeSystem, Grade


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
        model = GradeSystemType
        fields = ["url", "name"]


class GradeSystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GradeSystem
        fields = ["url", "name", "fk_grade_system_type"]


class GradeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Grade
        fields = ["url", "name", "weight", "fk_grade_system"]
