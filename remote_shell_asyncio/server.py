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
    data= await reader.read(1024)
    data.decode('utf-8')
    data=data.split()
    command=subprocess.run(data, capture_output=True,shell=True)
    if command.returncode == 0:
        stdout=str(command.stdout,'utf-8')
        #Send data to the client.
        writer.write(bytes(stdout,'utf-8'))
        await writer.drain()

    else:
        stderr=str(command.stderr,'utf-8')
        writer.write(bytes(stderr,'utf-8'))
        await writer.drain()

    writer.close()


async def main():
    HOST=argumento.host
    PORT=argumento.port
    server=await asyncio.start_server(handler_shell,HOST,PORT)
    addr=server.sockets[0].getsockname()
    print('server ',addr)

    async with server:
        await server.serve_forever()

asyncio.run(main())
