import sys
from PyQt5.QtWidgets import *

BUTTONS = [["1", "2", "3", "."],
           ["4", "5", "6", "+"],
           ["7", "8", "9", "-"],
           ["*", "0", "/", "="],
           ["C", "(", ")"]]


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.input_field = QLabel("")
        self.error_field = QLabel("")
        self.setup_ui()

    def setup_ui(self):
        self.setMaximumWidth(400)
        self.setStyleSheet("font-size: 20px")
        self.input_field.setStyleSheet("font-size: 24px")
        self.error_field.setStyleSheet("font-size: 16px")
        main_layout = QVBoxLayout()
        buttons_layout = QGridLayout()

        main_layout.addWidget(self.input_field)
        main_layout.addWidget(self.error_field)
        main_layout.addLayout(buttons_layout)

        for i in range(len(BUTTONS)):
            for j in range(len(BUTTONS[i])):
                button = QPushButton(str(BUTTONS[i][j]))
                button.setStyleSheet("height: 50px")

                button.clicked.connect(self.buttons_handler)
                if button.text() == "=":
                    button.setStyleSheet("height: 120px")
                    buttons_layout.addWidget(button, i, j, 2, 1)
                else:
                    buttons_layout.addWidget(button, i, j)

        self.setLayout(main_layout)

    def buttons_handler(self):
        if self.sender().text() == "=":
            try:
                self.error_field.setText("")
                self.input_field.setText(str(eval(self.input_field.text())))
            except ZeroDivisionError:
                self.input_field.setText("")
                self.error_field.setText("Error, you can't divide by zero")
            except SyntaxError:
                self.input_field.setText("")
                self.error_field.setText("Error, the expression is not correct")

        elif self.sender().text() == "C":
            self.input_field.setText("")
            self.error_field.setText("")

        else:
            self.input_field.setText(self.input_field.text() + self.sender().text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculator()
    ex.show()
    sys.exit(app.exec())
