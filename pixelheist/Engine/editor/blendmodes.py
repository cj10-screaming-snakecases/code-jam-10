from typing import Callable

import numpy as np
from PIL import Image

# Blend modes take 2 images (the base and the new image), and returns a new image
# The base image may be modified in the process
BlendMode = Callable[[Image.Image, Image.Image], Image.Image]


def none(base: Image.Image, new: Image.Image) -> Image.Image:
    base.paste(new)
    return base


def multiply(base: Image.Image, new: Image.Image) -> Image.Image:
    base = np.asarray(base)
    new = np.asarray(new)
    result = base * new // 255
    return Image.fromarray(result)
