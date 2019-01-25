import json
import falcon

from storage import StingarES

es = StingarES()


class SensorResource(object):

    def on_get(self, req, resp):
        results = es.get_sensors()
        resp.body = str(results)
        resp.status = falcon.HTTP_200


class EventResource(object):

    def on_get(self, req, resp):
        results = es.get_events()
        resp.body = json.dumps(results, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class IndicatorResource(object):

    def on_get(self, req, resp):
        df = req.get_param('format') or ''

        results = es.get_indicators()
        if df == 'newline':
            resp.body = "\n".join(results)
        elif df == 'space':
            resp.body = " ".join(results)
        elif df == 'comma':
            resp.body = ",".join(results)
        else:
            resp.body = json.dumps(results, ensure_ascii=True)
        resp.status = falcon.HTTP_200


