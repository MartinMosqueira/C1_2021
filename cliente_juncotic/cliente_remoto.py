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

questions = ['hello|','email|','key|','out|']
for question in questions:
    error=True
    while error == True:
        value=input(question)
        result=question+value
        if question=='out|':
            result=value
        #Send data to the server.
        sock.sendall(bytes(result,encoding='utf8'))
        #Receive data the server.
        data = sock.recv(1024)
        print(data.decode('utf-8'))
        if data.decode('utf-8') == '200':
            error=False
            
print('closing socket')
sock.close()
