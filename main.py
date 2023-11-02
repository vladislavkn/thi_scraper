from spiders.wiki_spider import WikiSpider
import os
from utils.send_json import send_json
from utils.run_spider import run_spider
from utils.get_spider_results_json import get_spider_results_json

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.realpath(__file__))
    result_filename = os.path.join(current_directory, "results.json")

    print("Starting spider...")
    run_spider(WikiSpider, result_filename)
    print("Getting spider results...")
    spider_results = get_spider_results_json(result_filename)

    print("Sending results...")
    try:
        send_json(spider_results, 5000)
        print("Data sent successful")
    except Exception as exception:
        print(exception)
