"""GUI for the game."""
import sys
from PySide6 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    """Main Window class."""

    def __init__(self) -> None:
        """Initialize Main Window class."""
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self) -> None:
        """Initialize GUI elements."""
        self.resize(1000, 700)

        qrect = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        qrect.moveCenter(center_point)
        self.move(qrect.topLeft())

        self.setWindowTitle('cj10-screaming-snakecases')

        self.setStyleSheet('background: #efefef;')

        self.addToolBar(
            QtCore.Qt.ToolBarArea.LeftToolBarArea,
            self.left_bar()
        )
        self.addToolBar(
            QtCore.Qt.ToolBarArea.TopToolBarArea,
            self.top_bar()
        )
        self.addToolBar(
            QtCore.Qt.ToolBarArea.RightToolBarArea,
            self.right_bar()
        )

    def left_bar(self) -> QtWidgets.QToolBar:
        """Create and return a QToolBar for selecting tools on the left."""
        tool_bar = QtWidgets.QToolBar('Tool Bar')
        tool_bar.setMovable(False)
        tool_bar.setFixedWidth(40)
        tool_bar.setStyleSheet(
            'background: #ffffff;'
            'border-right: 0.5px solid #d8d8d8;'
        )

        return tool_bar

    def top_bar(self) -> QtWidgets.QToolBar:
        """Create and return a QToolBar for displaying title on the top."""
        tool_bar = QtWidgets.QToolBar('Title bar')
        tool_bar.setMovable(False)
        tool_bar.setFixedHeight(35)
        tool_bar.setStyleSheet(
            'background: #ffffff;'
            'border-bottom: 0.5px solid #e0e0e0;'
        )

        self.title = QtWidgets.QLabel('placeholder')
        self.title.setStyleSheet(
            'font-family: monospace;'
            'font-size: 15px;'
            'font-weight: 550;'
            'letter-spacing: 1.2px;'
        )

        left_spacer = QtWidgets.QWidget()
        left_spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred
        )
        right_spacer = QtWidgets.QWidget()
        right_spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred
        )

        tool_bar.addWidget(left_spacer)
        tool_bar.addWidget(self.title)
        tool_bar.addWidget(right_spacer)

        return tool_bar

    def right_bar(self) -> QtWidgets.QToolBar:
        """Create and return a QToolBar for configuration on the right."""
        tool_bar = QtWidgets.QToolBar('Configuration Bar')
        tool_bar.setMovable(False)
        tool_bar.setFixedWidth(175)
        tool_bar.setStyleSheet(
            'background: #ffffff;'
            'border-left: 0.5px solid #d8d8d8;'
        )

        return tool_bar


def main() -> None:
    """Entry Point."""
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
