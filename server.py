#!/usr/bin/env python
import SocketServer
import SimpleHTTPServer
import re
import para
from cluster import *

def execute(handler):
    found = re.search(
        '/execute/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)/',
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
        (dbhost, username, password, dbname, startTime, endTime, routeID) = found.group(1, 2, 3, 4, 5, 6, 7)
        # TODO: set into para

        para = Para()
        para.setDBProperty(dbhost, username, password, dbname)
        para.setTimeAndRoute(startTime, endTime, routeID)
        result, dataProperties = clusterMain(para)

        handler.wfile.write(str(result) + "|" + str(dataProperties))  # call sample function here


class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/execute/'):
            return execute(self)
        else:
            # serve files, and directory listings by following self.path from
            # current working directory
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


if '__main__' == __name__:
    PORT = 3111
    print "serving at port", PORT
    httpd = SocketServer.ThreadingTCPServer(('', PORT), CustomHandler)
    httpd.serve_forever()
