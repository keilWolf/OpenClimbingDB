from django.core.management.base import BaseCommand
from crawler.climbing_crawler.spiders.db_sandstein_json_spider import (
    DBSandsteinJsonSpider,
)
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from crawler.climbing_crawler import settings as my_settings


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(DBSandsteinJsonSpider)
        process.start()
