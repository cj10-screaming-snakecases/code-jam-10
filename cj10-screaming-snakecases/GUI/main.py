import sys

from PySide6 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    """Create a new window"""

    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()

    def initialize_UI(self) -> None:
        """Initializes the main layout"""
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
        """Creates title bar"""
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

    def menuItems(self):
        """Creates menu items of application"""
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
        """Design the tool bar for editing to left side"""
        tool_bar = QtWidgets.QToolBar('Tool Bar')
        tool_bar.setMovable(False)
        tool_bar.setFixedWidth(50)

        grid_layout = QtWidgets.QGridLayout()

        for i in range(6):
            button = QtWidgets.QPushButton()
            button.setStyleSheet(
                'width:100%;'
                'height:10px;'
            )
            icon = QtGui.QIcon(f'icons/img{i}.png')
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(15, 15))
            grid_layout.addWidget(button, i//1, i % 1)

        widget = QtWidgets.QWidget()
        widget.setLayout(grid_layout)
        tool_bar.addWidget(widget)

        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, tool_bar)

    def configurationBar(self) -> None:
        """Design the configuration bar to right side"""
        tool_bar = QtWidgets.QToolBar('Configuration Bar')
        tool_bar.setStyleSheet(
            'background:grey;'
        )
        tool_bar.setMovable(False)
        tool_bar.setFixedWidth(200)

        widget = QtWidgets.QWidget()
        tool_bar.addWidget(widget)

        self.addToolBar(QtCore.Qt.ToolBarArea.RightToolBarArea, tool_bar)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
