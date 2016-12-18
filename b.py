import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = ('10.181.1.201', 8000)
server_address = ('localhost', 50001)
client_socket.connect(server_address)

#request_header = 'GET / HTTP/1.1\r\nHost: 10.181.1.201\r\n\r\n'
request_header = 'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n'
client_socket.send(request_header)

response = ''
recv = client_socket.recv(1024)
print recv
client_socket.close()
