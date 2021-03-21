from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters

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

    queryset = models.GradeSystemType.objects.all()
    serializer_class = serializers.GradeSystemTypeSerializer


class GradeSystemViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.GradeSystem.objects.all()
    serializer_class = serializers.GradeSystemSerializer


class GradeViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer


class RouteCharacterViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.RouteCharacter.objects.all()
    serializer_class = serializers.RouteCharacterSerializer


class LightViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.Light.objects.all()
    serializer_class = serializers.LightSerializer


class OrientationViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.Orientation.objects.all()
    serializer_class = serializers.OrientationSerializer


class RockTypeViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.RockType.objects.all()
    serializer_class = serializers.RockTypeSerializer


class AscentStyleViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.AscentStyle.objects.all()
    serializer_class = serializers.AscentStyleSerializer


class DiaryViewSet(viewsets.ModelViewSet):

    queryset = models.Diary.objects.all()
    serializer_class = serializers.DiarySerializer


class PersonViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer


class DiaryPersonViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.DiaryPerson.objects.all()
    serializer_class = serializers.DiaryPersonSerializer


class SectorViewSet(viewsets.ModelViewSet):

    queryset = models.Sector.objects.all()
    serializer_class = serializers.SectorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    @action(detail=False)
    def roots(self, request):
        """Return only the root sectors that do not have a parent."""
        roots = models.Sector.objects.filter(fk_sector=None)
        serializer = self.get_serializer(roots, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def get_childs(self, request, pk=None):
        parent_sector = self.get_object()
        child_sectors = models.Sector.objects.filter(fk_sector=parent_sector)
        serializer = self.get_serializer(child_sectors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def get_parents(self, request, pk=None):
        current_sector = self.get_object()
        parents = []
        parent = current_sector.fk_sector
        while parent:
            parents.append(parent)
            parent = parent.fk_sector
        serializer = self.get_serializer(parents, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def get_routes(self, request, pk=None):
        current_sector = self.get_object()
        routes = models.Route.objects.filter(fk_sector=current_sector)
        serializer = serializers.RouteSerializer(
            routes, many=True, context={"request": request}
        )
        return Response(serializer.data)


class RouteViewSet(viewsets.ModelViewSet):

    queryset = models.Route.objects.all()
    serializer_class = serializers.RouteSerializer


class RouteCharactersViewSet(viewsets.ModelViewSet):

    queryset = models.RouteCharacters.objects.all()
    serializer_class = serializers.RouteCharactersSerializer


class RouteGradesViewSet(viewsets.ModelViewSet):

    queryset = models.RouteGrades.objects.all()
    serializer_class = serializers.RouteGradesSerializer


class AscentViewSet(viewsets.ModelViewSet):

    queryset = models.Ascent.objects.all()
    serializer_class = serializers.AscentSerializer


class RopePartyViewSet(viewsets.ModelViewSet):

    queryset = models.RopeParty.objects.all()
    serializer_class = serializers.RopePartySerializer
