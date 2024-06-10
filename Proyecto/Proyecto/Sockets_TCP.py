import socket
import threading
import pickle
import os
import sys
import signal
import hashlib

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
passwords = {}

# Ruta del archivo de la base de datos
db_folder = 'database'
db_file = os.path.join(db_folder, 'chat.pkl')
users_file = os.path.join(db_folder, 'users.pkl')

# Crear la carpeta de la base de datos si no existe
os.makedirs(db_folder, exist_ok=True)

# Cargar mensajes de la base de datos
if os.path.exists(db_file):
    with open(db_file, 'rb') as f:
        messages = pickle.load(f)
else:
    messages = []

# Cargar usuarios y contraseñas de la base de datos
if os.path.exists(users_file):
    with open(users_file, 'rb') as f:
        stored_users = pickle.load(f)
        usernames = list(stored_users.keys())
        passwords = stored_users
else:
    stored_users = {}

# Función que guarda los mensajes en un archivo pickle
def store_message(ip, username, message, recipient=None):
    messages.append((ip, username, message, recipient))
    with open(db_file, 'wb') as f:
        pickle.dump(messages, f)

# Función para devolver el historial del usuario
def get_message_history(requester_username):
    public_messages = [msg for msg in messages if msg[3] is None]
    private_messages = [msg for msg in messages if msg[3] == requester_username or msg[1] == requester_username]
    return public_messages + private_messages

# Función que desconecta al usuario
def disconnected(client_socket):
    if client_socket in clients:
        index = clients.index(client_socket)
        username = usernames[index]
        ip = client_addresses[index]
        message = f"ChatBot: {username} ({ip}) se ha desconectado".encode('utf-8')
        broadcast(message, client_socket)
        clients.remove(client_socket)
        usernames.remove(username)
        client_addresses.remove(ip)

# Función que envía los mensajes públicos
def broadcast(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(message)

# Funcion para enviar mensajes privados a un usuario
def send_private_message(sender_socket, recipient_username, message):
    if recipient_username in usernames:
        recipient_index = usernames.index(recipient_username)
        recipient_socket = clients[recipient_index]
        sender_index = clients.index(sender_socket)
        sender_username = usernames[sender_index]
        private_message = f"Privado de {sender_username}: {message}".encode('utf-8')
        recipient_socket.send(private_message)
        store_message(client_addresses[sender_index], sender_username, f"Privado para {recipient_username}: {message}", recipient_username)
    else:
        sender_socket.send(f"Usuario {recipient_username} no encontrado.".encode('utf-8'))

# Algoritmo de hashing SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Función para manejar los mensajes de los clientes
def handle_client(client_socket, client_address):
    print(f"{client_address} Cliente conectado.")
    try:
        # Solicitar nombre de usuario
        client_socket.send("ChatBot: Username".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        # Solicitar contraseña
        client_socket.send("ChatBot: Introduce contraseña:".encode('utf-8'))
        password = client_socket.recv(1024).decode('utf-8')

        # Guardar el nombre de usuario y la contraseña para usuarios nuevos
        if username not in usernames:
            usernames.append(username)
            clients.append(client_socket)
            client_addresses.append(client_address[0])
            passwords[username] = hash_password(password)
            # Almacenar en un archivo pickle los usuarios
            stored_users[username] = passwords[username]
            with open(users_file, 'wb') as f:
                pickle.dump(stored_users, f)
            message = f"ChatBot: {username} ({client_address[0]}) se ha unido al chat".encode('utf-8')
            broadcast(message, client_socket)
        # Verificar la contraseña si el usuario ya entro antes
        else:
            if passwords[username] != hash_password(password):
                client_socket.send("ChatBot: Contraseña incorrecta. Desconectando...".encode('utf-8'))
                client_socket.close()
                return

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'exit':
                print(f"{client_address} Cliente se ha desconectado.")
                client_socket.send('exit'.encode('utf-8'))
                disconnected(client_socket)
                client_socket.close()
                break
            elif message == 'history':
                client_socket.send("ChatBot: Introduce contraseña para ver el historial:".encode('utf-8'))
                password = client_socket.recv(1024).decode('utf-8')
                index = clients.index(client_socket)
                username = usernames[index]
                if passwords[username] == hash_password(password):
                    history = get_message_history(username)
                    history_message = '\n'.join([f"{ip} ({username}): {msg}" for ip, username, msg, _ in history])
                    client_socket.sendall(history_message.encode('utf-8'))
                else:
                    client_socket.send("ChatBot: Contraseña incorrecta.".encode('utf-8'))
            elif message.startswith('@'):
                recipient_username, private_message = message.split(' ', 1)
                recipient_username = recipient_username[1:]  # Eliminar el prefijo '@'
                send_private_message(client_socket, recipient_username, private_message)
            else:
                print(f"{client_address}: {message}")
                index = clients.index(client_socket)
                username = usernames[index]
                ip = client_addresses[index]
                store_message(ip, username, message)
                broadcast(f"{username}: {message}".encode('utf-8'), client_socket)

    except Exception as e:
        print(f"Error: {e}")
        disconnected(client_socket)
        client_socket.close()

def receive_connections():
    # Aceptar conexiones de los clientes
    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

# Función para manejar la señal de interrupción (por ejemplo, Ctrl+C)
def signal_handler(sig, frame):
    print('Deteniendo el servidor...')
    for client in clients:
        client.send('exit'.encode('utf-8'))
        client.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
receive_connections()