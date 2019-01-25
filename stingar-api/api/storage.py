from elasticsearch import Elasticsearch
from elasticsearch_dsl import A, Search


class StingarES:

    def __init__(self, host='elasticsearch'):
        self.es = Elasticsearch([{'host': host}])

    def get_sensors(self):
        sensors = []
        s = Search(index="sensors", using=self.es)
        response = s.execute()
        for hit in response:
            sensors.append(hit.to_dict())
        return sensors

    def get_events(self):
        events = []
        s = Search(index="stingar-*", using=self.es)
        response = s.execute()
        for hit in response:
            events.append(hit.to_dict())
        return events

    def get_indicators(self):
        hits = []
        s = Search(index="stingar-*", using=self.es)
        a = A('terms', field='src_ip.keyword')
        s.aggs.bucket("indicators", a)
        response = s.execute()
        for bucket in response.aggregations.indicators.buckets:
            hits.append(bucket.key)
        return hits
