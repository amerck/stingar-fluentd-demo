import falcon
import resources

api = application = falcon.API()

events = resources.EventResource()
indicators = resources.IndicatorResource()
sensors = resources.SensorResource()

api.add_route('/api/v1/events', events)
api.add_route('/api/v1/indicators', indicators)
api.add_route('/api/v1/sensors', sensors)
