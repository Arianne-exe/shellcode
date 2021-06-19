from socket import socket
import sys

puerto = int(3305)
host = 'terminal'
archi = "db.sqlite3"

def main(host,puerto,archi):
    s = socket()
    s.connect((host, int(puerto)))

    while True:
        f = open(archi, "rb")
        content = f.read(1024)

        while content:
            # Enviar contenido.
            s.send(content)
            content = f.read(1024)

        break


    try:
        s.send(chr(1))
    except TypeError:
        # Compatibilidad con Python 3.
        s.send(bytes(chr(1), "utf-8"))

    # Cerrar conexión y archivo.
    s.close()
    f.close()
    print("El archivo ha sido enviado correctamente.")


if __name__ == "__main__":
    main(host,puerto,archi)
