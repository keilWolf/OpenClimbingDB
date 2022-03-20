# Climbing Crawler

This projects aims in getting data about climbing routes from different websites around the world.

## Requirements

You need some virtualenv with `scrapy` installed.

https://scrapy.org/

## Development / Project Setup

_for detailed information see the scrapy documentation_

**Basic project structure**

```bash
scrapy startproject ClimbingCrawler
```

**Generate new Spiders**

```bash
scrapy genspider climbing_crawler example.com
```

## Interactive Testing

https://docs.scrapy.org/en/latest/topics/shell.html
https://docs.scrapy.org/en/latest/topics/commands.html

**Example**

```bash
scrapy parse http://db-sandsteinklettern.gipfelbuch.de/jsonwege.php\?app\=yacguide\&sektorid\=326 --spider=DBSandsteinJsonSpider -c parse_routes --meta='{"summit":"326"}'
```

## Crawl Data

```bash
scrapy crawl [SPIDER]
```

Will run the crawling and feed the data in the database.

| Spider                | Estimated Time To Fetch DB in min |
| --------------------- | --------------------------------- |
| DBSandsteinJsonSpider | 24                                |
| frankenjura           | 12                                |

You can stop when an exception is fired. Set the `CLOSESPIDER_ERRORCOUNT = 1` in the settings.py file.
