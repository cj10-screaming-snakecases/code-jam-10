from typing import Any, Callable

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


def screen(base: ImageArray, new: ImageArray) -> ImageArray:
    return 255 - (255 - base) * (255 - new) // 255


def overlay(base: ImageArray, new: ImageArray) -> ImageArray:
    result = base * new // 255
    result[base >= 128] = 255 - (255 - base) * (255 - new) // 255
    return result * 2


def difference(base: ImageArray, new: ImageArray) -> ImageArray:
    result = base - new
    result[new > base] = new - base
    return result


def color_dodge(base: ImageArray, new: ImageArray) -> ImageArray:
    return base // (255 - new)


def color_burn(base: ImageArray, new: ImageArray) -> ImageArray:
    return 255 - (255 - base) / new


darken_only: BlendMode = np.minimum

lighten_only: BlendMode = np.maximum
