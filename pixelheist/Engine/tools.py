# This file contains the class ImageTools that should be able to take in any image (as a 2D pixel array)
# and return another 2D pixel array according to what is called. Any other to be added in time should be able
# to be added here easily.
# However, if an Image object is more desired over a np array, it will need to be changd in the future.

from typing import Callable

import numpy as np
from PIL import Image, ImageEnhance

ImageType = Image.Image

ImageTool = Callable[[ImageType, ...], ImageType]


def tool_from_enhancer(enhancer) -> ImageTool:
    def wrapper(image: ImageType, amount: int) -> ImageType:
        # Amount is -100 ~ 100, scale to match 0 ~ 2
        factor = (amount / 100) + 1
        e = enhancer(image)
        return e.enhance(factor)

    return wrapper


contrast = tool_from_enhancer(ImageEnhance.Contrast)

brightness = tool_from_enhancer(ImageEnhance.Brightness)

sharpness = tool_from_enhancer(ImageEnhance.Sharpness)


def zoom(image: ImageType, scale: float) -> ImageType:
    w, h = image.size
    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = Image.fromarray(image.resize((new_w, new_h)))

    return resized


def color_channel(image: ImageType, channel: str) -> ImageType:
    # channel = RGB(A)
    color_id = 'RGBA'.index(channel)

    im_arr = np.asarray(image)
    h, w, channels = im_arr.shape

    filtered_image = np.zeros((h, w, channels))
    filtered_image[:, :, color_id] = im_arr[:, :, color_id]

    return Image.fromarray(filtered_image)


class ImageTools:
    def __init__(self, image: ImageType) -> None:
        self.image = image
        self.imArray = np.asarray(image)
        self.ROI = self.imArray.copy()

    def set_ROI(self, x, y, w, h):
        # Sets a Region Of Interest (ROI). This is useful for when we only want to zoom in on
        # a portion of the image for displaying, etc. By default, ROI = entire image

        self.ROI = self.imArray[y: y + h, x: x + w]

    def zoom(self, scale: float) -> ImageType:
        h, w, _ = self.imArray.shape
        new_w = int(w * scale)
        new_h = int(h * scale)

        resized = Image.fromarray(self.ROI.resize((new_w, new_h)))

        return resized

    def contrast(self, factor: float) -> ImageType:
        # 0 < factor < 1: Decrease contrast
        # factor = 1: No change
        # factor > 1: Increase contrast

        temp = self.ROI

        enhancer = ImageEnhance.Contrast(temp)
        contrasted_image = enhancer.enhance(factor)

        return contrasted_image

    def brightness(self, brightness: float) -> ImageType:
        # 0 < brightness < 1: Decrease contrast
        # brightness = 1: No change
        # brightness > 1: Increase brightness

        temp = self.ROI

        enhancer = ImageEnhance.Brightness(temp)
        brightened_image = enhancer.enhance(brightness)

        return brightened_image

    def sharpness(self, sharpness: float) -> ImageType:
        # 0 < sharpness < 1: Decrease sharpness
        # sharpness = 1: No change
        # sharpness > 1: Increase sharpness

        temp = Image.fromarray(self.ROI)

        enhancer = ImageEnhance.Sharpness(temp)
        sharpened_image = enhancer.enhance(sharpness)

        return sharpened_image

    def color_channel(self, channel: str) -> ImageType:
        # channel = RGB(A)
        colorID = 'RGBA'.index(channel)

        h, w, channels = self.image.shape

        filtered_image = np.zeros((h, w, channels))
        filtered_image[:, :, colorID] = self.imArray[:, :, colorID]

        return Image.fromarray(filtered_image)