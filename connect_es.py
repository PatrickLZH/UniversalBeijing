from elasticsearch import Elasticsearch
import logging

logging.basicConfig(level=logging.DEBUG)

try:
    # 最简单的连接方式
    es = Elasticsearch("http://localhost:9200")
    print("ES Client created")
    print("Ping result:", es.ping())
    print("Info:", es.info())
except Exception as e:
    print("Connection failed:", e)
    import traceback
    traceback.print_exc()