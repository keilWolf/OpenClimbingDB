# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from ocdb.models import Sector, Route, RouteGrades


class SectorItem(DjangoItem):
    django_model = Sector


class RouteItem(DjangoItem):
    django_model = Route


class RouteGradeItem(DjangoItem):
    django_model = RouteGrades
