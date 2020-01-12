import http.server as server
import socketserver

parameters = {
    'PORT': 8080,
    'SERVER_ADDRESS': "127.0.0.1"
}


class SimpleServer(server.BaseHTTPRequestHandler):
    def do_GET(self):
        print('Path requested by client : ' + self.path)
        try:
            if self.path.endswith('.html'):
                f = open('.'+self.path)
                self.send_response(200)
                self.send_header('Content-type', 'text-html')
                self.end_headers()
                self.wfile.write(f.read().encode())
                f.close()
        except IOError:
            self.send_error(404, 'file not found')


if __name__ == '__main__':
    Handler = SimpleServer
    address = parameters['SERVER_ADDRESS']
    port = parameters['PORT']

    print('Webserver is starting...')
    httpd = socketserver.TCPServer((address, port), Handler)

    print('Webserver is running on ' + address + '/' + str(port) + '...')
    httpd.serve_forever()

