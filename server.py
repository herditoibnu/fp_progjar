#!/usr/bin/env python 

""" 
An echo server that uses threads to handle multiple clients at a time. 
Entering any line of input at the terminal will exit the server. 
""" 

import select 
import socket 
import sys 
import threading
import mimetypes
import os
import subprocess


class Response:
    def __init__(self, path):
        self.path = '.' + path

    def start(self):
        self.content = str(self.read_content(self.path))
        self.file_type = str(mimetypes.guess_type(self.path))
        self.header = str(self.build_header(self.content, self.file_type))

    def read_content(self, path):
        if os.path.isdir(path):
            if path == './dilarang/':
                content = self.get_403()
                self.response_type = '403'
            elif os.path.exists(path + '/index.html'):
                content = self.get_index_html(path)
                self.response_type = '200'
            elif os.path.exists(path + '/index.php'):
                content = self.translate_index_php(path)
                self.response_type = '200'
            elif path[-1:] != '/':
                content = self.refresh_directory(path)
                self.response_type = '200'
            else:
                content = self.get_directory_content(path)
                self.response_type = '200'
        elif os.path.isfile(path):
            if path == './dipindah.html':
                content = self.get_301()
                self.response_type = '301'
            elif os.path.splitext(path)[1] == '.php':
                content = self.translate_php(path)
                self.response_type = '200'
            else:
                content = self.get_file(path)
                self.response_type = '200'
        else:
            content = self.get_404()
            self.response_type = '404'
        return content

    def build_header(self, content, file_type):
        if self.response_type == '200':
            header = 'HTTP/1.1 200 OK\r\nContent-Type: ' + file_type + '; charset=UTF-8\r\nContent-Length:' \
                     + str(len(content)) + '\r\n\r\n'
        elif self.response_type == '301':
            header = 'HTTP/1.1 301 Moved Permanently\r\nContent-Type: ' + file_type + '; charset=UTF-8\r\nContent-Length:' \
                     + str(len(content)) + '\r\n\r\n'
        elif self.response_type == '403':
            header = 'HTTP/1.1 403 Forbidden\r\nContent-Type: ' + file_type + '; charset=UTF-8\r\nContent-Length:' \
                     + str(len(content)) + '\r\n\r\n'
        elif self.response_type == '404':
            header = 'HTTP/1.1 404 Not Found\r\nContent-Type: ' + file_type + '; charset=UTF-8\r\nContent-Length:' \
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

    def get_301(self):
        return self.get_file('./kepindah.html')

    def get_403(self):
        return self.get_file('./403.html')

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

class PostResponse(Response):

    def set(self, argv):
        self.argv = ''
        argv = argv.split('&')
        print argv
        for i in range(len(argv)):
            argv[i] = argv[i].split('=')[1]
            self.argv += ' ' + argv[i]

    def translate_php(self, path):
        proc = subprocess.Popen("php " + path + self.argv, shell=True, stdout=subprocess.PIPE)
        return proc.stdout.read()


class Server: 
    def __init__(self): 
        self.host = ''
        self.port = 50008
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
        self.open_socket()
        input = [self.server,sys.stdin]
        running = 1
        while running:
            try:
                inputready,outputready,exceptready = select.select(input,[],[])

                for s in inputready:

                    if s == self.server:
                        # handle the server socket
                        c = Client(self.server.accept())
                        c.start()
                        self.threads.append(c)

                    elif s == sys.stdin:
                        # handle standard input
                        junk = sys.stdin.readline()
                        running = 0
            except KeyboardInterrupt:
                print '>> Shut down server...'
                running = 0
        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            if data:
                request_header = data.split('\r\n')
                request_file = request_header[0].split()[1].replace('%20', ' ')
                if data[:3] == 'GET':
                    response = Response(request_file)
                    response.start()
                    self.client.sendall(response.header + response.content)
                elif data[:4] == 'HEAD':
                    response = Response(request_file)
                    response.start()
                    self.client.sendall(response.header)
                elif data[:4] == 'POST':
                    argv = request_header[-1]
                    response = PostResponse(request_file)
                    response.set(argv)
                    response.start()
                    self.client.sendall(response.content)
                else:
                    self.client.sendall('Invalid method')

            else:
                self.client.close()
                s.threads.remove(self)
                running = 0

if __name__ == "__main__": 
    s = Server() 
    s.run()
