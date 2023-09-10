from dataclasses import dataclass
from typing import Iterable

import numpy as np
from PIL import Image, ImageQt

from pixelheist.Engine.editor import blendmodes

ImageType = Image.Image


@dataclass
class EditorLayer:
    image: ImageType
    blend_mode: blendmodes.BlendMode = blendmodes.none
    locked: bool = False
    modified: bool = False


class LayerStack:
    def __init__(self, layers: Iterable[EditorLayer]):
        self.layers = list(layers)
        self._cached_output: ImageQt.ImageQt | None = None

    def get_final_image(self) -> ImageQt.ImageQt:
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
