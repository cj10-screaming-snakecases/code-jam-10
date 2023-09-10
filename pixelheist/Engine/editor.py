from PIL import Image

from pixelheist.Engine.layers import EditorLayer, LayerStack


class Editor:
    def __init__(self, layers: LayerStack, selected_index: int = -1):
        self.layers = layers
        self.selected_index = selected_index

    @property
    def selected_layer(self):
        return self.layers.layers[self.selected_index]

    def render_output(self):
        return self.layers.render_output()

    def apply_contrast(self, amount: int):
        self.selected_layer.contrast = amount

    def apply_brightness(self, amount: int):
        self.selected_layer.brightness = amount

    def apply_sharpness(self, amount: int):
        self.selected_layer.sharpness = amount

    @classmethod
    def from_image(cls, image: Image.Image):
        return cls(LayerStack([EditorLayer(image)], image.size), 0)
