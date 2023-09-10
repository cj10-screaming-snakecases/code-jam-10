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
