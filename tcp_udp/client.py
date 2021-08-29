import socket
import argparse


analizador = argparse.ArgumentParser()
analizador.add_argument("-w", "--host", help="Host", type=str)
analizador.add_argument("-p", "--port", help="Puerto", type=int)
analizador.add_argument("-t", "--transport", help="package transport", type=str)
argumento = analizador.parse_args()

def tcp_client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddress=((host,port))
    sock.connect(serverAddress)

    while True:
        message = input('user:~$')
        sock.sendall(bytes(message,encoding='utf8'))
        data = sock.recv(1024)
        print(data.decode('utf-8'))

        if message == 'exit':
            break
    print('closing socket')
    sock.close()

def udp_client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        message = input('user:~$')
        sock.sendto(bytes(message,encoding='utf8'), (host, port))
        data=sock.recvfrom(1024)
        print(data[0].decode('utf8'))

        if message == 'exit':
            break
    print('closing socket')
    sock.close()

if __name__ == "__main__":
    HOST=argumento.host
    PORT=argumento.port

    if argumento.transport == 'tcp':
        tcp_client(HOST, PORT)
    elif argumento.transport == 'udp':
        udp_client(HOST, PORT)
