import socket
import threading
import pickle
import os
import sys
import signal

# Configuración del servidor
server_ip = ''
server_port = 60000

# Crear socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)

print(f"Servidor escuchando en {server_ip}:{server_port}")

clients = []
usernames = []
client_addresses = []

# Ruta del archivo de la base de datos
db_folder = 'database'
db_file = os.path.join(db_folder, 'chat.pkl')

# Crear la carpeta de la base de datos si no existe
os.makedirs(db_folder, exist_ok=True)

# Cargar mensajes de la base de datos
if os.path.exists(db_file):
    with open(db_file, 'rb') as f:
        messages = pickle.load(f)
else:
    messages = []

def store_message(ip, username, message, recipient=None):
    messages.append((ip, username, message, recipient))
    with open(db_file, 'wb') as f:
        pickle.dump(messages, f)

def get_message_history(requester_username):
    public_messages = [msg for msg in messages if msg[3] is None]
    private_messages = [msg for msg in messages if msg[3] == requester_username or msg[1] == requester_username]
    return public_messages + private_messages

def disconneted(client_socket):
    index = clients.index(client_socket)
    username = usernames[index]
    ip = client_addresses[index]
    message = f"ChatBot:{username} ({ip}) se ha desconectado".encode('utf-8')
    broadcast(message, client_socket)
    clients.remove(client_socket)
    usernames.remove(username)
    client_addresses.remove(ip)

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            client.send(message)

def send_private_message(sender, recipient_username, message):
    if recipient_username in usernames:
        recipient_index = usernames.index(recipient_username)
        recipient_socket = clients[recipient_index]
        sender_index = clients.index(sender)
        sender_username = usernames[sender_index]
        private_message = f"Privado de {sender_username}: {message}".encode('utf-8')
        recipient_socket.send(private_message)
        store_message(client_addresses[sender_index], sender_username, f"Privado para {recipient_username}: {message}", recipient_username)
    else:
        sender.send(f"Usuario {recipient_username} no encontrado.".encode('utf-8'))

# Función para manejar los mensajes de los clientes
def handle_client(client_socket, client_address):
    print(f"{client_address} Cliente conectado.")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'exit':
                print(f"{client_address} Cliente se ha desconectado.")
                client_socket.send('exit'.encode('utf-8'))
                disconneted(client_socket)
                client_socket.close()
                break
            elif message == 'history':
                index = clients.index(client_socket)
                username = usernames[index]
                history = get_message_history(username)
                history_message = '\n'.join([f"{ip} ({username}): {msg}" for ip, username, msg, _ in history])
                client_socket.sendall(history_message.encode('utf-8'))
            elif message.startswith('@'):
                recipient_username, private_message = message.split(' ', 1)
                recipient_username = recipient_username[1:]  # Remove '@' prefix
                send_private_message(client_socket, recipient_username, private_message)
            else:
                print(f"{client_address}: {message}")
                index = clients.index(client_socket)
                username = usernames[index]
                ip = client_addresses[index]
                store_message(ip, username, message)
                broadcast(f"{username}: {message}".encode('utf-8'), client_socket)
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
        client_addresses.append(client_address[0])
        message = f"ChatBot : {username} ({client_address[0]}) se ha unido al chat".encode('utf-8')
        broadcast(message, client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

# Función para manejar la señal de interrupción
def signal_handler(sig, frame):
    print('Deteniendo el servidor...')
    for client in clients:
        client.close()
    sys.exit(0)

# Registrar la señal de interrupción cuando aprietas ctrl+C
signal.signal(signal.SIGINT, signal_handler)

receve_connections()