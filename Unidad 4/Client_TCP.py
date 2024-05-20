import socket
import threading

# Configuración del cliente
server_ip = input("Ingrese la IP del servidor: ")
server_port = 5000

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
