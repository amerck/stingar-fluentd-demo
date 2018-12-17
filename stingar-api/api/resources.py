import json
from elasticsearch import Elasticsearch
import falcon

es = Elasticsearch([{'host': 'elasticsearch'}])


class EventResource(object):

    def on_get(self, req, resp):
        results = es.search(index="stingar-*")
        resp.body = json.dumps(results['hits']['hits'], ensure_ascii=False)
        resp.status = falcon.HTTP_200


class IndicatorResource(object):

    def on_get(self, req, resp):
        results = es.search(index="stingar-*", _source_include=["peerIP"])
        resp.body = json.dumps(results['hits']['hits'], ensure_ascii=True)
        resp.status = falcon.HTTP_200


class SensorResource(object):

    def on_get(self, req, resp):
        query = {
            "aggs": {
                "identifiers": {
                    "terms": {
                        "field": "identifier.keyword"
                    }
                }
            }
        }

        results = es.search(index="stingar-*", body=query)
        resp.body = json.dumps(results['aggregations'], ensure_ascii=True)
        resp.status = falcon.HTTP_200
