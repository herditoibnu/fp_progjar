import mimetypes
import os
import subprocess


class Response:

    def __init__(self, path):
        self.path = '.' + path
        self.content = str(self.read_content(self.path))
        self.type = str(mimetypes.guess_type(self.path))
        self.header = str(self.build_header(self.content, self.type))

    def read_content(self, path):
        if os.path.isdir(path):
            if os.path.exists(path + '/index.html'):
                content = self.get_index_html(path)
            elif os.path.exists(path + '/index.php'):
                content = self.translate_index_php(path)
            elif path[-1:] != '/':
                content = self.refresh_directory(path)
            else:
                content = self.get_directory_content(path)
        elif os.path.isfile(path):
            if os.path.splitext(path)[1] == '.php':
                content = self.translate_php(path)
            else:
                content = self.get_file(path)
        else:
            content = self.get_404()
        return content

    def build_header(self, content, type):
        header = 'HTTP/1.1 200 OK\r\nContent-Type: ' + type + '; charset=UTF-8\r\nContent-Length:' \
                 + str(len(content)) + '\r\n\r\n'
        return header

    def get_file(self, path):
        f = open(path, 'rb')
        content = f.read()
        f.close()
        return content

    def translate_php(self, path):
        proc = subprocess.Popen("php " + path, shell=True, stdout=subprocess.PIPE)
        return proc.stdout.read()

    def get_index_html(self, path):
        return self.get_file(path + '/index.html')

    def translate_index_php(self, path):
        return self.translate_php(path + '/index.php')

    def get_404(self):
        return self.get_file('./404.html')

    def refresh_directory(self, path):
        return '<html><head> <meta http-equiv="refresh" content="0; url= ' + path[1:] + '/"/> </head><body></body></html>'

    def get_directory_content(self, path):
        datas = os.listdir('./'+path)
        list_file = ""
        for data in datas:
            if os.path.isfile('./'+path+data):
                list_file = list_file + '<p><a href = ' + data.replace(' ','%20') + '>' + data + '</a></p>'
            else:
                list_file = list_file + '<p><a href = ' + data.replace(' ','%20') + '/>' + data + '/</a></p>'
        content = '<html>' + list_file + '</html>'
        return content
