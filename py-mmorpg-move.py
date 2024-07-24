import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Top-Down View Game")

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)

# Player properties
player_pos = [screen_width // 2, screen_height // 2]
player_radius = 20
player_speed = 5

# World dimensions
world_width = 1600
world_height = 1200

# Camera properties
camera = pygame.Rect(0, 0, screen_width, screen_height)

def move_camera(camera, target_rect):
    camera.x = target_rect.x + target_rect.width // 2 - camera.width // 2
    camera.y = target_rect.y + target_rect.height // 2 - camera.height // 2

    # Limit scrolling to map size
    camera.x = max(0, min(camera.x, world_width - camera.width))
    camera.y = max(0, min(camera.y, world_height - camera.height))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed
    if keys[pygame.K_w]:
        player_pos[1] -= player_speed
    if keys[pygame.K_s]:
        player_pos[1] += player_speed

    # Fill the screen with white
    screen.fill(white)

    # Create a rectangle for the player
    player_rect = pygame.Rect(player_pos[0] - player_radius, player_pos[1] - player_radius, player_radius * 2, player_radius * 2)

    # Move the camera to follow the player
    move_camera(camera, player_rect)

    # Draw the player (a blue circle)
    pygame.draw.circle(screen, blue, (player_rect.centerx - camera.x, player_rect.centery - camera.y), player_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
