import falcon
import resources

api = application = falcon.API()

events = resources.EventResource()
indicators = resources.IndicatorResource()

api.add_route('/events', events)
api.add_route('/indicators', indicators)
