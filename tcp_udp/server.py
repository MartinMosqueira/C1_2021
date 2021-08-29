import socket
import argparse


analizador = argparse.ArgumentParser()
analizador.add_argument("-p", help="Port", type=int)
analizador.add_argument("-t", help="package transport", type=str)
analizador.add_argument("-f", help="Save file", type=str)
argumento = analizador.parse_args()

def tcp_server(host,port):
    objectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dataServer=((host,port))
    objectSocket.bind(dataServer)
    objectSocket.listen(1)
    print('-------- TCP protocol --------')
 
    while True:
        print('waiting for a connection')
        connection, client_address = objectSocket.accept()

        try:
            print('connection from ', client_address)
            while True:
                data = connection.recv(1024)
                if not data:
                    print('no data from', client_address)
                    break
                file.write(data.decode('utf-8')+'\n')

        finally:
            file.close()
            connection.close()

def udp_server(host, port):
    objectSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dataServer=((host,port))
    objectSocket.bind(dataServer)
    print('-------- UDP protocol --------')

    while True:
        print('waiting for a connection')
        data_client, client_address = objectSocket.recvfrom(1024)
        print('connection from ', client_address)
        file.write(data_client.decode('utf-8')+'\n')

    file.close()
    clientsocket.close()

if __name__ == "__main__":

    HOST=''
    PORT=argumento.p
    file=open(argumento.f, 'a')

    if argumento.t == 'tcp':
        tcp_server(HOST, PORT)
    elif argumento.t == 'udp':
        udp_server(HOST, PORT)
    