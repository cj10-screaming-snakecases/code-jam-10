import logging
import random
import string

import geopy.exc
from geopy.geocoders import Nominatim
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

# Configure logging
logging.basicConfig(filename='pixelheist/Engine/test/logs/ChalGen.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ForensicChallengeGenerator:
    def __init__(self, image_path):
        self.geolocator = Nominatim(user_agent="geo_flag_generator")
        try:
            self.image = Image.open(image_path)
        except Exception as e:
            logging.error(f"Error opening the image: {e}")
            self.image = None

        if self.image:
            logging.info("Image opened successfully.")
        else:
            logging.error("Image not found. Please check the image path.")

    @staticmethod
    def random_flag(form):
        if form:
            length = 6
            choices = string.ascii_uppercase
        else:
            length = 13
            choices = string.ascii_letters + string.digits
        return "SNAKE" + "".join(random.choices(choices, k=length))

    def hide_flag_in_image(self):
        if self.image:
            flag = self.random_flag(True)

            # Create a copy of the image
            image_with_flag = self.image.copy()
            draw = ImageDraw.Draw(image_with_flag)

            font = ImageFont.truetype("arial.ttf", 8)  # Change the font and size as needed
            draw.text((350, 300), flag, font=font, fill="black")  # Adjust fill color as needed

            image_with_flag.save('pixelheist/Engine/test/img/flag_image_with_text.png')

            logging.debug(f'Flag hidden in the image: {flag}')
        else:
            logging.error("Image not found. Please check the image path.")

    def hide_flag_in_metadata(self):
        if self.image:
            flag = self.random_flag(False)
            flag = str(flag)

            png_metadata = PngImagePlugin.PngInfo()
            png_metadata.add_text("Flag", flag)

            self.image.save('pixelheist/Engine/test/img/flag_metadata_image.png', pnginfo=png_metadata)

            logging.debug(f'Flag hidden in the image metadata: {flag}')
        else:
            logging.error("Image not found. Please check the image path.")

    def hide_flag_in_geoloc(self):
        if not self.image:
            logging.error("Image not found. Please check the image path.")
            return

        city = "Amsterdam"
        flag = self.random_flag()
        flag = str(flag)

        try:
            location = self.geolocator.geocode(city)
            if location:
                latitude = location.latitude
                longitude = location.longitude
                logging.debug(f'Geographical Location - Latitude: {latitude}, Longitude: {longitude}')
            else:
                logging.error("Failed to obtain geographical location information.")
                return
        except geopy.exc.GeocoderTimedOut:
            logging.error("Geocoding service timed out. Please try again later.")
            return
        except Exception as e:
            logging.error(f"Error obtaining geographical location information: {e}")
            return

        # Embed the location information into the image metadata
        png_metadata = PngImagePlugin.PngInfo()
        png_metadata.add_text("Flag", flag)
        png_metadata.add_text("Latitude", str(latitude))
        png_metadata.add_text("Longitude", str(longitude))

        # Save the image with the hidden flag and location information
        self.image.save('pixelheist/Engine/test/img/flag_geoloc_image.png', pnginfo=png_metadata)

        logging.debug(f'Flag hidden in the image with geographical location: {flag}')


# Example usage:
if __name__ == '__main__':
    # Path to input image
    image_path = 'pixelheist/Engine/test/img/How-to-Generate-Random-Numbers-in-Python.jpg'
    logging.debug(f'Image path: {image_path}')

    generator = ForensicChallengeGenerator(image_path)
    generator.hide_flag_in_image()
    generator.hide_flag_in_metadata()
    generator.hide_flag_in_geoloc()
