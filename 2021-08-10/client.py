import socket
import argparse


analizador = argparse.ArgumentParser()
analizador.add_argument("-w", "--host", help="Host", type=str)
analizador.add_argument("-p", "--port", help="Puerto", type=int)
argumento = analizador.parse_args()

# create an object socket TCP/IP.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
HOST=argumento.host
PORT=argumento.port
serverAddress=((HOST,PORT))
sock.connect(serverAddress)

while True:
    message = input('##: ')
    sock.sendall(bytes(message,encoding='utf8'))
    data = sock.recv(1024)
    print(data.decode('utf-8'))

    if message == 'exit':
        break
print('closing socket')
sock.close()
