from dataclasses import dataclass
from typing import Iterable

import numpy as np
from PIL import Image, ImageQt

from pixelheist.Engine import blendmodes
from pixelheist.Engine.tools import brightness, contrast, sharpness

ImageType = Image.Image


class LayerIsLocked(Exception):
    pass


@dataclass
class EditorLayer:
    image: ImageType
    blend_mode: blendmodes.BlendMode = blendmodes.none
    locked: bool = False
    modified: bool = False
    _contrast: int = 0
    _brightness: int = 0
    _sharpness: int = 0

    @property
    def contrast(self):
        return self._contrast

    @contrast.setter
    def contrast(self, value):
        self._contrast = value
        self.modified = True

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value
        self.modified = True

    @property
    def sharpness(self):
        return self._sharpness

    @sharpness.setter
    def sharpness(self, value):
        self._sharpness = value
        self.modified = True

    def render(self):
        out_img = self.image
        for tool, amount in [
            (brightness, self._brightness),
            (contrast, self._contrast),
            (sharpness, self._sharpness),
        ]:
            if amount == 0:
                continue
            out_img = tool(out_img, amount)
        return out_img

    @classmethod
    def from_dict(cls, data):
        return cls(
            Image.open(data['filepath']),
            getattr(blendmodes, data['blend_mode']),
            data['locked']
        )


class LayerStack:
    def __init__(self, layers: Iterable[EditorLayer], size: tuple[int, int] | None = None):
        self.layers = list(layers)
        if size is None:
            size = self.layers[0].image.size
        self.size = size
        self._cached_output: ImageQt.ImageQt | None = None

    def render_output(self) -> ImageQt.ImageQt:
        # Use cached output
        if not any(layer.modified for layer in self.layers) \
                and self._cached_output is not None:
            return self._cached_output

        image_array = np.zeros(self.size + (4,), dtype=np.uint8)
        for layer in self.layers:
            layer_image = np.asarray(layer.render())
            image_array = layer.blend_mode(image_array, layer_image)  # type: ignore

        image = ImageQt.ImageQt(Image.fromarray(image_array))
        self._cached_output = image
        return image
