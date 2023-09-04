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


    def random_flag(self):
        if self.form == True:
            return f'SNAKE{{{"".join(random.choice(string.ascii_letters.upper()) for _ in range(6))}}}' #for readability in image
        else:
            return f'SNAKE{{{"".join(random.choice(string.ascii_letters + string.digits) for _ in range(13))}}}'

    def hide_flag_in_image(self):
        
        if self.image:
            self.form = True
            flag = self.random_flag()
            
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
            self.form = False
            flag = self.random_flag()
            flag = str(flag)
    
            png_metadata = PngInfo()
            png_metadata.add_text("Flag", flag)
            
            
            self.image.save('cj10-screaming-snakecases/Engine/test/img/flag_metadata_image.png', pnginfo=png_metadata)
            
            print(f'Flag hidden in the image metadata: {flag}')
        else:
            print("Image not found. Please check the image path.")
            
# Example usage:
if __name__ == '__main__':
    image_path = 'C:/Users/cyn0v/Documents/GitHub/code-jam-10/cj10-screaming-snakecases/Engine/test/img/How-to-Generate-Random-Numbers-in-Python.jpg'  # Provide the path to your input image
    generator = ForensicChallengeGenerator(image_path)
    generator.hide_flag_in_image()
    generator.hide_flag_in_metadata() 
