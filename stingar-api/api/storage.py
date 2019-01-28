import datetime

from elasticsearch import Elasticsearch
from elasticsearch_dsl import A, Search


class StingarES:

    def __init__(self, host='elasticsearch'):
        self.es = Elasticsearch([{'host': host}])

    def get_sensors(self, **kwargs):
        sensors = []
        s = Search(index="sensors", using=self.es)

        # Build filters from kwargs
        for k, v in kwargs.items():
            s = s.filter('term', **{k: v})

        response = s.execute()
        for hit in response:
            sensors.append(hit.to_dict())
        return sensors

    def get_events(self, from_date=None, to_date=None, *args, **kwargs):
        events = []
        s = Search(index="stingar-*", using=self.es)

        # Set timestamp filter for events
        if from_date:
            from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d_%H:%M:%S")
        if to_date:
            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d_%H:%M:%S")
        s = s.filter('range', start_time={'gte': from_date, 'lte': to_date})

        # Build filters from kwargs
        for k, v in kwargs.items():
            s = s.filter('terms', **{k: v})

        response = s.execute()
        for hit in response:
            events.append(hit.to_dict())
        return events

    def get_indicators(self):
        hits = []
        s = Search(index="stingar-*", using=self.es)

        # Aggregate on src_ip
        a = A('terms', field='src_ip.keyword')
        s.aggs.bucket("indicators", a)

        response = s.execute()
        for bucket in response.aggregations.indicators.buckets:
            hits.append(bucket.key)
        return hits
