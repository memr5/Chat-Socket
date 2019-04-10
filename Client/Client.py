import socket
import select
import sys
from os import system

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = '10.0.2.15'
Port = 12345
s.connect((IP_address, Port))
inputStream_list = [sys.stdin, s]
flag = 0
while True:
    try:
        read_sockets, write_socket, error_socket = select.select(inputStream_list, [], [])

        for socks in read_sockets:
            if socks == s:
                message = socks.recv(1024).decode('utf-8')
                if message == "Do you want to find another stranger? (y or n) : ":
                    flag = 1
                print(message)
            elif socks == sys.stdin:
                message = input()
                s.send(message.encode('utf-8'))
            if message == 'n' and flag == 1:
                inputStream_list.remove(s)
                break
            elif message == 'y' and flag == 1:
                flag = 0
                _ = system('clear')
        if s not in inputStream_list:
            break
    except:
        break
s.close()
sys.exit()
