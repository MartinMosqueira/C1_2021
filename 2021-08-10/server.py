#Escriba un programa cliente/servidor en python que permita ejecutar comandos GNU/Linux en una
#computadora remota.
#Técnicamente, se deberá ejecutar un código servidor en un equipo “administrado”, y programar
#un cliente (administrador) que permita conectarse al servidor mediante sockets STREAM.
#El cliente deberá darle al usuario un prompt en el que pueda ejecutar comandos de la shell.
#Esos comandos serán enviados al servidor, el servidor los ejecutará, y retornará al cliente:

#la salida estándar resultante de la ejecución del comando
#la salida de error resultante de la ejecución del comando.
#El cliente mostrará en su consola local el resultado de ejecución del comando remoto, ya sea 
#que se haya realizado correctamente o no, anteponiendo un OK o un ERROR según corresponda.

#Ejemplo de ejecución del cliente (la salida de los comandos corresponden a la ejecución en el
#equipo remoto.

#diego@cryptos$ python3 ejecutor_cliente.py
#> pwd
#OK
#/home/diego
#> ls -l /home
#OK
#drwxr-xr-x 158 diego diego 20480 May 26 18:57 diego
#drwx------   2 root  root  16384 May 28  2014 lost+found
#drwxr-xr-x   6 andy  andy   4096 Jun  4  2015 user
#> ls /cualquiera
#ERROR
#ls: cannot access '/cualquiera': No such file or directory
#>
#Agregue en el cliente la opción “-l <file>” para permitirle al usuario almacenar un log de toda la sesión (comandos ejecutados y su fecha/hora).

import socket
import subprocess
import argparse
import logging


analizador = argparse.ArgumentParser()
analizador.add_argument("-w", "--host", help="Host", type=str)
analizador.add_argument("-p", "--port", help="Port", type=int)
analizador.add_argument("-l", "--file", help="Save log file", type=str)
argumento = analizador.parse_args()

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

    try:
        print('connection from ', client_address)
        logging.debug('connection from '+str(client_address))
        while True:
            data = connection.recv(1024)
            if not data:
                print('no data from', client_address)
                logging.warning('no data from '+str(client_address))
                break

            print('received: ',data.decode('utf-8'))
            logging.debug(data.decode('utf-8'))
            data=data.split()
            command=subprocess.run(data, capture_output=True,shell=True)
            if command.returncode == 0:
                print('sending data back to the client')
                logging.debug(str(command.stdout,'utf-8'))
                stdout=str(command.stdout,'utf-8')
                connection.sendall(bytes('OK\n'+stdout,'utf-8'))
            else:
                logging.warning(str(command.stderr,'utf-8'))
                stderr=str(command.stderr,'utf-8')
                connection.sendall(bytes('ERROR\n'+stderr,'utf-8'))

    finally:
        # Clean up the connection
        connection.close()
