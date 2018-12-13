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

