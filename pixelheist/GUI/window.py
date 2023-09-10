"""GUI for the game."""
import sys
from pathlib import Path

from PIL import Image
from PySide6 import QtCore, QtGui, QtWidgets

from pixelheist.Engine import Editor

# from ..Engine.editor.ImageTools import ImageTools

# class MagnifierWidget(QtWidgets.QWidget):
#     """Widget used to display Magnifier."""

#     def __init__(self, image):
#         """Initialize the Magnifier."""
#         super().__init__()
#         self.image = image
#         self.zoom = 2
#         self.slider = None

#         self._view = QtWidgets.QGraphicsView()
#         self.scene = QtWidgets.QGraphicsScene()
#         self._view.setScene(self.scene)

#         self._layout = QtWidgets.QVBoxLayout()
#         self._layout.addWidget(self._view)
#         self.setLayout(self._layout)

#         self.display_magnified_image()

#     def display_magnified_image(self) -> None:
#         """Magnifies the image from scale 1 - 6."""
#         if self.image:
#             magnified = self.image.scaled(
#                 self.image.width() * self.zoom,
#                 self.image.height() * self.zoom
#             )
#             pixmap = QtGui.QPixmap.fromImage(magnified)

#             self.scene.clear()
#             self.scene.addPixmap(pixmap)

#     def update_magnified_image(self) -> None:
#         """Update the image according to the slider."""
#         self.zoom = self.slider.value()
#         self.display_magnified_image()


class MainWindow(QtWidgets.QMainWindow):
    """Create a new window."""

    def __init__(self) -> None:
        """Initialize Main Window class."""
        super().__init__()
        self.editor_engine = Editor.from_image(
            Image.open("pixelheist/Engine/test/img/testimage.png")
        )

        self.initUI()

    def initUI(self) -> None:
        """Initialize the main layout and window settings."""
        self.resize(1000, 670)

        qrect = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        qrect.moveCenter(center_point)
        self.move(qrect.topLeft())

        self.setWindowTitle('Pixel Heist - CJ10 The Screaming Snakecases')

        self.titleBar()
        self.editToolBar()
        self.imagePreview()

    def imagePreview(self) -> None:
        label = QtWidgets.QLabel()
        label.setPixmap(QtGui.QPixmap.fromImage(self.editor_engine.render_output()))
        self.setCentralWidget(label)

    def titleBar(self) -> None:
        """Create the title bar."""
        tool_bar = QtWidgets.QToolBar('Title Bar')
        tool_bar.setMovable(False)
        tool_bar.setFixedHeight(35)
        tool_bar.setStyleSheet(
            'border-bottom: 0.5px solid black;'
        )
        self.title = QtWidgets.QLabel('Pixel Heist')

        self.title.setStyleSheet(
            'font-family: monospace;'
            'font-size: 15px;'
            'font-weight: 550;'
            'letter-spacing: 1.2px;'
            'background: transparent;'
            'border: none;'
        )

        left_padding = QtWidgets.QWidget()
        left_padding.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred
        )
        right_padding = QtWidgets.QWidget()
        right_padding.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred
        )
        left_padding.setStyleSheet('border: none;')
        right_padding.setStyleSheet('border: none;')

        tool_bar.addWidget(left_padding)
        tool_bar.addWidget(self.title)
        tool_bar.addWidget(right_padding)
        self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, tool_bar)

    def editToolBar(self) -> None:
        """Design the tool bar for editing to left side."""
        tool_bar = QtWidgets.QToolBar('Tool Bar')
        tool_bar.setMovable(False)
        tool_bar.setFixedWidth(60)
        tool_bar.setStyleSheet(
            'border-right: 0.5px solid black;'
        )

        gui_dir = Path(__file__).parent
        button_assests = [
            (gui_dir / 'icons/zoom.png', self.magnifier),
            (gui_dir / 'icons/hand.png', self.hand),
            (gui_dir / 'icons/properties.png', self.configurationBar)
        ]

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.setSpacing(10)
        widget = QtWidgets.QWidget()
        widget.setStyleSheet(
            'border: none;'
        )
        widget.setLayout(vertical_layout)
        tool_bar.addWidget(widget)

        for icon_path, action in button_assests:
            button = QtWidgets.QPushButton()
            button.setStyleSheet(
                """
                QPushButton {
                    width: 50px;
                    height: 37px;
                    background: #e0e0e0;
                    border: 1.5px solid black;
                    border-radius: 8px;
                    margin-left: 1px;
                }
                QPushButton:hover {
                    background: #ebebeb;
                }
                """
            )
            icon = QtGui.QIcon(str(icon_path))
            button.setIcon(icon)
            button.clicked.connect(action)
            button.setIconSize(QtCore.QSize(20, 20))
            vertical_layout.addWidget(button)

        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, tool_bar)

    def configurationBar(self) -> None:
        """Create the configuration bar."""
        tool_bar = QtWidgets.QToolBar('Configuration Bar')
        tool_bar.setObjectName('conf_bar')
        tool_bar.setStyleSheet(
            'border-left: 0.5px solid black;'
        )
        tool_bar.setMovable(False)
        tool_bar.setFixedWidth(252)

        config_widget = QtWidgets.QWidget()
        config_widget.setStyleSheet(
            'border: none'
        )
        config_layout = QtWidgets.QVBoxLayout()
        config_widget.setLayout(config_layout)

        tool_bar.addWidget(config_widget)

        self.addToolBar(QtCore.Qt.ToolBarArea.RightToolBarArea, tool_bar)

        def sliderFunc(func, value_text: QtWidgets.QLabel, slider):
            def value_changer():
                value_text.setText(str(slider.value()))
                print(slider.value())
                # self.img = func(slider.value())
            return value_changer

        def createSlider(
            name: str,
            func
        ):
            slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
            slider.setRange(-100, 100)
            slider.setStyleSheet(
                """
                QSlider::groove:horizontal {
                    border: 1px solid #999999;
                    background: #dddddd;
                }

                QSlider::handle:horizontal {
                    background: #337ab7;
                    width: 5px;
                    border: 1px solid #2e6da4;
                }
                """
            )
            slider.setFixedWidth(233)

            name_label = QtWidgets.QLabel(name)
            name_label.setStyleSheet(
                'font-family: monospace;'
                'font-size: 15px;'
                'font-weight: 550;'
                'background: transparent;'
            )
            name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

            text_value = QtWidgets.QLabel('0')
            text_value.setStyleSheet(
                'font-family: monospace;'
                'font-size: 15px;'
                'font-weight: 550;'
                'background: transparent;'
            )
            text_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

            labels_layout = QtWidgets.QHBoxLayout()

            labels_layout.addWidget(name_label)
            labels_layout.addWidget(text_value)

            config_layout.addLayout(labels_layout)
            config_layout.addWidget(slider)

            slider.valueChanged.connect(sliderFunc(func, text_value, slider))

        # createSlider('Contrast', self.img.zoom)
        # createSlider('Brightness', self.img.zoom)
        # createSlider('Sharpness', self.img.zoom)

    def hand(self) -> None:
        pass

    def magnifier(self) -> None:
        pass


def main() -> None:
    """Entry Point."""
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
