from PIL import Image

# Load the image
image_path = 'cj10-screaming-snakecases/Engine/test/img/flag_metadata_image.png'  # Update with your image path
image = Image.open(image_path)
image.show()

# Print all metadata
metadata = image.info
for key, value in metadata.items():
    print(f"{key}: {value}")
