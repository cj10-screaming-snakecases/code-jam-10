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

            # Convert img to NumPy array
            img_array = np.array(self.image)

            # Gaussian noise with the specified noise level
            mean = 0
            std_dev = noise_level * 255
            noise = np.random.normal(mean, std_dev, img_array.shape).astype(np.uint8)

            # Add noise to the image
            noisy_image = img_array + noise

            # Clip the pixel values to the valid range [0, 255]
            noisy_image = np.clip(noisy_image, 0, 255)

            noisy_image = Image.fromarray(noisy_image)

            font = ImageFont.truetype("arial.ttf", 8)  # Change the font and size as needed
            draw = ImageDraw.Draw(noisy_image)
            draw.text((300, 260), flag, font=font, fill="black")  # Adjust fill color as needed

            noisy_image.save('pixelheist/Engine/test/img/flag_with_gaussian_noise.png')

            logging.debug(f'Flag hidden in the image with Gaussian noise: {flag}')
        else:
            logging.error("Image not found. Please check the image path.")

    def hide_flag_in_colorshift(self):
        constant_value = random.randint(100, 255)
        if self.image:
            # copy
            image_with_flag = self.image.copy()
            draw = ImageDraw.Draw(image_with_flag)

            width, height = image_with_flag.size
            pixels = image_with_flag.load()

            # Add flag before encrypting (messed this up a few times lmfao)
            flag = self.random_flag(True)
            font = ImageFont.truetype("arial.ttf", 20)  # Change the font and size as needed
            flag_x = width // 2
            flag_y = height // 2
            draw.text((flag_x, flag_y), flag, font=font, fill="black")  # Adjust fill color as needed

            step = 0  # randomnessval
            for x in range(width):
                for y in range(height):
                    r, g, b = pixels[x, y]
                    r = (r + constant_value + step) % 256
                    g = (g + constant_value + step) % 256
                    b = (b + constant_value + step) % 256
                    pixels[x, y] = (r, g, b)
                    step += 1  # Increment step for each pixel

            image_with_flag.save('pixelheist/Engine/test/img/flag_color_shift.png')

            logging.debug(f'Color shift applied with constant {constant_value}')
        else:
            logging.error("Image not found. Please check the image path.")
        return constant_value

    def generate_levels(self, num_levels=5):
        levels = []
        image_path = 'pixelheist/Engine/test/img/How-to-Generate-Random-Numbers-in-Python.jpg'
        flag = None
        prev_challenge_solution = None

        for level in range(1, num_levels + 1):
            level_challenges = []
            logging.debug(f'Generating Level {level}')

            # Level 1: Add flag to image
            if level == 1:
                self.image = Image.open(image_path)
                flag = self.random_flag(True)
                self.hide_flag_in_image()
                level_challenges.append(f'Flag added to the image: {flag}')
                prev_challenge_solution = flag

            # Level 2: Encrypt the flag in metadata
            if level >= 2:
                self.image = Image.open('pixelheist/Engine/test/img/flag_image_with_text.png')
                flag = self.encrypt_flag(prev_challenge_solution, self.random_encryption_technique())
                self.hide_flag_in_metadata()
                level_challenges.append(f'Flag encrypted in metadata: {flag}')
                prev_challenge_solution = flag

            # Level 3: Encrypt the flag and add to geolocation
            if level >= 3:
                self.image = Image.open('pixelheist/Engine/test/img/flag_metadata_image.png')
                flag = self.encrypt_flag(prev_challenge_solution, self.random_encryption_technique())
                self.hide_flag_in_geoloc()
                level_challenges.append(f'Flag added to geolocation: {flag}')
                prev_challenge_solution = flag

            # Level 4: Add flag to noise and color shift
            if level >= 4:
                self.image = Image.open('pixelheist/Engine/test/img/flag_geoloc_image.png')
                flag = self.encrypt_flag(prev_challenge_solution, self.random_encryption_technique())
                self.hide_flag_in_noise()
                const = self.hide_flag_in_colorshift()
                level_challenges.append(f'Applied Gaussian noise (Level: {const}): {flag}')
                prev_challenge_solution = flag

            # Level 5: Add more encryption
            if level == 5:
                self.image = Image.open('pixelheist/Engine/test/img/flag_color_shift.png')
                flag = self.encrypt_flag(prev_challenge_solution, self.random_encryption_technique())
                level_challenges.append(f'Flag added with additional encryption: {flag}')

            levels.append(level_challenges)

        return levels


# Example usage:
if __name__ == '__main__':
    # Path to input image
    image_path = 'pixelheist/Engine/test/img/How-to-Generate-Random-Numbers-in-Python.jpg'
    logging.debug(f'Image path: {image_path}')

    generator = ForensicChallengeGenerator(image_path)
    # Generate 5 levels of difficulty
    levels = generator.generate_levels(num_levels=5)

    # Log the challenges and solutions
    for i, level_challenges in enumerate(levels):
        logging.debug(f'Level {i + 1} Challenges:')
        for challenge in level_challenges:
            logging.debug(f'- {challenge}')
        logging.debug('')

    # Print the challenges and solutions in each level
    for i, level_challenges in enumerate(levels):
        print(f'Level {i + 1} Challenges:')
        for challenge in level_challenges:
            print(f'- {challenge}')
        print()
    # generator.hide_flag_in_image()
    # generator.hide_flag_in_metadata()
    # generator.hide_flag_in_geoloc()
    # generator.hide_flag_in_noise()
    # generator.hide_flag_in_colorshift()
