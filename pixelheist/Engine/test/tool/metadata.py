import logging

from PIL import Image

# Configure logging
logging.basicConfig(filename='pixelheist/Engine/test/logs/image_metadata.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load the image
image_path = 'pixelheist/Engine/test/img/imgflag_metadata_image.png'  # Update with your image path

try:
    image = Image.open(image_path)
    logging.debug(f"Loaded image from {image_path}")
except Exception as e:
    logging.error(f"Error opening the image: {e}")
    image = None

# Display the image
if image:
    try:
        image.show()
        logging.debug("Displayed the image.")
    except Exception as e:
        logging.error(f"Error displaying the image: {e}")

# Print all metadata
metadata = image.info if image else {}
for key, value in metadata.items():
    print(f"{key}: {value}")
    logging.debug(f"Metadata - {key}: {value}")
