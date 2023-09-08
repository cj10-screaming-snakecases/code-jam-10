"""GUI for the game."""
import sys
from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets


class MagnifierWidget(QtWidgets.QWidget):
    """Widget used to display Magnifier."""

    def __init__(self, image):
        """Initialize the Magnifier."""
        super().__init__()
        self.image = image
        self.zoom = 2

        self._view = QtWidgets.QGraphicsView()
        self.scene = QtWidgets.QGraphicsScene()
        self._view.setScene(self.scene)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._view)
        self.setLayout(self._layout)

        self.display_magnified_image()

    def display_magnified_image(self):
        """Magnifies the image from scale 1 - 6."""
        if self.image:
            magnified = self.image.scaled(
                self.image.width() * self.zoom,
                self.image.height() * self.zoom
            )
            pixmap = QtGui.QPixmap.fromImage(magnified)

            self.scene.clear()
            self.scene.addPixmap(pixmap)

    def update_magnified_image(self):
        """Update the image according to the slider."""
        # self.zoom = self.slider.value()
        self.display_magnified_image()


class MainWindow(QtWidgets.QMainWindow):
    """Create a new window."""

    def __init__(self) -> None:
        """Initialize Main Window class."""
        super().__init__()
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
        self.menuItems()
        self.editToolBar()
        self.configurationBar()

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
            'padding-left: 10px;'
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

    def menuItems(self) -> None:
        """Create the menu items of application and add them to toolbar."""
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction('New')
        file_menu.addAction('Open')
        file_menu.addAction('Save')
        file_menu.addAction('LogOut')
        file_menu.addAction('Exit')

        edit_menu = menubar.addMenu('Edit')
        edit_menu.addAction('Undo')
        edit_menu.addAction('Redo')
        edit_menu.addAction('Cut')
        edit_menu.addAction('Copy')

        view_menu = menubar.addMenu('View')
        view_menu.addAction('Zoom In')
        view_menu.addAction('Zoom Out')
        view_menu.addAction('Reset Zoom')

        help_menu = menubar.addMenu('Help')
        help_menu.addAction('About')

    def editToolBar(self) -> None:
        """Design the tool bar for editing to left side."""
        tool_bar = QtWidgets.QToolBar('Tool Bar')
        tool_bar.setMovable(False)
        tool_bar.setFixedWidth(60)
        tool_bar.setStyleSheet(
            'border-right: 0.5px solid black;'
        )

        gui_dir = Path(__file__).parent
        icons = [
            gui_dir / Path('icons/crop.png'),
            gui_dir / Path('icons/magicwand.png'),
            gui_dir / Path('icons/pen.png'),
            gui_dir / Path('icons/picktool.png'),
            gui_dir / Path('icons/resize.png'),
            gui_dir / Path('icons/move.png'),
            gui_dir / Path('icons/search.png'),
            gui_dir / Path('icons/brightness.png')
        ]

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.setSpacing(10)
        widget = QtWidgets.QWidget()
        widget.setStyleSheet(
            'border: none;'
        )
        widget.setLayout(vertical_layout)
        tool_bar.addWidget(widget)

        for i in range(8):
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
            icon = QtGui.QIcon(str(icons[i]))
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(15, 15))
            vertical_layout.addWidget(button)

        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, tool_bar)

    def configurationBar(self) -> None:
        """Create the configuration bar."""
        tool_bar = QtWidgets.QToolBar('Configuration Bar')
        tool_bar.setStyleSheet(
            'border-left: 0.5px solid black;'
        )
        tool_bar.setMovable(False)
        tool_bar.setFixedWidth(200)

        widget = QtWidgets.QWidget()
        tool_bar.addWidget(widget)

        self.addToolBar(QtCore.Qt.ToolBarArea.RightToolBarArea, tool_bar)


def main() -> None:
    """Entry Point."""
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
