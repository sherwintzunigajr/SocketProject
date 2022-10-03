import socket
import sys

INPUT = sys.argv[1]
HEADER = 64
PORT = 4000
SERVER = "10.120.70.106"
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

if INPUT == "register":

    userName = "@" + sys.argv[2]
    ipv4 = sys.argv[3]
    portNum = sys.argv[4]

    def register(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    register(userName + '/' + ipv4 + '/' + portNum)

elif INPUT == "query":

    def query(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        print(client.recv(2048).decode(FORMAT))

    query('query')

elif INPUT == "follow":

    def follow(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        print(client.recv(2048).decode(FORMAT))

    query('follow')

    pass
elif INPUT == "drop":
    pass
elif INPUT == "exit"
    pass
else:
    print("INVALID COMMAND")
