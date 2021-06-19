


import threading
import signal
import socket
import sys
import os


FIN_COMANDO = b'#00#'

def desplegar_salida_comando(salida):
    salida = salida.decode('UTF-8')
    print(salida)

def obtener_respuesta(socket):
    salida = socket.recv(2048)
    while not salida.endswith(FIN_COMANDO):
        salida += salida.recv(2048)
    quitar_caracteres = len(FIN_COMANDO)
    return salida[:-quitar_caracteres]

def mandar_comando(comando, socket):
    comando = comando.encode('UTF-8')
    comando += FIN_COMANDO
    socket.send(comando)
    salida = obtener_respuesta(socket)
    return salida

def atender_cliente(socket, addr):
    comando = ''
    while comando != b'exit':
        comando = input('{} $>'.format(addr))
        respuesta = mandar_comando(comando, socket)
        desplegar_salida_comando(respuesta)

def inicializar_servidor(puerto):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('', int(puerto)))
    servidor.listen(5)
    while True:
            cliente, addr = servidor.accept()
            print('Escuchando peticiones en el puerto %s' % puerto)
            hilo = threading.Thread(target=atender_cliente, args=(cliente, addr))
            hilo.start()

if __name__ == '__main__':
    puerto = sys.argv[1]
    inicializar_servidor(puerto)
