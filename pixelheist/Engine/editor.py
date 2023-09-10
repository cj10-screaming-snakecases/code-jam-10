from pixelheist.Engine.layers import EditorLayer, LayerStack
from pixelheist.Engine.tools import ImageTool


class Editor:
    def __init__(self, layers: LayerStack, selected_index: int = -1):
        self.layers = layers
        self.selected_index = selected_index

    @property
    def selected_layer(self):
        return self.layers.layers[self.selected_index]

    def render_output(self):
        return self.layers.render_output()

    def apply(self, tool: ImageTool, *args, **kwargs):
        self.selected_layer.apply(tool, *args, **kwargs)

    @classmethod
    def from_image(cls, image):
        return cls(LayerStack([EditorLayer(image)]), 0)
