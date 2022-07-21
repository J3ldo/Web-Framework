import socket
import threading
import shutil, os

def nothing():
    return

class WebApp:
    def __init__(self):
        self.routes = {}
        self.before_req = nothing
        self.after_req = nothing
        self.handled_errors = {}


    def route(self, *args):
        def inner(func):
            if len(args) <= 0:
                raise Exception('You need to pass the route of the url.')
            if args[0][0] != '/':
                raise Exception("Routes need to start with a /")
            elif self.routes.get(args[0]) is not None:
                raise Exception("Route already exists")

            fill_in = False
            text = ""
            _id = 0
            route_name = args[0]
            for i in list(args[0]):
                if i == '<':
                    fill_in = True
                    _id += 1

                elif i == ">" and fill_in:
                    text += i
                    fill_in = False
                    route_name = route_name.replace(text, "<>")
                    text = ""


                if fill_in:
                    text += i


            self.routes[route_name] = {'func': func, 'methods': args[1] if len(args) > 1 else ['GET'], 'special_list': [], 'has_special': False}

            fill_in = False
            text = ""
            _id = 0
            for i in list(args[0]):
                if i == '<':
                    fill_in = True
                    _id += 1
                    continue

                elif i == ">" and fill_in:
                    fill_in = False
                    self.routes[route_name]['special'][text] = {'text': text, 'id': _id}
                    self.routes[route_name]['special_list'].append(text)
                    self.routes[route_name]['has_special'] = True
                    text = ""
                    continue

                elif fill_in:
                    text += i


        return inner


    def get(self, *args):
        def inner(func):
            self.route(args[0], ["GET"])(func)


        return inner

    def post(self, *args):
        def inner(func):
            self.route(args[0], ["POST"])(func)

        return inner

    def error_handler(self, error:int):
        def inner(func):
            self.handled_errors[error] = func


        return inner

    def load_blueprint(self, blueprint):
        for route in blueprint.routes:
            if route in self.routes.keys():
                raise Exception("Duplicate route.")
            self.routes[route] = blueprint.routes[route]


    #print(socket.gethostbyname(socket.gethostname()))

    def before_request(self, func):
        self.before_req = func

    def after_request(self, func):
        self.after_req = func

    def start(self, ip, port, debug=False):
        from .listener import listen
        shutil.rmtree(__file__[:-11] + "/templates")
        os.mkdir(__file__[:-11] + "/templates")


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PORT = port  # 80
        IP = ip  # "0.0.0.0"
        s.bind((IP, PORT))
        print(f"Listening on: http://{socket.gethostbyname(socket.gethostname() if IP == '0.0.0.0' else IP)}:{PORT}")

        s.listen()
        while True:
            clientdata, addr = s.accept()

            thread = threading.Thread(target=listen, args=(self, clientdata, addr, debug,))
            thread.start()