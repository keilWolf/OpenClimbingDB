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

https://docs.scrapy.org/en/latest/topics/shell.html
https://docs.scrapy.org/en/latest/topics/commands.html


## Crawl Data

```bash
scrapy crawl [SPIDER]
```

Will run the crawling and feed the data in the database.

| Spider       | Estimated Time To Fetch DB in min |
| ------------ | --------------------------------- |
| db_sandstein | 5                                 |
| frankenjura  | 12                                |
