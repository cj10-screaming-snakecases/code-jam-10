"""GUI for the game."""
import sys
from PySide6 import QtCore, QtWidgets, QtGui


class MainWindow(QtWidgets.QMainWindow):
    """Create a new window."""

    def __init__(self) -> None:
        """Initialize Main Window class."""
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self) -> None:
        """Initialize the main layout and window settings."""
        self.resize(1000, 670)

        qrect = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        qrect.moveCenter(center_point)
        self.move(qrect.topLeft())

        self.setWindowTitle('The Screaming Snakecases')

        self.titleBar()
        self.menuItems()
        self.editToolBar()
        self.configurationBar()

    def titleBar(self) -> None:
        """Create the title bar."""
        tool_bar = QtWidgets.QToolBar('Title Bar')
        tool_bar.setMovable(False)
        tool_bar.setFixedHeight(35)
        self.title = QtWidgets.QLabel('Pixel Heist')

        self.title.setStyleSheet(
            'padding-left: 10px;'
            'font-family: monospace;'
            'font-size: 15px;'
            'font-weight: 550;'
            'letter-spacing: 1.2px;'

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

        grid_layout = QtWidgets.QGridLayout()
        icons = [
            'crop.png',
            'magicwand.png',
            'pen.png',
            'picktool.png',
            'resize.png',
            'zoom.png'
        ]

        for i in range(6):
            button = QtWidgets.QPushButton()
            button.setStyleSheet(
                'width:50px;'
                'height:40px;'
                'margin:-3px -25px ;'
                'background-color:lightgrey;'
                'padding-left:-2px;'
            )
            icon = QtGui.QIcon(f'icons/{icons[i]}')
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(15, 15))
            grid_layout.addWidget(button, i//1, i % 1)

        widget = QtWidgets.QWidget()
        widget.setLayout(grid_layout)
        tool_bar.addWidget(widget)

        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, tool_bar)

    def configurationBar(self) -> None:
        """Create the configuration bar."""
        tool_bar = QtWidgets.QToolBar('Configuration Bar')
        tool_bar.setStyleSheet(
            'background:lightgrey;'
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
