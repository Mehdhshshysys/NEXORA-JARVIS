from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


HOST = "127.0.0.1"
PORT = 8000


WEB_DIR = Path(__file__).resolve().parent


class NEXORAHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            directory=str(WEB_DIR),
            **kwargs
        )

    def log_message(self, format, *args):
        print(
            f"[NEXORA WEB] {self.address_string()} - {format % args}"
        )


def start_server():

    server = ThreadingHTTPServer(
        (HOST, PORT),
        NEXORAHandler
    )

    print("=" * 40)
    print("NEXORA-JARVIS WEB SERVER")
    print("=" * 40)

    print(
        f"Server running at: http://{HOST}:{PORT}"
    )

    print(
        "Press CTRL+C to stop the server."
    )

    try:
        server.serve_forever()

    except KeyboardInterrupt:

        print(
            "\nNEXORA WEB SERVER STOPPED."
        )

    finally:

        server.server_close()


if __name__ == "__main__":
    start_server()
