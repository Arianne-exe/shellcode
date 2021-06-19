from socket import socket
import sys

def main(host,puerto):
    s = socket()
    s.connect((host, int(puerto)))

    while True:
        f = open("logoUv.jpg", "rb")
        content = f.read(1024)

        while content:
            # Enviar contenido.
            s.send(content)
            content = f.read(1024)

        break

    # Se utiliza el caracter de código 1 para indicar
    # al cliente que ya se ha enviado todo el contenido.
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
    host=sys.argv[1]
    puerto=sys.argv[2]
    main()