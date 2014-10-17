'''
Created on 17 Oct 2014

@author: Ed

Code to test the little printer by simulating the direct print api.

It will print any POST or GET request to the dummy URL to the console.
'''

import BaseHTTPServer

class LittlePrinterServer(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        print '{0}:{1}'.format(self.path,
                               self.command)
        self.send_response(200, 'OK')
    
    def do_GET(self):
        print '{0}:{1}'.format(self.path,
                               self.command)
        self.send_response(200, 'OK')
    
        
def run(server_class=BaseHTTPServer.HTTPServer,
        handler_class=LittlePrinterServer):
    server_address = ('', 8010)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

print 'Listening'
run()