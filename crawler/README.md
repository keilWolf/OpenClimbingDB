# Climbing Crawler

This projects aims in getting data about climbing routes from different websites around the world.

## Requirements

You need some virtualenv with `scrapy` installed.

https://scrapy.org/

## Development / Project Setup

*for detailed information see the scrapy documentation*

**Basic project structure**

```bash
scrapy startproject ClimbingCrawler
```

**Generate new Spiders**

```bash
scrapy genspider climbing_crawler example.com
```

## Interactive Testing

> Currently not working, because of import problems

You can test your spider interactivly like:

```bash
scrapy parse --spider=db_sandstein -c parse_summit -d 1 http://db-sandsteinklettern.gipfelbuch.de/weg.php\?gipfelid\=13035
```


## Crawl Data - Django Integration

```bash
python manage.py crawl
```

Will run the crawling and feed the data in the database.