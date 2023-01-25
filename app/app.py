import os
import elastic_transport
from elasticsearch import Elasticsearch
from queue import Queue
import json
import time
from scrapers.scraper import get_article


if __name__ == "__main__":
    url = os.getenv("ARTICLE_URL", "https://en.wikipedia.org/wiki/Special:Random")
    es_url = os.getenv("ES_URL", "http://127.0.0.1:9200")

    # Connect to Elasticsearch cluster
    es = Elasticsearch([es_url])

    # Create a queue to hold the data
    q = Queue()

    while True:

        # Check if the queue is empty
        if q.empty():
            print("Queue is empty, fetching new data...")

            # Add new data to the queue
            data = get_article(url)

            if data:
                q.put(data)
        else:
            # Get data from the queue
            data = q.get()

            try:
                # Send data to Elasticsearch
                res = es.index(
                    index="wikipedia", document=json.dumps(data), id=data["article_url"]
                )
                print(f"Data {res['result']} to Elasticsearch: \n", data)
            except elastic_transport.ConnectionError:
                print("Couldn't connected ES. Wait a bit, no need to rush")

            # Sleep for a while
            time.sleep(30)
