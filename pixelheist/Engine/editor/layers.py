from dataclasses import dataclass
from typing import Iterable

import numpy as np
from PIL import Image, ImageQt

from pixelheist.Engine.editor import blendmodes
from pixelheist.Engine.editor.tools import ImageTool

ImageType = Image.Image


class LayerIsLocked(Exception):
    pass


@dataclass
class EditorLayer:
    image: ImageType
    blend_mode: blendmodes.BlendMode = blendmodes.none
    locked: bool = False
    modified: bool = False

    def apply(self, func: ImageTool, *args, **kwargs) -> None:
        if self.locked:
            raise LayerIsLocked
        self.image = func(self.image, *args, **kwargs)
        self.modified = True


class LayerStack:
    def __init__(self, layers: Iterable[EditorLayer]):
        self.layers = list(layers)
        self._cached_output: ImageQt.ImageQt | None = None

    def render_output(self) -> ImageQt.ImageQt:
        # Use cached output
        if not any(layer.modified for layer in self.layers) \
                and self._cached_output is not None:
            return self._cached_output

        image_array = np.zeros([800, 800, 4], dtype=np.uint8)
        for layer in self.layers:
            layer_image = np.asarray(layer.image)
            image_array = layer.blend_mode(image_array, layer_image)  # type: ignore

        image = ImageQt.ImageQt(Image.fromarray(image_array))
        self._cached_output = image
        return image
