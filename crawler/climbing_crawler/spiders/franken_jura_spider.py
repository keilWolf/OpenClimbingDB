import scrapy


class FrankenJuraSpider(scrapy.Spider):
    name = "franken_jura"
    allowed_domains = ["example.com"]
    start_urls = ["http://example.com/"]

    def parse(self, response):
        pass
