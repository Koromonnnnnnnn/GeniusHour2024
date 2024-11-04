import pygame

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Polygon")

# Define the polygon points
points = [
    (0, 12), (454, 181), (492, 369),
    (135, 439), (127, 433), (75, 454),
    (73, 451), (52, 447), (36, 447)
]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill((0, 0, 0))

    # Draw the polygon
    pygame.draw.polygon(screen, (255, 0, 0), points)

    # Draw some simple interior points
    for x in range(50, 500, 20):  # Adjust range for interior points
        for y in range(50, 500, 20):
            if (x + y) % 40 == 0:  # Simple condition for every other point
                screen.set_at((x, y), (0, 255, 0))  # Color interior points green

    # Update the display
    pygame.display.flip()

pygame.quit()
