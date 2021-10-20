#Reescriba el código del servidor remote_shell para que ahora, en vez de utilizar multiprocessing
#o threading para lograr atender a varios clientes simultáneamente, lo haga haciendo uso de 
#concurrencia por medio de asyncio.

import argparse
import subprocess
import asyncio

analizador = argparse.ArgumentParser()
analizador.add_argument("-w", "--host", help="Host", type=str)
analizador.add_argument("-p", "--port", help="Port", type=int)
argumento = analizador.parse_args()

async def handler_shell(reader,writer):
    try:
        print('new connection...')
        while True:
            data= await reader.read(1024)
            if not data:
                print('closing connection...')
                break
            print('received: ',data.decode('utf-8'))
            data=data.split()
            command=subprocess.run(data, capture_output=True,shell=True)
            if command.returncode == 0:
                stdout=str(command.stdout,'utf-8')
                #Add task to loop
                writer.write(bytes(stdout,'utf-8'))
                #Send data to the client.
                await writer.drain()

            else:
                stderr=str(command.stderr,'utf-8')
                #Add task to loop
                writer.write(bytes(stderr,'utf-8'))
                #Send data to the client.
                await writer.drain()

    finally:
        # Close the connection
        writer.close()


async def main():
    HOST=argumento.host
    PORT=argumento.port
    #Create asynchronous server
    server=await asyncio.start_server(handler_shell,HOST,PORT)
    addr=server.sockets[0].getsockname()
    print('serving on ',addr)

    async with server:
        #waiting new connection
        await server.serve_forever()

asyncio.run(main())
