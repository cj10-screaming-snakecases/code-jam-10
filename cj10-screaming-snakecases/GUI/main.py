import sys
from PySide6 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_UI()

    def initialize_UI(self) -> None:
        self.resize(1000, 700)

        qrect = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        qrect.moveCenter(center_point)
        self.move(qrect.topLeft())

        self.setWindowTitle('cj10-screaming-snakecases')

        self.top_bar()
        self.left_bar()

    def left_bar(self) -> None:
        tool_bar = QtWidgets.QToolBar('Tool Bar')
        tool_bar.setMovable(False)
        tool_bar.setFixedWidth(40)

        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, tool_bar)

    def top_bar(self) -> None:
        tool_bar = QtWidgets.QToolBar('placeholder')
        tool_bar.setMovable(False)
        tool_bar.setFixedHeight(35)

        self.title = QtWidgets.QLabel('placeholder')
        self.title.setStyleSheet(
            'padding-left: 10px;'
            'font-family: monospace;'
            'font-size: 15px;'
            'font-weight: 550;'
            'letter-spacing: 1.2px;'
        )

        tool_bar.addWidget(self.title)

        self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, tool_bar)

def main() -> None:
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()