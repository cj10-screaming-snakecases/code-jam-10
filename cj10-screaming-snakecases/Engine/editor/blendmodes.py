__all__ = [
    "BlendMode",
    "default",
    "multiply",
    "screen",
    "overlay",
    "darken_only",
    "lighten_only",
]

from functools import wraps
from typing import Callable

import numpy as np
from PIL import Image

ImageType = Image.Image

BlendMode = Callable[[ImageType, ImageType], ImageType]


def _numpy_to_image(func) -> BlendMode:  # utility decorator for using numpy arrays instead
    @wraps(func)
    def wrapper(image1: ImageType, image2: ImageType) -> ImageType:
        arr1 = np.asarray(image1)
        arr2 = np.asarray(image2)
        out_arr = func(arr1, arr2)
        return Image.fromarray(out_arr)
    return wrapper


# https://en.wikipedia.org/wiki/Blend_modes


def default(image1: ImageType, image2: ImageType) -> ImageType:
    """Default option (no blending). Simply pastes one image on the other."""
    image1.paste(image2)
    return image1


@_numpy_to_image
def multiply(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """Multiply blend mode. Pixel values (normalized to 0-1) are multiplied."""
    return arr1 * arr2 // 255


@_numpy_to_image
def screen(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """Screen blend mode. Similar to multiply, but the multiplication is applied in the inverse way."""
    return 255 - ((255 - arr1) * (255 - arr2) // 255)


@_numpy_to_image
def overlay(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """Overlay blend mode. Uses multiply for darker base pixels, and screen for lighter base pixels."""
    multiply_base = (arr1 * arr2 // 255) * 2
    screen_base = 255 - 2 * ((255 - arr1) * (255 - arr2) // 255)

    out_arr = multiply_base  # start with multiply, then overlay the screen
    out_arr[arr1 >= 128] = screen_base
    return out_arr


@_numpy_to_image
def darken_only(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """Darken only blend mode. Picks the darkest value for each pixel"""
    return np.min(arr1, arr2)


@_numpy_to_image
def lighten_only(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """Lighten only blend mode. Picks the lightest value for each pixel"""
    return np.max(arr1, arr2)
