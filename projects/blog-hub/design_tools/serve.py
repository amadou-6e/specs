"""Static file server with no-cache headers — run from .spec/design_tools/layout/"""
import http.server, sys

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def log_message(self, fmt, *args):
        pass  # silence request log

port = int(sys.argv[1]) if len(sys.argv) > 1 else 9323
http.server.test(HandlerClass=NoCacheHandler, port=port, bind='localhost')
