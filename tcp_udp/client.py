import socket
import argparse
import sys
import re


analizador = argparse.ArgumentParser()
analizador.add_argument("-a", help="Host", type=str)
analizador.add_argument("-p", help="Puerto", type=int)
analizador.add_argument("-t", help="package transport", type=str)
argumento = analizador.parse_args()

def tcp_client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddress=((host,port))
    sock.connect(serverAddress)

    while True:
        print('message:'+'\n')
        message = sys.stdin.read()
        sock.sendall(bytes(message,encoding='utf8'))

        if re.search('exit', message):
            break
    print('closing socket')
    sock.close()

def udp_client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        print('message:'+'\n')
        message = sys.stdin.read()
        sock.sendto(bytes(message,encoding='utf8'), (host, port))

        if re.search('exit', message):
            break
    print('closing socket')
    sock.close()

if __name__ == "__main__":
    HOST=argumento.a
    PORT=argumento.p

    if argumento.t == 'tcp':
        tcp_client(HOST, PORT)
    elif argumento.t == 'udp':
        udp_client(HOST, PORT)
