import requests


def send_json(data, url):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        raise Exception("Reuest failed with status code " + response.status_code)
