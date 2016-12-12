import socket
import select
import ConfigParser
import sys
import response as resp


config = ConfigParser.ConfigParser()
config.readfp(open(r'httpserver.conf'))
port_num = int(config.get('portList', 'port'))

server_address = ('localhost', port_num)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            else:
                # receive data from client, break when null received
                data = sock.recv(4096)
                if data:

                    request_header = data.split('\r\n')
                    request_file = request_header[0].split()[1].replace('%20',' ')
                    response = resp.Response(request_file)
                    sock.sendall(response.header + response.content)
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
