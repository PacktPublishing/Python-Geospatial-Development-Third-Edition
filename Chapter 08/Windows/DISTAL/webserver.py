# webserver.py

import http.server

address = ('', 8000)
handler = http.server.CGIHTTPRequestHandler
server = http.server.HTTPServer(address, handler)
server.serve_forever()

