#encoding:utf-8
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
     
    '''
    #动态生成页面
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
    '''
    
    def do_GET(self):
        '''
        读取本地路径的page文件
        '''
        try:
            full_path = os.getcwd() + self.path
            if not os.path.exists(full_path):
                raise ServerException("'{0}' not found".format(self.path))
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
                
            else:
                raise ServerException("Unknown object'{0}'".format(self.path))
        except Exception as msg:
            self.handle_error(msg)
            
    def handle_file(self,full_path):
        try:
            with open(full_path,'rb') as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = "'{0}' can not be read:{1}".format(self.path,msg)
    
    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """
    def handle_error(self,msg):
        content = self.Error_Page.format(path = self.page,msg = msg)
        self.send_content(content,404)
        
    def send_content(self,content,status = 200):
        self.send_response(status)
        self.send_header("Content-type","text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)    
        
        
    
   
        
           

class ServerException(Exception):
    '''For internal error reporting.'''
    pass        
        
        
if __name__ == '__main__':
    serverAddress = ('',8080)
    server = BaseHTTPServer.HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()
    