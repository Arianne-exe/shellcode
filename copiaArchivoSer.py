import socket

# Creamos una lista con los datos del la conexión
CONEXION = (socket.gethostname(), 3305)

servidor = socket.socket()

# Ponemos el servidor a la escucha
servidor.bind(('', 3305))
servidor.listen(5)
print ("Escuchando {0} en {1}".format(*CONEXION))
# Aceptamos conexiones
sck, addr = servidor.accept()
print ("Conectado a: {0}:{1}".format(*addr))
while True:
    # Recibimos la longitud que envia el cliente
    recibido = sck.recv(1024).strip()
    if recibido:
        print ("Recibido:", recibido)
    # Verificamos que lo que recibimos sea un número
    # en caso que así sea, enviamos el mensaje "OK"
    # al cliente indicandole que estamos listos
    # para recibir el archivo
    recibido=recibido.decode("utf-8")
    if recibido.isdigit():
        sck.send(b'OK')

        # Inicializamos el contador que
        # guardara la cantidad de bytes recibidos
        buffer = 0
        # Abrimos el archivo en modo escritura binaria
        with open("archivo.pdf", "wb") as archivo:
            # Nos preparamos para recibir el archivo
            # con la longitud específica
            while (buffer < int(recibido)): #quite el igual
                data = sck.recv(1)
                if not len(data):
                    # Si no recibimos datos
                    # salimos del bucle
                    break
                # Escribimos cada byte en el archivo
                # y aumentamos en uno el buffer
                archivo.write(data)
                buffer += 1
                print(str(buffer))

            if buffer == int(recibido):
                print("Archivo descargado con éxito")
            else:
                print ("Ocurrió un error/Archivo incompleto")
        break
#1691152