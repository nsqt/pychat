
import select, socket, sys
import netsock_util
from netsock_util import Room, Hall, Player

READ_BUFFER = 4096

if len(sys.argv) < 2:
    print('Usage: python3 client.py [hostname]', file = sys.stderr)
    sys.exit(1)

else:
    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_connection.connect((sys.argv[1], netsock_util.PORT))


def prompt():
    print('$>', end=' ', flush=True)

print('Connected to Server\n')
msg_prefix = ' '

socket_list = [sys.stdin, server_connection]

while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        if s is server_connection: #Incoming Chat Message
            msg = s.recv(READ_BUFFER)
            if not msg:
                print('Server Down!')
                sys.exit(2)
            else:
                if msg == netsock_util.QUIT_STRING.encode():
                    sys.stdout.write('Bye\n')
                    sys.exit(2)
                else:
                    sys.stdout.write(msg.decode())
                    if 'Please tell us your name' in msg.decode():
                        msg_prefix = 'name: ' # identify name
                    else:
                        msf_prefix = ''
                    prompt()
        else:
            msg = msg_prefix + sys.stdin.readline()
            server_connection.sendall(msg.encode())