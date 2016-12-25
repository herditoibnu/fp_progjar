import socket
#from bs4 import BeautifulSoup

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = ('10.181.1.201', 8000)
server_address = ('localhost', 50008)
client_socket.connect(server_address)

#request_header = 'GET / HTTP/1.1\r\nHost: 10.181.1.201\r\n\r\n'
# request_header = 'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n'

request_header_type = raw_input('input method: ')
# request_header_type = 'GET /'
request_header_path = raw_input('input path: ')
request_header_http = ' HTTP/1.1\r\nHost: localhost\r\n\r\n'
request_header_all = request_header_type + ' /' + request_header_path + request_header_http


if(request_header_type == 'POST'):
    argName = raw_input('input name: ')
    argEmail = raw_input('input email: ')
    request_header_all = request_header_all +  'name='+argName + '&email='+argEmail

print request_header_all
client_socket.send(request_header_all)

response = ''
recv = client_socket.recv(1024)
# soup = BeautifulSoup(recv)
# print soup.get_text()
print recv

client_socket.close()
