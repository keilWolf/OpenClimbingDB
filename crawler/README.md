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

You can test your spider interactivly like:

```bash
scrapy parse --spider=db_sandstein -c parse_summit -d 1 http://db-sandsteinklettern.gipfelbuch.de/weg.php\?gipfelid\=13035
```

## Crawl Data

Scrapy will save data as json lines

### DB Sandstein Klettern

http://db-sandsteinklettern.gipfelbuch.de/

e.g.
```bash
scrapy runspider ./climbing_crawler/spiders/db_sandstein_spider.py -a filter="Bulgarien" -o ./out/bulgarien.jsonl
```

**Possible Filters are the base countries:**

see: http://db-sandsteinklettern.gipfelbuch.de/adr.php

- Bulgarien
- China
- Deutschland
- Frankreich
- Griechenland
- Großbritannien
- Italien
- Jordanien
- Namibia
- Polen
- Portugal
- Russland
- Schweiz
- Slowakei
- Spanien
- Tschechische Republik
- Türkei
- Österreich
