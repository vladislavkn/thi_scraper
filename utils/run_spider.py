import os
import logging
from scrapy.crawler import CrawlerProcess

logging.getLogger("scrapy").propagate = False


def run_spider(spider, filename):
    if os.path.exists(filename):
        os.remove(filename)

    process = CrawlerProcess(
        settings={
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.1234.567 Safari/537.36",
            "FEED_FORMAT": "json",
            "FEED_URI": filename,
            "LOG_ENABLED": False,
        }
    )

    process.crawl(spider)
    process.start()
