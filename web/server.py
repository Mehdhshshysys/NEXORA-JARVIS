import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


HOST = "127.0.0.1"
PORT = 8000

WEB_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = WEB_DIR.parent

sys.path.insert(0, str(PROJECT_ROOT))

from main import build_agent


AGENT, MEMORY, VOICE = build_agent()


class NEXORAHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            directory=str(WEB_DIR),
            **kwargs
        )

    def log_message(self, format, *args):
        print(
            f"[NEXORA WEB] "
            f"{self.address_string()} - "
            f"{format % args}"
        )

    def send_json(self, data, status=200):

        response = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(response))
        )

        self.end_headers()

        self.wfile.write(response)

    def do_GET(self):

        path = urlparse(self.path).path

        if path == "/api/status":

            self.send_json({
                "success": True,
                "status": "online",
                "name": "NEXORA-JARVIS"
            })

            return

        if path == "/":

            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):

        path = urlparse(self.path).path

        if path != "/api/command":

            self.send_json(
                {
                    "success": False,
                    "error": "مسیر API پیدا نشد."
                },
                404
            )

            return

        try:

            content_length = int(
                self.headers.get(
                    "Content-Length",
                    "0"
                )
            )

            if content_length <= 0:

                self.send_json(
                    {
                        "success": False,
                        "error": "دستوری دریافت نشد."
                    },
                    400
                )

                return

            if content_length > 10000:

                self.send_json(
                    {
                        "success": False,
                        "error": "درخواست بیش از حد بزرگ است."
                    },
                    413
                )

                return

            body = self.rfile.read(
                content_length
            )

            data = json.loads(
                body.decode("utf-8")
            )

            command = str(
                data.get("command", "")
            ).strip()

            if not command:

                self.send_json(
                    {
                        "success": False,
                        "error": "دستور خالی است."
                    },
                    400
                )

                return

            print(
                f"[NEXORA COMMAND] {command}"
            )

            result = AGENT.execute(
                command
            )

            self.send_json({
                "success": True,
                "response": str(result)
            })

        except json.JSONDecodeError:

            self.send_json(
                {
                    "success": False,
                    "error": "داده JSON معتبر نیست."
                },
                400
            )

        except Exception as error:

            print(
                f"[NEXORA ERROR] {error}"
            )

            self.send_json(
                {
                    "success": False,
                    "error": "خطا در اجرای دستور."
                },
                500
            )


def start_server():

    server = ThreadingHTTPServer(
        (HOST, PORT),
        NEXORAHandler
    )

    print("=" * 45)
    print("        NEXORA-JARVIS WEB SERVER")
    print("=" * 45)

    print(
        f"Web: http://{HOST}:{PORT}"
    )

    print(
        "NEXORA Agent: ONLINE"
    )

    print(
        "Press CTRL+C to stop."
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
