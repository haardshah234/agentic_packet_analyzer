
import json
import threading
import webbrowser

from pathlib import Path
from queue import Queue
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .generate_html import generate_html
from packet_analyzer.fetch_testcases import fetch_testcases

testcases_relative_filepath = "jsons/testcases.json"
project_root = Path(__file__).parent.parent
testcases_filepath = project_root / testcases_relative_filepath

def start_server(packet_definitions: list[dict]):

    testcase_queue = Queue()

    # Save testcases.json in the current working directory.

    html_page = generate_html(packet_definitions)

    class RequestHandler(BaseHTTPRequestHandler):

        def do_GET(self):

            if self.path != "/":
                self.send_error(404)
                return

            response = html_page.encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()

            self.wfile.write(response)

        def do_POST(self):

            if self.path != "/run":
                self.send_error(404)
                return

            try:

                content_length = int(self.headers.get("Content-Length", 0))
                request_body = self.rfile.read(content_length)

                testcase_data = json.loads(request_body.decode("utf-8"))

                if not isinstance(testcase_data, dict):
                    raise ValueError("Invalid testcase JSON structure.")

                # Save the JSON dictionary to testcases.json.
                testcases_filepath.write_text(
                    json.dumps(testcase_data, indent=4),
                    encoding="utf-8"
                )

                # Notify the analyzer that the file has been saved.
                testcase_queue.put(True)

                response = {
                    "success": True,
                    "message": "Testcases saved successfully."
                }

                response_body = json.dumps(response).encode("utf-8")

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response_body)))
                self.end_headers()

                self.wfile.write(response_body)

            except Exception as error:

                response_body = json.dumps({
                    "success": False,
                    "message": str(error)
                }).encode("utf-8")

                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response_body)))
                self.end_headers()

                self.wfile.write(response_body)

        def log_message(self, format, *args):
            pass

    server = ThreadingHTTPServer(
        ("127.0.0.1", 2304),
        RequestHandler
    )

    server_thread = threading.Thread(
        target=server.serve_forever,
        daemon=True
    )

    server_thread.start()

    webbrowser.open("http://127.0.0.1:2304")

    return server, testcase_queue


import json

def wait_for_testcase_submission(server, testcase_queue):

    try:
        print("Waiting for testcase submission...")
        print("If you accidentally closed the window, you can open the same form again in any browser by going to localhost:2304")

        testcase_queue.get()

        expected_testcases = fetch_testcases()

        print("Testcases loaded successfully!")
        return expected_testcases

    except KeyboardInterrupt:
        print("Stopped by user.")
        return None

    finally:
        server.shutdown()
        server.server_close()