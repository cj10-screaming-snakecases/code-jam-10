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

        self.setStyleSheet('background: #efefef;')

        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, self.left_bar())
        self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.top_bar())
        self.addToolBar(QtCore.Qt.ToolBarArea.RightToolBarArea, self.right_bar())

    def left_bar(self) -> QtWidgets.QToolBar:
        tool_bar = QtWidgets.QToolBar('Tool Bar')
        tool_bar.setMovable(False)
        tool_bar.setFixedWidth(40)
        tool_bar.setStyleSheet(
            'background: #ffffff;'
            'border-right: 0.5px solid #d8d8d8;'
        )

        return tool_bar

    def top_bar(self) -> QtWidgets.QToolBar:
        tool_bar = QtWidgets.QToolBar('placeholder')
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
        left_spacer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        right_spacer = QtWidgets.QWidget()
        right_spacer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)

        tool_bar.addWidget(left_spacer)
        tool_bar.addWidget(self.title)
        tool_bar.addWidget(right_spacer)

        return tool_bar

    def right_bar(self) -> QtWidgets.QToolBar:
        tool_bar = QtWidgets.QToolBar('Configuration Bar')
        tool_bar.setMovable(False)
        tool_bar.setFixedWidth(175)
        tool_bar.setStyleSheet(
            'background: #ffffff;'
            'border-left: 0.5px solid #d8d8d8;'
        )

        return tool_bar

def main() -> None:
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()