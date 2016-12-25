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
    argNumber = int(raw_input('number of arguments: '))
    argv = ''
    for i in range(1,argNumber+1):
        arg = raw_input('argument ' + str(i) + ': ')
        argv += '&arg' + str(i) + '=' + arg
    request_header_all = request_header_all + argv[1:]

print request_header_all
client_socket.send(request_header_all)

response = ''
recv = client_socket.recv(1024)

cut = recv.split("\r\n");

if request_header_type == "GET" or request_header_type == "POST":
	#print recv
	type_file = cut[1]
	try:
		type_file = type_file.split("'")[1]
	except Exception:
		type_file = "text/"

	sizefile = cut[2]
	sizefile = sizefile.split("Content-Length:")[1]
	buff = int(sizefile)
	print recv
	if type_file[:5] != "text/":
		fname = request_header_path.split("/")[-1]
		filename = "Downloads/"+ fname
		save = open(filename,"w+")
		while buff > 0:
			isi = client_socket.recv(1024)
			save.write(isi)
			buff-=1024
		print("data downloaded")
		save.close()
	else:
		isi = client_socket.recv(1024)
		print isi