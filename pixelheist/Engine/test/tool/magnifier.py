import logging

import pygame
from PIL import Image

# Configure logging
logging.basicConfig(filename='pixelheist/Engine/test/logs/magnifier.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Pygame
pygame.init()
logging.debug("Pygame initialized successfully.")

# Load the image
image_path = "pixelheist/Engine/test/img/flag_image_with_text.png"  # Replace with your image path
try:
    image = Image.open(image_path)
    logging.debug(f"Loaded image from {image_path}")
except Exception as e:
    logging.error(f"Error opening the image: {e}")
    image = None

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = image.size
MAGNIFIER_SIZE = 100
ZOOM_FACTOR = 2
WHITE = (255, 255, 255)

# Create a Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Image Magnifier")
logging.debug("Pygame screen created successfully.")

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Load the background image (only load once)
bg = pygame.image.load(image_path)
logging.debug("Background image loaded successfully.")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouse pos
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate the cropping coordinates
    left = max(0, mouse_x - (MAGNIFIER_SIZE // 2))
    top = max(0, mouse_y - (MAGNIFIER_SIZE // 2))
    right = min(image.width, left + MAGNIFIER_SIZE)
    bottom = min(image.height, top + MAGNIFIER_SIZE)

    # Magnifier region
    if right > left and bottom > top:
        region = image.crop((left, top, right, bottom))
        logging.debug("Cropped region for magnifier.")

        # Magnifier Center
        center_x = mouse_x - left
        center_y = mouse_y - top
        logging.debug(f"Mouse position: ({mouse_x}, {mouse_y}), Center: ({center_x}, {center_y})")

        # Region to pygame surface
        pygame_image = pygame.image.fromstring(region.tobytes(), region.size, region.mode)
        logging.debug("Converted region to Pygame surface.")

        # Clear the screen
        screen.fill(WHITE)
        logging.debug("Cleared the Pygame screen.")

        # Background
        screen.blit(bg, (0, 0))
        logging.debug("Drawn the background image.")

        # Display the magnified image centered around the mouse cursor position (can be offset later if needed)
        magnified_width = MAGNIFIER_SIZE * ZOOM_FACTOR
        magnified_height = MAGNIFIER_SIZE * ZOOM_FACTOR
        screen.blit(pygame.transform.scale(pygame_image, (magnified_width, magnified_height)),
                    (mouse_x - magnified_width // 2, mouse_y - magnified_height // 2))
        logging.debug("Drawn the magnified image.")

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
