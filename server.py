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
follower = {}
currTweet = ''
currTweeter = ''

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Tracker server setup
def handle_client(conn, addr):

    global currTweeter, currTweet
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            # Client side logic, if tracker receives certain keywords from the client, then it will perform the respected action

            # REGISTER command
            if msg.find('@') == 0:
                if msg in users:
                    print("FAILURE")
                    connected = False
                    break

                print(f"[{addr}] {msg}")
                users.append(msg)
                print("SUCCESS")
                print(users)

                follower[msg.split('/')[0]] = []

                print(follower)

            # QUERY command
            elif msg == 'query':
                sendUsers = ''

                for i in users:
                    sendUsers += '['
                    sendUsers += i
                    sendUsers += '] '

                conn.send(f"Registered Handles[{len(users)}] {sendUsers}".encode(FORMAT))

            # FOLLOW command
            elif msg.find('follow') != -1:

                followStr = msg[7:]

                user1 = followStr.split()[0]
                user2 = followStr.split()[1]

                # If no users are registered
                if not users:
                    print("FAILURE")
                    connected = False
                    break

                # Check to see if user1 is registered
                if not any(user1 in i for i in users):
                    print("FAILURE")
                    connected = False
                    break

                # Check to see if user2 is registered
                if not any(user2 in i for i in users):
                    print("FAILURE")
                    connected = False
                    break

                # Check to see if user is already following
                if any(user1 in i for i in follower[user2]):
                    print("FAILURE")
                    connected = False
                    break

                # Update follower list
                follower[user2].append(user1)
                print('SUCCESS')

                print(follower)

            # DROP command
            elif msg.find('drop') != -1:

                dropStr = msg[5:]

                user1 = dropStr.split()[0]
                user2 = dropStr.split()[1]

                # If no users are registered
                if not users:
                    print("FAILURE")
                    connected = False
                    break

                # Check to see if user1 is registered
                if not any(user1 in i for i in users):
                    print("FAILURE")
                    connected = False
                    break

                # Check to see if user2 is registered
                if not any(user2 in i for i in users):
                    print("FAILURE")
                    connected = False
                    break

                # Check to see if user is even following
                if not any(user1 in i for i in follower[user2]):
                    print("FAILURE")
                    connected = False
                    break

                # Update follower list
                follower[user2].remove(user1)
                print('SUCCESS')

                # Debug
                print(follower)

            # EXIT command
            elif msg.find('exit') != -1:

                userExited = msg[5:]

                # If no users are registered
                if not users:
                    print("FAILURE")
                    connected = False
                    break

                # Check to see if user is even registered
                if not any(userExited in i for i in users):
                    print("FAILURE")
                    connected = False
                    break

                # Remove from follower lists (values)
                for i in follower:
                    if any(userExited in j for j in follower[i]):
                        follower[i].remove(userExited)

                # Remove from follower list (key)
                del follower[userExited]

                # Remove from user list
                for i in users:
                    if i.find(userExited) != -1:
                        users.remove(i)

                print('exit-complete')
                print(users)
                print(follower)

            #TWEET command
            elif msg.find('tweet') != -1:

                currTweet = msg[6:]

                currTweeter = currTweet.split()[0]
                currTweet = "\"" + currTweet.split()[1] + "\""

                print('SUCCESS')

            # TWEET PROPAGATION command
            elif msg.find('getTweet') != -1:

                receiver = msg[9:]

                if any(receiver in j for j in follower[currTweeter]):
                    conn.send(currTweet.encode(FORMAT))
                else:
                    conn.send('No tweets at this time'.encode(FORMAT))
                    print("FAILURE")
                    connected = False
                    break

    # Close the client side signal
    conn.close()


# Start the server function
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# Start the server
print("[STARTING] server is starting...")
start()