import falcon
import auth
import resources

api = application = falcon.API(middleware=[auth.AuthMiddleware()])

events = resources.EventResource()
indicators = resources.IndicatorResource()
sensors = resources.Sensors()
sensor = resources.Sensor()

api.add_route('/api/v1/events', events)
api.add_route('/api/v1/indicators', indicators)
api.add_route('/api/v1/sensors', sensors)
api.add_route('/api/v1/sensors/{ident}', sensor)
