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

# Client side gets inputs straight from the command line and sends prompts to the tracker, basically asking it based off user input

# REGISTER command
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

# QUERY command
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

# FOLLOW command
elif INPUT == "follow":

    userFollows = sys.argv[2]
    userFollowed = sys.argv[3]

    def follow(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    follow('follow/' + userFollows + ' ' + userFollowed)

# DROP command
elif INPUT == "drop":

    userDrop = sys.argv[2]
    userDropped = sys.argv[3]


    def drop(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    drop('drop/' + userDrop + ' ' + userDropped)

# TWEET command
elif INPUT == "tweet":

    tweeter = sys.argv[2]
    userTweet = sys.argv[3]

    def tweet(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    tweet('tweet/' + tweeter + ' ' + userTweet)

# TWEET PROPAGATION command
elif INPUT == 'getTweet':

    user = sys.argv[2]

    def getTweet(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        print(client.recv(2048).decode(FORMAT))

    getTweet('getTweet/' + user)

# EXIT command
elif INPUT == "exit":

    userExited = sys.argv[2]

    def exit(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    exit('exit/' + userExited)

# every other type of unacceptable input
else:
    print("INVALID COMMAND")
