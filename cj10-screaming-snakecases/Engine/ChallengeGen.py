import random
import string

from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo


class ForensicChallengeGenerator:
    def __init__(self, image_path):
        try:
            self.image = Image.open(image_path)
        except Exception as e:
            print(f"Error opening the image: {e}")
            self.image = None

        if self.image:
            print("Image opened successfully.")
        else:
            print("Image not found. Please check the image path.")

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

            image_with_flag.save('cj10-screaming-snakecases/Engine/test/img/flag_image_with_text.png')

            print(f'Flag hidden in the image: {flag}')
        else:
            print("Image not found. Please check the image path.")

    def hide_flag_in_metadata(self):
        if self.image:
            flag = self.random_flag(False)
            flag = str(flag)

            png_metadata = PngInfo()
            png_metadata.add_text("Flag", flag)

            self.image.save('cj10-screaming-snakecases/Engine/test/img/flag_metadata_image.png', pnginfo=png_metadata)

            print(f'Flag hidden in the image metadata: {flag}')
        else:
            print("Image not found. Please check the image path.")


# Example usage:
if __name__ == '__main__':
    image_path = 'cj10-screaming-snakecases/Engine/test/img/How-to-Generate-Random-Numbers-in-Python.jpg'
    generator = ForensicChallengeGenerator(image_path)
    generator.hide_flag_in_image()
    generator.hide_flag_in_metadata()
