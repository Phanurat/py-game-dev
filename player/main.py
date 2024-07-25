import pygame
import socket
import threading
import json
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MMORPG Client")

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

# Player properties
player_pos = [screen_width // 2, screen_height // 2]
player_radius = 20
player_speed = 5
players = {}
points = []

# Server configuration
SERVER = '192.168.31.95'  # Replace with the IP address of the server machine
PORT = 12345

def receive_messages(client_socket):
    global players, points
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg:
                if msg.startswith("NEW_PLAYER"):
                    _, player_id, position = msg.split(":", 2)
                    players[player_id] = json.loads(position)
                elif msg.startswith("UPDATE_POSITION"):
                    _, player_id, position = msg.split(":", 2)
                    players[player_id] = json.loads(position)
                elif msg.startswith("REMOVE_PLAYER"):
                    _, player_id = msg.split(":", 1)
                    if player_id in players:
                        del players[player_id]
                elif msg.startswith("NEW_POINT"):
                    _, point = msg.split(":", 1)
                    points.append(json.loads(point))
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER, PORT))
        print("Connected to the server.")
    except ConnectionRefusedError:
        print("Failed to connect to the server. Make sure the server is running and the IP address is correct.")
        return
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        return

    # Generate a unique player ID
    player_id = str(random.randint(1000, 9999))

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_pos[0] -= player_speed
        if keys[pygame.K_d]:
            player_pos[0] += player_speed
        if keys[pygame.K_w]:
            player_pos[1] -= player_speed
        if keys[pygame.K_s]:
            player_pos[1] += player_speed
        
        screen.fill(white)
        pygame.draw.circle(screen, blue, player_pos, player_radius)

        # Send player position to the server
        try:
            client_socket.sendall(f"UPDATE_POSITION:{player_id}:{json.dumps(player_pos)}".encode())
        except Exception as e:
            print(f"Error sending player position: {e}")

        # Draw other players
        for pid, pos in players.items():
            pygame.draw.circle(screen, blue, pos, player_radius)

        # Draw points
        for point in points:
            pygame.draw.circle(screen, red, point, 10)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    client_socket.close()

if __name__ == "__main__":
    main()
