#Reescribir el ejercicio de remote_shell de modo que permita recibir consultas desde varios clientes
#remotos en forma simultánea. Justifique el uso del mecanismo de concurrencia/paralelismo utilizado.

import socket
import subprocess
import argparse
import logging
import threading

analizador = argparse.ArgumentParser()
analizador.add_argument("-w", "--host", help="Host", type=str)
analizador.add_argument("-p", "--port", help="Port", type=int)
analizador.add_argument("-l", "--file", help="Save log file", type=str)
argumento = analizador.parse_args()

def thread_server(clientsocket,addr):
    try:
        print('connection from ', addr)
        logging.debug('connection from '+str(addr))
        while True:
            data = clientsocket.recv(1024)
            if not data:
                print('no data from', addr)
                logging.warning('no data from '+str(addr))
                break

            print('received: ',data.decode('utf-8'))
            logging.debug(data.decode('utf-8'))
            data=data.split()
            command=subprocess.run(data, capture_output=True,shell=True)
            if command.returncode == 0:
                print('sending data back to the client')
                logging.debug(str(command.stdout,'utf-8'))
                stdout=str(command.stdout,'utf-8')
                clientsocket.sendall(bytes('OK\n'+stdout,'utf-8'))
            else:
                logging.warning(str(command.stderr,'utf-8'))
                stderr=str(command.stderr,'utf-8')
                clientsocket.sendall(bytes('ERROR\n'+stderr,'utf-8'))

    finally:
        # Clean up the connection
        clientsocket.close()

logging.basicConfig(filename=argumento.file, filemode='w',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# create an object socket TCP/IP.
objectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Associate the socket with the port address.
HOST=argumento.host
PORT=argumento.port
dataServer=((HOST,PORT))
objectSocket.bind(dataServer)
# Number to connections. 
objectSocket.listen(1)

while True:
    print('waiting for a connection')
    connection, client_address = objectSocket.accept()
    th=threading.Thread(target=thread_server, args=(connection, client_address,))
    th.start()
