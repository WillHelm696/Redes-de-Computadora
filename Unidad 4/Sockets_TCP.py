import socket
import threading

# Configuración del servidor
server_ip = '0.0.0.0'
server_port = 5000

# Crear socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)

print(f"Servidor escuchando en {server_ip}:{server_port}")

clients=[]
usernames=[]

def disconneted(client_socket):
    index = clients.index(client_socket)
    username = usernames[index]
    message = f"ChatBot:{username} se ha desconectado".encode('utf-8')
    broadcast(message,client_socket)
    clients.remove(client_socket)
    usernames.remove(username)

def broadcast(message,client_socket):
    for client in clients:
        if client != client_socket:
            client.send(message)

# Función para manejar los mensajes de los clientes
def handle_client(client_socket, client_address):
    print(f"{client_address} Cliente conectado.")
    while True:
        try:
            message = client_socket.recv(1024)
            if message.decode('utf-8') == 'exit':
                print(f"{client_address} Cliente se ha desconectado.")
                client_socket.send('exit'.encode('utf-8'))
                disconneted(client_socket)
                client_socket.close()
                break
            print(f"{client_address}:{message.decode('utf-8')}")
            broadcast(message,client_socket)

        except:

            disconneted(client_socket)

            print(f"{client_address} Error de conexión con el cliente.")
            client_socket.close()
            break

def receve_connections():

    # Aceptar conexiones de los clientes
    while True:
        client_socket, client_address = server_socket.accept()

        client_socket.send("@Username".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client_socket)

        message = f"ChatBot : {username} Se a unido al chat".encode('utf-8')
        broadcast(message,client_socket)

        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

receve_connections()