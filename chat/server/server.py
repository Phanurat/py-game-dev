import socket
import threading

# Server configuration
HOST = '0.0.0.0'
PORT = 65432

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received message: {data.decode()}")
            # Broadcast message to all clients
            for client in clients:
                if client != conn:
                    client.sendall(data)
        except ConnectionResetError:
            break
    conn.close()

# List of connected clients
clients = []

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server started on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
