from typing import Iterable

from PIL import Image


class Layer:
    """Represents a layer in the editor"""

    def __init__(self, image: Image.Image):
        self.im = image


class LayerStack:
    def __init__(self, layers: Iterable[Layer]):
        self.layers = list(layers)

    def add_layer(self, layer: Layer):
        self.layers.append(layer)

    def process_final_image(self):
        img = self.layers[0]
        for layer in self.layers[1:]:
            pass


if __name__ == '__main__':
    i = Image.open('../test/img/How-to-Generate-Random-Numbers-in-Python.jpg')
    l = Layer(i)
