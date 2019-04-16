# Chat-Socket
## About it
This is a **Socket-Programming** based **Chat Application**. The main feature of this application is that it connects the user with another user having ``common interests``. This is a ``command line`` based application.
***
## Code
All of the code is in **_python_** and requires some what knowledge of ``socket-programming`` to understand it
* It will accept connection from clients and after accepting connection it will start a new thread to get user's interests.
```python
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12345
    server.bind(('', port))
    server.listen(100)
    global list_of_connection
    while True:
        try:
            conn, addr = server.accept()
            list_of_connection.append(conn)
            print("Got connection from : ", addr)
            start_new_thread(get_interest, (conn, addr))
        except:
            break
    server.close()
```
* To take user's ``interests`` and store it in a dictionary : 
```python
def get_interest(conn, addr):

    msg = "Enter your interests (comma separated): "
    conn.send(msg.encode('utf-8'))
    interests = str(conn.recv(1024).decode('utf-8')).lower()
    print("Interests of " + str(addr) + " is " + interests)
    interests = interests.split(',')
    interests_by_users[addr] = set(interests)

    for interest in interests:
        if interest in dict_of_interest:
            dict_of_interest[interest].append([conn, addr])
        else:
            dict_of_interest[interest] = [[conn, addr]]
    search_stranger(conn, addr)
```
* To search stranger with common interests : 
```python
def search_stranger(conn, addr):

    status[addr] = 0
    flag = 0
    conn.send("Searching.....".encode('utf-8'))
    sleep(1)
    for interest in interests_by_users[addr]:
        random.shuffle(dict_of_interest[interest])
        for connection, address in dict_of_interest[interest]:
            if connection != conn and connection in list_of_connection and status[address] == 0:
                common_interests = interests_by_users[addr].intersection(interests_by_users[address])
                conn.send(("You both like : " + str(common_interests)).encode('utf-8'))
                connection.send(("You both like : "+str(common_interests)).encode('utf-8'))
                status[addr] = 1
                status[address] = 1
                flag = 1
                start_new_thread(start_chatting, (conn, addr, connection, address))
                break
        if flag == 1:
            break
```
* To initiate conversation between two users with common interests :
```python
def start_chatting(conn1, addr1, conn2, addr2):
    try:
        sleep(1)
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
                    sleep(2)
                    start_new_thread(new_conversation, (conn1, addr1))
                    start_new_thread(new_conversation, (conn2, addr2))
                    input_stream_list.remove(conn1)
                    input_stream_list.remove(conn2)
                    break
            if len(input_stream_list) == 0:
                break
    except:
        remove(conn1, addr1)
        remove(conn2, addr2)
```
* To find new stranger after ending one conversation : 
```python
def new_conversation(conn, addr):
    try:
        conn.send("Do you want to find another stranger? (y or n) : ".encode('utf-8'))
        msg = conn.recv(1024)
        if msg.decode('utf-8').lower() == 'y':
            sleep(2)
            more_interests(conn, addr)
            start_new_thread(search_stranger, (conn, addr))
        else:
            remove(conn, addr)
    except:
        remove(conn, addr)
```        
* To add more interests after ending one conversation : 
```python
def more_interests(conn, addr):
    conn.send("Do you want to add more interests? (y or n) : ".encode('utf-8'))
    msg = conn.recv(1024)
    if msg.decode('utf-8').lower() == 'y':
        conn.send("Enter your interests (comma separated): ".encode('utf-8'))
        interests = str(conn.recv(1024).decode('utf-8')).lower().split(',')
        interests = set(interests)
        interests_by_users[addr] = interests_by_users[addr].union(interests)
        print("New interests of " + str(addr) + " " + str(interests_by_users[addr]))
        for interest in interests_by_users[addr]:
            if interest in dict_of_interest and [conn, addr] not in dict_of_interest[interest]:
                dict_of_interest[interest].append([conn, addr])
            elif interest not in dict_of_interest:
                dict_of_interest[interest] = [[conn, addr]]
```
* To remove and close connection from server:
```python
def remove(conn, addr):
    if conn in list_of_connection:
        list_of_connection.remove(conn)
        conn.close()
        print("Connection removed : ", addr)
    interests_by_users.pop(addr, None)
```
## Next goals
* Optimization of the code
* Option to remove unwanted interests after every conversation
* Connect a user with zero interests to another user having zero interests
* Connect a user with any random user with zero interests whenever there is no user having common interests
* Avoid connection with the same user with whom the user was connected before
## Contributors
* [Meet Ranoliya (@memr5)](https://github.com/memr5)
