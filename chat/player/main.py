import pygame
import socket
import threading

# Pygame configuration
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Chat Client")
font = pygame.font.Font(None, 36)

# Networking configuration
HOST = '192.168.31.95'
PORT = 65432

# Initialize socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                messages.append(message)
        except:
            break

messages = []

# Start the receiving thread
threading.Thread(target=receive_messages, daemon=True).start()

def main():
    input_box = pygame.Rect(100, HEIGHT - 50, WIDTH - 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width()+10)
    input_rect = pygame.Rect(100, HEIGHT - 50, width, 40)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                client_socket.close()
                return
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        client_socket.sendall(text.encode())
                        text = ''
                        txt_surface = font.render(text, True, color)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                    txt_surface = font.render(text, True, color)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_rect.w = width
        screen.blit(txt_surface, (input_rect.x+5, input_rect.y+5))
        pygame.draw.rect(screen, color, input_rect, 2)

        # Display messages
        y = 10
        for msg in messages:
            msg_surface = font.render(msg, True, (255, 255, 255))
            screen.blit(msg_surface, (10, y))
            y += 40

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
