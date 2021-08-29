import socket
import argparse


analizador = argparse.ArgumentParser()
analizador.add_argument("-w", "--host", help="Host", type=str)
analizador.add_argument("-p", "--port", help="Port", type=int)
analizador.add_argument("-t", "--transport", help="package transport", type=str)
analizador.add_argument("-l", "--file", help="Save file", type=str)
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
                
                msg='received: '+data.decode('utf-8')
                connection.sendall(bytes(msg,'utf-8'))
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
        msg='received: '+data_client.decode('utf-8')
        objectSocket.sendto(bytes(msg,'utf-8'), client_address)
        file.write(data_client.decode('utf-8')+'\n')

    file.close()
    clientsocket.close()


if __name__ == "__main__":

    HOST=argumento.host
    PORT=argumento.port
    file=open(argumento.file, 'a')

    if argumento.transport == 'tcp':
        tcp_server(HOST, PORT)
    elif argumento.transport == 'udp':
        udp_server(HOST, PORT)
    