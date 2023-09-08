import logging
import random
import string

import geopy.exc
import numpy as np
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

    def random_flag(self, form):
        if form:
            length = 6
            choices = string.ascii_uppercase
        else:
            length = 13
            choices = string.ascii_letters + string.digits
        return "SNAKE{" + "".join(random.choices(choices, k=length)) + "}"


    def random_meta_gen(self):
        metadata = {
            "Author": random.choice(["Alice", "Bob", "Charlie"]),
            "Date": f"{random.randint(2000, 2023)}-{random.randint(1, 12)}-{random.randint(1, 28)}",
            "Description": random.choice(["Landscape", "Portrait", "Abstract"]),
            "Camera Model": random.choice(["Canon EOS", "Nikon D", "Sony Alpha"]),
            "Exposure Time": f"{random.randint(1, 30)}/{random.randint(1, 1000)} seconds",
            "Focal Length": f"{random.uniform(10.0, 300.0):.2f} mm",
            "ISO": random.randint(100, 6400),
        }
        return metadata


    def random_encryption_technique(self):
        encryption_techniques = [
            # "AES",
            # "RSA",
            "Caesar Cipher",
            "Vigenère Cipher",
            "Substitution Cipher",
            "Transposition Cipher",
            "XOR Cipher",
        ]
        return random.choice(encryption_techniques)

    def encrypt_flag(self, flag, technique):
        # if technique == "AES":
        #     key = Fernet.generate_key()
        #     f = Fernet(key)
        #     encrypted_flag = f.encrypt(flag.encode()).decode()
        # elif technique == "RSA":
        #     private_key = serialization.load_pem_private_key(
        #         Fernet.generate_key(),
        #         password=None,
        #         backend=default_backend()
        #     )
        #     encrypted_flag = private_key.sign(flag.encode(), padding.PSS(
        #         mgf=padding.MGF1(hashes.SHA256()),
        #         salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256(),
        #     )
        if technique == "Caesar Cipher":
            shift = random.randint(1, 25)
            encrypted_flag = ''.join([chr((ord(char) + shift - 65) % 26 + 65) for char in flag])
        elif technique == "Vigenère Cipher":
            key = ''.join(random.choice(string.ascii_uppercase) for _ in range(len(flag)))
            encrypted_flag = ''.join([chr(((ord(char) + ord(key[i])) % 26) + 65) for i, char in enumerate(flag)])
        elif technique == "Substitution Cipher":
            key = ''.join(random.sample(string.ascii_letters, len(string.ascii_letters)))
            substitution_key = dict(zip(string.ascii_letters, key))
            encrypted_flag = ''.join([substitution_key[char] if char.isalpha() else char for char in flag])
        elif technique == "Transposition Cipher":
            encrypted_flag = ''.join([flag[i::3] for i in range(3)])
        elif technique == "XOR Cipher":
            xor_key = ''.join(random.choice(string.ascii_letters) for _ in range(len(flag)))
            encrypted_flag = ''.join([chr(ord(char) ^ ord(xor_key[i])) for i, char in enumerate(flag)])
        else:
            encrypted_flag = flag

        return encrypted_flag

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

            metadata = self.random_meta_gen()
            for key, value in metadata.items():
                flag += f'\n{key}: {value}'

            # Add random encryption (1 in 5 chance of single encryption, 1 in 20 chance of double encryption)
            if random.randint(1, 5) == 1:
                encryption_technique = self.random_encryption_technique()
                flag = self.encrypt_flag(flag, encryption_technique)
                logging.debug(f'Flag encrypted using {encryption_technique}')

            if random.randint(1, 20) == 1:
                encryption_technique = self.random_encryption_technique()
                flag = self.encrypt_flag(flag, encryption_technique)
                logging.debug(f'Flag double encrypted using {encryption_technique}')

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
        flag = self.random_flag(False)
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

        # Add random encryption (1 in 5 chance of single encryption, 1 in 20 chance of double encryption)
        if random.randint(1, 5) == 1:
            encryption_technique = self.random_encryption_technique()
            flag = self.encrypt_flag(flag, encryption_technique)
            logging.debug(f'Flag encrypted using {encryption_technique}')

        if random.randint(1, 20) == 1:
            encryption_technique = self.random_encryption_technique()
            flag = self.encrypt_flag(flag, encryption_technique)
            logging.debug(f'Flag double encrypted using {encryption_technique}')

        png_metadata = PngImagePlugin.PngInfo()
        png_metadata.add_text("Flag", flag)
        png_metadata.add_text("Latitude", str(latitude))
        png_metadata.add_text("Longitude", str(longitude))

        # Save the image with the hidden flag and location information
        self.image.save('pixelheist/Engine/test/img/flag_geoloc_image.png', pnginfo=png_metadata)

        logging.debug(f'Flag hidden in the image with geographical location: {flag}')


    def hide_flag_in_noise(self, noise_level=0.1):
        if self.image:
            flag = self.random_flag(True)

            # Convert the image to a NumPy array
            img_array = np.array(self.image)

            # Calculate Gaussian noise with the specified noise level
            mean = 0
            std_dev = noise_level * 255
            noise = np.random.normal(mean, std_dev, img_array.shape).astype(np.uint8)

            # Add the noise to the image
            noisy_image = img_array + noise

            # Clip the pixel values to the valid range [0, 255]
            noisy_image = np.clip(noisy_image, 0, 255)

            # Convert the NumPy array back to an image
            noisy_image = Image.fromarray(noisy_image)

            # Add the flag to the noisy image
            font = ImageFont.truetype("arial.ttf", 8)  # Change the font and size as needed
            draw = ImageDraw.Draw(noisy_image)
            draw.text((300, 260), flag, font=font, fill="black")  # Adjust fill color as needed

            noisy_image.save('pixelheist/Engine/test/img/flag_with_gaussian_noise.png')

            logging.debug(f'Flag hidden in the image with Gaussian noise: {flag}')
        else:
            logging.error("Image not found. Please check the image path.")


# Example usage:
if __name__ == '__main__':
    # Path to input image
    image_path = 'pixelheist/Engine/test/img/How-to-Generate-Random-Numbers-in-Python.jpg'
    logging.debug(f'Image path: {image_path}')

    generator = ForensicChallengeGenerator(image_path)
    generator.hide_flag_in_image()
    generator.hide_flag_in_metadata()
    generator.hide_flag_in_geoloc()
    generator.hide_flag_in_noise()
