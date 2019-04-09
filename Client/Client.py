import socket
import select
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = '10.0.2.15'
Port = 12345
s.connect((IP_address, Port))
inputStream_list = [sys.stdin, s]

while True:

    read_sockets, write_socket, error_socket = select.select(inputStream_list, [], [])

    for socks in read_sockets:
        if socks == s:
            message = socks.recv(1024).decode('utf-8')
            print(message)
        else:
            message = input()
            s.send(message.encode('utf-8'))
        if message == 'bye':
            inputStream_list.remove(s)
            break
    if s not in inputStream_list:
        break

s.close()
