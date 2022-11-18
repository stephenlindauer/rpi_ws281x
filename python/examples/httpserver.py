from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

hostName = "0.0.0.0"
serverPort = 8080


class RequestHandler(BaseHTTPRequestHandler):
    def render(self, filename):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            fin = open('%s/views/%s.html' % (dir_path, filename))
            contents = fin.read()
            fin.close()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(contents, "utf-8"))
        except FileNotFoundError as e:
            self.render("404")
        except Exception as e:
            self.render("500")

    def do_GET(self):
        print("do_get")

        if (self.path == "/"):
            self.handleIndex()
        elif (self.path == "/preview"):
            self.render("preview")
        elif (self.path.startswith("/api/")):
            self.handleAPIRequest()
        else:
            self.handle404()

    def handleIndex(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(
            bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def handleAPIRequest(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        (_, api, endpoint, type) = self.path.split("/")
        if (endpoint == 'animation'):
            self.handleAnimation(type)
        self.wfile.write(
            bytes(json.dumps({"status": "OK"}), "utf-8"))

    def handleAnimation(self, animationType):
        system.setAnimation(animationType)

    def handle404(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes("<html><head><title>404</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Page not found</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


class HTTPServerWrapper:
    def start(self):
        webServer = HTTPServer((hostName, serverPort), RequestHandler)
        print("Webserver started http://%s:%s" % (hostName, serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")
