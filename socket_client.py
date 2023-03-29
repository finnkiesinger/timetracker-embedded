import socketio


class WebsocketClient:
    io = socketio.Client()

    def __init__(self, url=None):
        self.url = url
        self.connected = False

    def connect(self, url=None):
        conn = url or self.url
        if conn is None:
            raise Exception(
                "URL has to be passed to this function or the constructor")

        self.io.connect(conn)
        self.connected = True

    def add_callback(self, event, callback):
        if self.connected:
            raise Exception(
                "Callbacks have to be added before a connection to the server is established")
        self.io.on(event, handler=callback)

    def emit(self, event, message):
        self.io.emit(event, message)


def handle_scan_result(message):
    print(message)


