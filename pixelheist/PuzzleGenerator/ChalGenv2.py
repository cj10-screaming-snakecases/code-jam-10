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

    @staticmethod
    def random_flag(form):
        if form:
            length = 6
            choices = string.ascii_uppercase
        else:
            length = 13
            choices = string.ascii_letters + string.digits
        return "SNAKE{" + "".join(random.choices(choices, k=length)) + "}"

    @staticmethod
    def random_meta_gen():
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
            "Caesar Cipher",
            "Vigenère Cipher",
            "Substitution Cipher",
            "Transposition Cipher",
            "XOR Cipher",
        ]
        return random.choice(encryption_techniques)

    @staticmethod
    def encrypt_flag(flag, technique, max_length=20):
        if len(flag) > max_length:
            print(flag)
            raise ValueError(f"Flag length ({len(flag)}) exceeds the maximum length ({max_length}).")

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
            flag = self.random_flag(True)  # Initialize with a random flag text

            # Create a copy of the image
            image_with_flag = self.image.copy()
            draw = ImageDraw.Draw(image_with_flag)

            font = ImageFont.truetype("arial.ttf", 8)
            draw.text((350, 300), flag, font=font, fill="black")

            image_with_flag.save('pixelheist/Engine/test/img/flag_image_with_text.png')

            logging.debug(f'Flag hidden in the image: {flag}')
            return flag
        else:
            logging.error("Image not found. Please check the image path.")
            return None

    def hide_flag_in_metadata(self):
        if self.image:
            flag = self.random_flag(True)  # Initialize with a random flag text

            # Generate random metadata
            metadata = self.random_meta_gen()

            # Append the metadata information to the flag
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

            self.image.save('pixelheist/Engine/test/img/imgflag_metadata_image.png', pnginfo=png_metadata)

            logging.debug(f'Flag hidden in the image metadata: {flag}')
            return flag
        else:
            logging.error("Image not found. Please check the image path.")
            return None

    def hide_flag_in_geoloc(self):
        if not self.image:
            logging.error("Image not found. Please check the image path.")
            return None

        flag = self.random_flag(False)  # Initialize with a random flag text
        city = "Amsterdam"

        try:
            location = self.geolocator.geocode(city)
            if location:
                latitude = location.latitude
                longitude = location.longitude
                logging.debug(f'Geographical Location - Latitude: {latitude}, Longitude: {longitude}')
            else:
                logging.error("Failed to obtain geographical location information.")
                return None
        except geopy.exc.GeocoderTimedOut:
            logging.error("Geocoding service timed out. Please try again later.")
            return None
        except Exception as e:
            logging.error(f"Error obtaining geographical location information: {e}")
            return None

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
        return flag

    def hide_flag_in_noise(self, prev_solution=None, noise_level=0.1):
        if self.image:
            flag = self.random_flag(True)  # Initialize with a random flag text

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

            font = ImageFont.truetype("arial.ttf", 8)
            draw = ImageDraw.Draw(noisy_image)
            draw.text((300, 260), flag, font=font, fill="black")

            noisy_image.save('pixelheist/Engine/test/img/flag_with_gaussian_noise.png')

            logging.debug(f'Flag hidden in the image with Gaussian noise: {flag}')
            return flag
        else:
            logging.error("Image not found. Please check the image path.")
            return None

    def hide_flag_in_colorshift(self, prev_solution=None):
        constant_value = random.randint(100, 255)
        if self.image:
            # Copy the image
            image_with_flag = self.image.copy()
            draw = ImageDraw.Draw(image_with_flag)
            width, height = image_with_flag.size
            pixels = image_with_flag.load()
            # Add flag before encrypting
            flag = self.random_flag(True)
            font = ImageFont.truetype("arial.ttf", 20)
            flag_x = width // 2
            flag_y = height // 2
            draw.text((flag_x, flag_y), flag, font=font, fill="black")
            step = 0  # Randomness value
            for x in range(width):
                for y in range(height):
                    r, g, b = pixels[x, y]
                    r = (r + constant_value + step) % 256
                    g = (g + constant_value + step) % 256
                    b = (b + constant_value + step) % 256
                    pixels[x, y] = (r, g, b)
                    step += 1  # Increment step for each pixel
            image_with_flag.save('pixelheist/Engine/test/img/flag_color_shift.png')
            logging.debug(
                f'Color shifting challenge applied with constant value {constant_value}. Flag hidden in the image.')
            return flag
        else:
            logging.error("Image not found. Please check the image path.")
            return None

    def generate_challenge(self, num_levels=5):
        challenges = []

        for level in range(1, num_levels + 1):
            level_challenges = []
            logging.debug(f'Generating Level {level}')

            # Level 1: Add flag to image
            if level == 1:
                flag = self.hide_flag_in_image()
                level_challenges.append(f'Flag added to the image: {flag}')

            # Level 2: Encrypt the flag in metadata
            if level >= 2:
                flag = self.hide_flag_in_metadata()
                level_challenges.append(f'Flag encrypted in metadata: {flag}')

            # Level 3: Encrypt the flag and add to geolocation
            if level >= 3:
                flag = self.hide_flag_in_geoloc()
                level_challenges.append(f'Flag added to geolocation: {flag}')

            # Level 4: Add flag to noise and color shift
            if level >= 4:
                flag = self.hide_flag_in_noise(prev_challenge_solution)
                flag = self.hide_flag_in_colorshift(flag)
                level_challenges.append(f'Flag added to the image with Gaussian noise and color shift: {flag}')

            challenges.append(level_challenges)

        return challenges

    @staticmethod
    def generate_hints(challenges):
        hints = []
        for level_challenges in challenges:
            level_hints = []
            for challenge in level_challenges:
                # Generate hints based on the challenge description
                hint = f"Hint for challenge: {challenge}"
                level_hints.append(hint)
            hints.append(level_hints)
        return hints

    @staticmethod
    def generate_solutions(challenges):
        solutions = []
        for level_challenges in challenges:
            level_solutions = []
            for challenge in level_challenges:
                # Generate solutions based on the challenge description
                solution = f"Solution for challenge: {challenge}"
                level_solutions.append(solution)
            solutions.append(level_solutions)
        return solutions


if __name__ == '__main__':
    # input image
    image_path = 'pixelheist/Engine/test/img/How-to-Generate-Random-Numbers-in-Python.jpg'
    logging.debug(f'Image path: {image_path}')

    generator = ForensicChallengeGenerator(image_path)

    challenges = generator.generate_challenge(num_levels=5)

    hints = generator.generate_hints(challenges)

    solutions = generator.generate_solutions(challenges)

    # Log the challenges, hints, and solutions
    for i, level_challenges in enumerate(challenges):
        logging.debug(f'Level {i + 1} Challenges:')
        for j, challenge in enumerate(level_challenges):
            logging.debug(f'- Challenge {j + 1}: {challenge}')
            logging.debug(f'  - Hint: {hints[i][j]}')
            logging.debug(f'  - Solution: {solutions[i][j]}')
        logging.debug('')
