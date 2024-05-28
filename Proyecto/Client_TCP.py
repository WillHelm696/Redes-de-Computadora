import socket
import threading

# Configuración del cliente
server_ip = input("Ingrese la IP del servidor: ")
server_port = 60000

# Crear socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Función para recibir mensajes del servidor
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'exit':
                print("Conexión cerrada por el servidor.")
                client_socket.close()
                break
            print(message)
        except:
            print("Error de conexión con el servidor.")
            client_socket.close()
            break

# Crear hilo para recibir mensajes
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Enviar mensajes al servidor
while True:
    message = input()
    client_socket.send(message.encode('utf-8'))
    if message == 'exit':
        print("Conexión cerrada.")
        client_socket.close()
        break

############################################################################################################

import socket
import threading

# Configuración del cliente
HOST = '127.0.0.1'
PORT = 60000

username = input("Ingrese su nombre de usuario: ")

def send_messages(s):
    while True:
        message = input()
        if message.lower() == 'exit':
            s.sendall(f"{username}:exit".encode('utf-8'))
            break
        s.sendall(f"{username}:{message}".encode('utf-8'))

def receive_messages(s):
    while True:
        data = s.recv(1024)
        if not data:
            break
        print(data.decode('utf-8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(username.encode('utf-8'))
    threading.Thread(target=receive_messages, args=(s,)).start()
    send_messages(s)
