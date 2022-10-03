import socket
import threading
import sys

HEADER = 64
PORT = int(sys.argv[1])
SERVER = "10.120.70.106"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
users = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg.find('@') != -1:
                if msg in users:
                    print("FAILURE")
                    connected = False
                    break

                print(f"[{addr}] {msg}")
                users.append(msg)
                print("SUCCESS")
                print(users)
            elif msg == 'query':
                sendUsers = ''

                for i in users:
                    sendUsers += '['
                    sendUsers += i
                    sendUsers += '] '

                conn.send(f"Registered Handles[{len(users)}] {sendUsers}".encode(FORMAT))

            elif msg == 'follow':


    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("[STARTING] server is starting...")
start()