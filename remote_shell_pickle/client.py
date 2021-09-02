import socket
import argparse
import pickle
import threading


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
    message = input('user@'+str(threading.get_ident())+':~$: ')
    pickleMessage = pickle.dumps(message)
    #Send data to the server.
    sock.sendall(pickleMessage)
    #Receive data the server.
    data = sock.recv(1024)
    pickleReceive=pickle.loads(data)
    print(pickleReceive)

    if message == 'exit':
        break
print('closing socket')
sock.close()
