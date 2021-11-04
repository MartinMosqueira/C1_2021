# El cliente deberá establecer una conexión TCP contra el servidor, y por medio de dicho canal
# enviar al servidor las operaciones y operadores a calcular.
# El servidor recibirá las operaciones desde el cliente, y utilizará la cola de tareas Redis y
# los workers Celery para ejecutarlas. Deberá esperar el resultado calculado por Celery, y 
# luego enviar al cliente el resultado.
# Diseñe el protocolo de comunicación cliente-servidor como lo crea conveniente.

# Parámetros
# Los parámetros recibidos por el cliente serán los siguientes:

# -h ip_server
# -p port
# -o "operacion" (suma, resta, mult, div, pot)
# -n ## (primer operando)
# -m ## (segundo operando)
# Los parámetros recibidos por el servidor serán:

# -h ip_donde_atender
# -p port
# Ejemplo de ejecución:
# Servidor:

# python3 servidor_calc.py -h 0.0.0.0 -p 1234

# Cliente:

# python3 cliente_calc.py -h 127.0.0.1 -p 1234 -o suma -n 2 -m 3

# > 5

# Notas:
# Puede ejecutar toda la infraestructura en la misma computadora, por ejemplo, corriendo:
# Una terminal para el cliente
# Una terminal para el servidor
# Otra terminal con la cola de mensajes Redis
# Otra terminal con los workers Celery

import socketserver
import argparse
import pickle
from task import *

analizador = argparse.ArgumentParser()
analizador.add_argument("-w", "--host", help="Host", type=str)
analizador.add_argument("-p", "--port", help="Port", type=int)
argumento = analizador.parse_args()

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            print('connection...')
            while True:
                data=self.request.recv(1024)
                if not data:
                    print('client disconnected...')
                    break

                print('pickle data: ',data)
                pickleD=pickle.loads(data)
                print('received: ',pickleD)
                if pickleD[0] == 'suma':
                    result=suma.delay(pickleD[1],pickleD[2])

                elif pickleD[0] == 'resta':
                    result=resta.delay(pickleD[1],pickleD[2])

                elif pickleD[0] == 'div':
                    result=div.delay(pickleD[1],pickleD[2])
                
                elif pickleD[0] == 'mult':
                    result=mult.delay(pickleD[1],pickleD[2])

                elif pickleD[0] == 'pot':
                    result=pot.delay(pickleD[1],pickleD[2])
                
                else:
                    print('sending data back to the client')
                    pickleM=pickle.dumps('operation was not selected')
                    self.request.sendall(pickleM)
                    exit()


                print('sending data back to the client')
                pickleM=pickle.dumps(result.get())
                self.request.sendall(pickleM)

        finally:
            self.request.close()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    import threading
    import signal

    HOST=argumento.host
    PORT=argumento.port
    dataServer=((HOST,PORT))

    server = ThreadedTCPServer(dataServer, MyTCPHandler)

    with server:
        ip, port = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        print("Server loop running:",ip,port)

        try:
            signal.pause()
        except:
            server.shutdown()    
