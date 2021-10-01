#Reescribir el ejercicio de remote_shell_pickle para adaptarlo al uso de serversocket del
#lado del servidor.Añadir la opción -m para que al ejecutar el servidor, se pueda especificar
#si se atenderán varios clientes simultáneamente mediante forking (p) o threading (t).

import socketserver
import argparse
import subprocess
import pickle

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

                print('received: ',data)
                pickleDeserialize=pickle.loads(data)
                data=pickleDeserialize.split()
                command=subprocess.run(data, capture_output=True,shell=True)

                if command.returncode == 0:
                    print('sending data back to the client')
                    stdout=str(command.stdout,'utf-8')
                    pickleMessage=pickle.dumps(stdout)
                    #Send data to the client.
                    self.request.sendall(pickleMessage)
                else:
                    stderr=str(command.stderr,'utf-8')
                    pickleMessage=pickle.dumps(stderr)
                    #Send data to the client.
                    self.request.sendall(pickleMessage)
        
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
        ip, port = server.server_address
        #serve_forever: listen to multiple connections
        server_thread = threading.Thread(target=server.serve_forever)
        #separate the main thread from thread that serves 
        server_thread.daemon = True
        server_thread.start()

        print("Server loop running:",ip,port)

        try:
            signal.pause()
        except:
            server.shutdown()
