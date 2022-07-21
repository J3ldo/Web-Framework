
class Blueprint:
    def __init__(self):
        self.routes = {}

    def route(self, *args):
        def inner(func):
            if len(args) <= 0:
                raise Exception('You need to pass the route of the url.')
            elif self.routes.get(args[0]) is not None:
                raise Exception("Route already exists")

            self.routes[args[0]] = {'func': func, 'methods': args[1] if len(args) > 1 else ['GET']}

        return inner
