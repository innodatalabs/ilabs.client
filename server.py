from http.server import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self, *av, **kaw):
        print(self.path)
        print(self.headers)
        self.send_response(200, 'OK')
    
    def do_POST(self, *av, **kaw):
        print(av, kaw)

if __name__ == '__main__':
    httpd = HTTPServer( ('localhost', 8080), Handler)
    httpd.serve_forever()
