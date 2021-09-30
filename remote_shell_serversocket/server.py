#Reescribir el ejercicio de remote_shell_pickle para adaptarlo al uso de serversocket del
#lado del servidor.Añadir la opción -m para que al ejecutar el servidor, se pueda especificar
#si se atenderán varios clientes simultáneamente mediante forking (p) o threading (t).

import socketserver
import argparse

analizador = argparse.ArgumentParser()
analizador.add_argument("-w", "--host", help="Host", type=str)
analizador.add_argument("-p", "--port", help="Port", type=int)
analizador.add_argument("-m", "--multiclient", help="forking(p)/threading(t)", type=str)
argumento = analizador.parse_args()

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            print('connection...')
            while True:
                data=self.request.recv(1024)
                if not data:
                    print('no data client')
                    break

                print('received: ',data.decode('utf-8'))
                self.request.sendall(data)
        
        finally:
        # Clean up the connection
            self.request.close()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
class ForkingTCPServer(socketserver.ForkingMixIn,socketserver.TCPServer,):
    pass


if __name__ == "__main__":
    import threading
    import signal

    HOST=argumento.host
    PORT=argumento.port
    dataServer=((HOST,PORT))

    if argumento.multiclient == 't':
        server = ThreadedTCPServer(dataServer, MyTCPHandler)
    elif argumento.multiclient == "p":
        server = ForkingTCPServer(dataServer, MyTCPHandler)
        
    with server:
        #serve_forever: listen to multiple connections
        server_thread = threading.Thread(target=server.serve_forever)
        #separate the main thread from thread that serves 
        server_thread.daemon = True
        server_thread.start()

        print("Server loop running:", server_thread.name)

        try:
            signal.pause()
        except:
            server.shutdown()
