from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from ocdb import serializers
from ocdb import models


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class GradeSystemTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = models.GradeSystemType.objects.all()
    serializer_class = serializers.GradeSystemTypeSerializer


class GradeSystemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = models.GradeSystem.objects.all()
    serializer_class = serializers.GradeSystemSerializer


class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer


class RouteCharacterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = models.RouteCharacter.objects.all()
    serializer_class = serializers.RouteCharacterSerializer


class LightViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = models.Light.objects.all()
    serializer_class = serializers.LightSerializer


class OrientationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = models.Orientation.objects.all()
    serializer_class = serializers.OrientationSerializer


class RockTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = models.RockType.objects.all()
    serializer_class = serializers.RockTypeSerializer


class AscentStyleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = models.AscentStyle.objects.all()
    serializer_class = serializers.AscentStyleSerializer