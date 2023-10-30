import requests
from scrapy.crawler import CrawlerProcess
from spiders.wiki_spider import WikiSpider


def run_spider_and_collect_results():
    process = CrawlerProcess(
        settings={
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.1234.567 Safari/537.36",
            "FEED_FORMAT": "json",
            "FEED_URI": "output.json",
        }
    )

    process.crawl(WikiSpider)

    process.start()

    with open("output.json", "r") as f:
        results = f.read()
    return results


def send_data(data):
    payload = {"results": data}
    headers = {"Content-Type": "application/json"}

    response = requests.post("localhost:5000", json=payload, headers=headers)

    return response.status_code


if __name__ == "__main__":
    print("Starting spider...")
    spider_results = run_spider_and_collect_results()

    print("Data collected. Sending data...")
    status_code = send_data(spider_results)

    if status_code == 200:
        print("Data sent successful")
    else:
        print(f"HTTP-request failed with status code {status_code}")