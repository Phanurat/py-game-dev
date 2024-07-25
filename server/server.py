import socket
import threading
import json
import random

# Server configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 12345

clients = []
player_positions = {}
points = []

def broadcast(message):
    for client in clients:
        client.sendall(message.encode())

def handle_client(client_socket):
    global player_positions, points

    # Notify all clients of new player
    player_id = str(random.randint(1000, 9999))
    player_positions[player_id] = [random.randint(0, 800), random.randint(0, 600)]
    broadcast(f"NEW_PLAYER:{player_id}:{player_positions[player_id]}")

    # Add a new point
    new_point = [random.randint(0, 800), random.randint(0, 600)]
    points.append(new_point)
    broadcast(f"NEW_POINT:{new_point}")

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            if data.startswith("UPDATE_POSITION"):
                _, player_id, position = data.split(":", 2)
                player_positions[player_id] = json.loads(position)
                broadcast(f"UPDATE_POSITION:{player_id}:{player_positions[player_id]}")
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()
    clients.remove(client_socket)
    del player_positions[player_id]
    broadcast(f"REMOVE_PLAYER:{player_id}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server started. Waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    start_server()
