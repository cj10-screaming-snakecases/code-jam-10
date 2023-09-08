# This file contains the class ImageTools that should be able to take in any image (as a 2D pixel array)
# and return another 2D pixel array according to what is called. Any other to be added in time should be able
# to be added here easily.

# However, if an Image object is more desired over a np array, it will need to be changd in the future.


import numpy as np
from PIL import Image, ImageEnhance

# I have included some basic image manipulation tools here


class ImageTools:
    def __init__(self, image: Image) -> None:
        self.image = image
        self.imArray = np.asarray(image)
        self.ROI = self.imArray.copy()

    def set_ROI(self, x, y, w, h):
        # Sets a Region Of Interest (ROI). This is useful for when we only want to zoom in on
        # a portion of the image for displaying, etc. By default, ROI = entire image

        self.ROI = self.imArray[y: y + h, x: x + w]

    def zoom(self, scale: float) -> Image:
        h, w, _ = self.imArray.shape
        new_w = int(w * scale)
        new_h = int(h * scale)

        resized = Image.fromarray(self.ROI.resize((new_w, new_h)))

        return resized

    def contrast(self, factor: float) -> Image:
        # 0 < factor < 1: Decrease contrast
        # factor = 1: No change
        # factor > 1: Increase contrast

        temp = self.ROI

        enhancer = ImageEnhance.Contrast(temp)
        contrasted_image = enhancer.enhance(factor)

        return contrasted_image

    def brightness(self, brightness: float) -> Image:
        # 0 < brightness < 1: Decrease contrast
        # brightness = 1: No change
        # brightness > 1: Increase brightness

        temp = self.ROI

        enhancer = ImageEnhance.Brightness(temp)
        brightened_image = enhancer.enhance(brightness)

        return brightened_image

    def sharpness(self, sharpness: float) -> Image:
        # 0 < sharpness < 1: Decrease sharpness
        # sharpness = 1: No change
        # sharpness > 1: Increase sharpness

        temp = Image.fromarray(self.ROI)

        enhancer = ImageEnhance.Sharpness(temp)
        sharpened_image = enhancer.enhance(sharpness)

        return sharpened_image

    def color_channel(self, channel: str) -> Image:
        # channel = RGB
        colorID = 'RGB'.index(channel)
        color_channel = self.imArray[:, :, colorID] 

        filtered_image = np.zeros_like(self.imArray)
        filtered_image[:, :, 1] = color_channel 

        return Image.fromarray(filtered_image)

    def difference(self, other_image: Image) -> np.ndarray:
        other_imArray = np.asarray(other_image)

        return self.imArray - other_imArray


if __name__ == "__main__":
    # Testing

    # raw = Image.open(r"pixelheist\Engine\test\img\rainbow.png")
    raw = Image.open(r"pixelheist\Engine\test\img\testimage.png")
    
    # TEST FOR ImageSteg.encode_LSB AND ImageTools.difference
    # from ImageSteganography import ImageSteg
    # enc = ImageSteg(raw)
    # img = ImageTools(raw)
    # enc.encode_LSB("There is an impostor among us!", px=100, py=100)

    # diff = np.abs(img.difference(enc.image)) * 255

    # diff = Image.fromarray(diff)
    # diff.show()  # Expect to see some colored pixels near top left

    img = ImageTools(raw)
    green = img.color_channel('G')
    green.show()
    nogreen = Image.fromarray(img.difference(green))
    nogreen.show()
