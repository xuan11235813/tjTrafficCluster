#!/usr/bin/env python
import SocketServer
import SimpleHTTPServer
import re
import para


def set_database_connection(handler):
    found = re.search(
        '/setDatabaseConnection/(.*)/(.*)/(.*)/(.*)/',
        handler.path)
    if found is None:
        handler.send_response(400)
        handler.send_header('Content-type', 'text/plain')
        handler.end_headers()
        handler.wfile.write("Bad Request")
    else:
        handler.send_response(200)
        handler.send_header('Content-type', 'text/plain')
        handler.end_headers()
        handler.wfile.write("OK")  # call sample function here
        (dbhost, username, password, dbname) = found.group(1, 2, 3, 4)
        # TODO: set into para


def clustering(handler):
    found = re.search(
        '/setDatabaseConnection/(.*)/(.*)/(.*)/',
        handler.path)
    if found is None:
        handler.send_response(400)
        handler.send_header('Content-type', 'text/plain')
        handler.end_headers()
        handler.wfile.write("Bad Request")
    else:
        handler.send_response(200)
        handler.send_header('Content-type', 'text/plain')
        handler.end_headers()
        (startTime, endTime, routeID) = found.group(1, 2, 3)
        # TODO: set and write back to the handler
        handler.wfile.write("OK")  # call sample function here


class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/setDatabaseConnection/'):
            return set_database_connection(self)
        elif self.path.startswith('/clustering/'):
            return execute(self)
        else:
            # serve files, and directory listings by following self.path from
            # current working directory
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


if '__main__' == __name__:
    PORT = 3108
    print "serving at port", PORT
    httpd = SocketServer.ThreadingTCPServer(('', PORT), CustomHandler)
    httpd.serve_forever()
