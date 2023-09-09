# This file contains the class ImageViewer, which should show pixel-level statistics of a certain region of interest
# For example: Show histograms, color channels, and pixel-level details. (@Envxsion)

# This will have to be programmed in conjunction with the GUI soon.


import numpy as np
from PIL import Image


class ImageViewer():
    def __init__(self, image: Image) -> None:
        self.image = image
        self.imArray = np.asarray(image)

    def histogram(self):
        intensities = np.zeros((4, 256))  # 4 color channel - RGB(A), and 256 possible intensity values
        h, w, _ = self.imArray.shape

        channels = self.image.split()

        for channel, channel_imArray in enumerate(channels):
            intensities[channel] = channel_imArray.histogram()

        return intensities


if __name__ == '__main__':
    img = Image.open(r"pixelheist\Engine\test\img\testimage.png")
    temp = ImageViewer(img)

    print(temp.histogram()[0])  # Red colour
