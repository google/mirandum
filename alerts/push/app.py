from tornado import websocket, web, ioloop
import json
import time

clients = []

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, key=None):
        self.key = key
        if self not in clients:
            clients.append(self)

    def on_close(self):
        if self in clients:
            clients.remove(self)

class ApiHandler(web.RequestHandler):

    @web.asynchronous
    def get(self, *args):
        self.finish()
        key = self.get_argument("key")
        print key
        print clients
        for c in clients:
            if c.key == key:
                c.write_message("now")

    @web.asynchronous
    def post(self):
        pass

app = web.Application([
    (r'/ws/([A-Za-z0-9]*)', SocketHandler),
    (r'/api', ApiHandler),
])

if __name__ == '__main__':
    app.listen(8765)
    ioloop.IOLoop.instance().start()
