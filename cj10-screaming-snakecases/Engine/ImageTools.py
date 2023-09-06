
# This file contains the class ImageTools that should be able to take in any image (as a 2D pixel array)
# and return another 2D pixel array according to what is called. Any other to be added in time should be able
# to be added here easily.

# However, if an Image object is more desired over a np array, it will need to be changd in the future.


import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# I have included some basic image manipulation tools here

class ImageTools:
    def __init__(self, image, toArray=True) -> None:
        if toArray:
            image = np.asarray(image)

        self.image = image
        self.ROI = image.copy()

    def set_ROI(self, x, y, w, h):
        # Sets a Region Of Interest (ROI). This is useful for when we only want to zoom in on 
        # a portion of the image for displaying, etc. By default, ROI = entire image

        self.ROI = self.image[y:y+h, x:x+w]

    
    def zoom(self, scale, x, y, w, h):
        new_w = int(w * scale)
        new_h = int(h * scale)

        resized= np.array(Image.fromarray(self.ROI).resize((new_w, new_h)))

        return resized
    

    def contrast(self, factor):
        # 0 < factor < 1: Decrease contrast
        # factor = 1: No change
        # factor > 1: Increase contrast

        temp = Image.fromarray(self.ROI)

        enhancer = ImageEnhance.Contrast(temp)
        contrasted_image = enhancer.enhance(factor)

        contrasted_imArray = np.asarray(contrasted_image)
        return contrasted_imArray


    def brightness(self, brightness):
        # 0 < brightness < 1: Decrease contrast
        # brightness = 1: No change
        # brightness > 1: Increase brightness

        temp = Image.fromarray(self.ROI)

        enhancer = ImageEnhance.Brightness(temp)
        brightened_image = enhancer.enhance(brightness)

        brightened_imArray = np.asarray(brightened_image)
        return brightened_imArray


    def sharpness(self, sharpness):
        # 0 < sharpness < 1: Decrease sharpness
        # sharpness = 1: No change
        # sharpness > 1: Increase sharpness

        temp = Image.fromarray(self.ROI)

        enhancer = ImageEnhance.Sharpness(temp)
        sharpened_image = enhancer.enhance(sharpness)

        sharpened_imArray = np.asarray(sharpened_image)
        return sharpened_imArray


    def gaussian_blur(self, radius):
        temp = Image.fromarray(self.ROI)

        blurred_image = temp.filter(ImageFilter.GaussianBlur(radius))
        blurred_imArray = np.asarray(blurred_image)

        return blurred_imArray





if __name__ == "__main__":
    # Testing
    img = ImageTools()
                