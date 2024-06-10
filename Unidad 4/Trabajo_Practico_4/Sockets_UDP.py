import socket
import threading

# Configuración
BROADCAST_IP = '255.255.255.255'
PORT = 60000

# Pedir nombre de usuario
username = input("Ingrese su nombre de usuario: ")

# Crear socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(('', PORT))

def receive_messages():
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode('utf-8')
        user, msg = message.split(':', 1)
        if msg.strip() == 'exit':
            print(f"El usuario {user} ({addr[0]}) ha abandonado la conversación")
            break
        elif msg.strip() == 'nuevo':
            print(f"El usuario {user} se ha unido a la conversación")
        else:
            print(f"{user} ({addr[0]}) dice: {msg}")

def send_messages():
    while True:
        msg = input()
        if msg.strip().lower() == 'exit':
            message = f"{username}:exit"
            sock.sendto(message.encode('utf-8'), (BROADCAST_IP, PORT))
            print("Has abandonado la conversación")
            break
        else:
            message = f"{username}:{msg}"
            sock.sendto(message.encode('utf-8'), (BROADCAST_IP, PORT))

# Enviar mensaje de unión
sock.sendto(f"{username}:nuevo".encode('utf-8'), (BROADCAST_IP, PORT))

# Crear hilos para enviar y recibir mensajes
receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

# Iniciar hilos
receive_thread.start()
send_thread.start()

# Esperar a que los hilos terminen
send_thread.join()
receive_thread.join()

# Cerrar socket
sock.close()
