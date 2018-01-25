import BaseHTTPServer
import os

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    page = '''\
    <html>
    <body>
    <p> {name}</p>
    </body>
    </html>
    '''
    #动态构建Web页面
    def do_GET(self):
        page = self.create_page()
        self.send_page(page)
    
    def create_page(self):
        value = {'name':'renjie'}
        page = self.page.format(**value)
        return page
    
    def send_page(self,page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)
        
           

        
        
        
if __name__ == '__main__':
    serverAddress = ('',8080)
    server = BaseHTTPServer.HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()