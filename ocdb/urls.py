from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ocdb import views

# Default router
router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)

# Create a router and register our viewsets with it.
# router.register(r'areas', views.AreaViewSet)
# router.register(r'summits', views.SummitViewSet)
# router.register(r'routes', views.RouteViewSet)
# router.register(r'climbers', views.ClimberViewSet)
# router.register(r'ascents', views.AscentViewSet)
# router.register(r'rope_party', views.AscentClimbersViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
