import socket
import select
from _thread import *

list_of_connection = []
dict_of_interest = {}


def start_chatting(conn1, conn2):
    conn1.send("You are Connected, Say hi!".encode('utf-8'))
    conn2.send("You are Connected, Say hi!".encode('utf-8'))
    input_stream_list = [conn1, conn2]
    while True:
        read_sockets, write_socket, error_socket = select.select(input_stream_list, [], [])
        for socks in read_sockets:
            if socks == conn2:
                msg = conn2.recv(1024)
                temp = "Stranger : " + msg.decode('utf-8')
                conn1.send(temp.encode('utf-8'))
            else:
                msg = conn1.recv(1024)
                temp = "Stranger : " + msg.decode('utf-8')
                conn2.send(temp.encode('utf-8'))
            if msg.decode('utf-8') == "bye":
                remove(conn1)
                remove(conn2)
                input_stream_list.remove(conn1)
                input_stream_list.remove(conn2)
                break
        if len(input_stream_list) == 0:
            break


def remove(conn):
    if conn in list_of_connection:
        list_of_connection.remove(conn)
        conn.close()


def get_interest(conn, addr):
    global dict_of_interest
    global list_of_connection
    msg = "Enter your interest : "
    conn.send(msg.encode('utf-8'))
    interest = str(conn.recv(1024).decode('utf-8')).lower()
    print("Interest of " + str(addr) + "is " + interest)
    if interest in dict_of_interest:
        flag = 0
        for conn2 in dict_of_interest[interest]:
            if conn2[1] != 1 and conn2[0] in list_of_connection:
                conn2[1] = 1
                flag = 1
                dict_of_interest[interest].append([conn, 1])
                start_new_thread(start_chatting, (conn, conn2[0]))
                break
        if flag == 0:
            dict_of_interest[interest].append([conn, 0])
    else:
        dict_of_interest[interest] = [[conn, 0]]


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12345
    server.bind(('10.0.2.15', port))
    server.listen(100)
    global list_of_connection
    while True:
        try:
            conn, addr = server.accept()
            list_of_connection.append(conn)
            print("Got connection from : ",addr)
            start_new_thread(get_interest, (conn, addr))
        except:
            break
    server.close()


main()
