import socket
import threading

# Configuración del servidor
server_ip = ''
server_port = 60000

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

# Función para manejar la señal de interrupción
def signal_handler(sig, frame):
    print('Deteniendo el servidor...')
    for client in clients:
        client.close()
    conn.close()
    sys.exit(0)

# Registrar la señal de interrupción cuando aprietas ctrl+C
signal.signal(signal.SIGINT, signal_handler)

############################################################################################################

import socket
import sqlite3
import threading

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 60000

# Crear y conectar a la base de datos SQLite
conn = sqlite3.connect('chat.db', check_same_thread=False)
c = conn.cursor()

# Crear la tabla de mensajes si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')
conn.commit()

# Función para manejar la conexión de cada cliente
def handle_client(client_socket, addr):
    print(f"Conectado a {addr}")
    with client_socket:
        username = client_socket.recv(1024).decode('utf-8')
        # Enviar historial de mensajes al cliente
        c.execute("SELECT username, message FROM messages")
        messages = c.fetchall()
        for msg in messages:
            client_socket.sendall(f"{msg[0]}:{msg[1]}\n".encode('utf-8'))
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            if message.split(':', 1)[1] == 'exit':
                print(f"El usuario {username} ha abandonado la conversación")
                client_socket.sendall(f"{username}:exit".encode('utf-8'))
                break
            c.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, message.split(':', 1)[1]))
            conn.commit()
            print(f"Mensaje de {username}: {message.split(':', 1)[1]}")

# Iniciar el servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")
    while True:
        client_socket, addr = s.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()
