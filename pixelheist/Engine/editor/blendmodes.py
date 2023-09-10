from typing import Callable, Any

import numpy as np
from PIL import Image

# Blend modes take 2 images (the base and the new image), and returns a new image
# The base image may be modified in the process
ImageArray = np.ndarray[Any, np.uint8]

BlendMode = Callable[[ImageArray, ImageArray], ImageArray]


def none(base: ImageArray, new: ImageArray) -> ImageArray:
    base = Image.fromarray(base)
    new = Image.fromarray(new)
    base.paste(new)
    return np.asarray(base)  # type: ignore


def multiply(base: ImageArray, new: ImageArray) -> ImageArray:
    return base * new // 255
