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
    
    '''
    # 读取本地路径的page文件
    def do_GET(self):
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
    '''
    
    #动态查找对应的处理程序
    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path
            for case in self.Cases:
                handler = case()
                if handler.test(self):
                    handler.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)
    
    
    
    Cases = [case_no_file(),
             case_existing_file(),
             case_directory_index_file(),
             case_always_fail()]
    
    
        
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
    

class case_existing_file(object):
    def test(self,handler):
        return not os.path.exists(handler.full_path)
    def act(self,handler):
        raise ServerException("'{0}' not found".format(handler.path))
class case_no_file(object):
    def test(self, handler):
        return os.path.isfile(handler.full_path)
    def act(self, handler):
        handler.handle_file(handler.full_path)
class case_always_fail(object):
    '''Base case if nothing else worked.'''
    def test(self, handler):
        return True
    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))
        

    