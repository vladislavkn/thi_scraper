import os


def get_spider_results_json(filename):
    with open(filename, "r") as f:
        results = f.read()
    # os.remove(filename)

    return results
