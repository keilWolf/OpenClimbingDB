from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ocdb import views

# Default router
router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"grade-system-types", views.GradeSystemTypeViewSet)
router.register(r"grade-systems", views.GradeSystemViewSet)
router.register(r"grades", views.GradeViewSet)

router.register(r"rock-types", views.RockTypeViewSet)
router.register(r"route-characters", views.RouteCharacterViewSet)
router.register(r"lights", views.LightViewSet)
router.register(r"orientations", views.OrientationViewSet)
router.register(r"ascent-styles", views.AscentStyleViewSet)

router.register(r"persons", views.PersonViewSet)
router.register(r"diaries", views.DiaryViewSet)
router.register(r"diary-person", views.DiaryPersonViewSet)
router.register(r"sectors", views.SectorViewSet)

router.register(r"routes", views.RouteViewSet)
router.register(r"routes-grades", views.RouteGradesViewSet)
router.register(r"characters-of_route", views.RouteCharactersViewSet)

router.register(r"ascents", views.AscentViewSet)
router.register(r"rope-parties", views.RopePartyViewSet)
router.register(r"first-ascentionists-of_route", views.FirstAscentionistOfRouteViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
