import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QTextBrowser,
    QHBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout
)


class HtmlEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.editor = QPlainTextEdit()
        self.viewer = QTextBrowser()

        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(0, 0, 800, 800)
        main_layout = QVBoxLayout()
        layout = QHBoxLayout()
        layout.addWidget(self.editor)
        layout.addWidget(self.viewer)
        main_layout.addLayout(layout)
        button = QPushButton("run")
        button.clicked.connect(lambda: self.viewer.setText(self.editor.toPlainText()))
        main_layout.addWidget(button)
        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HtmlEditor()
    ex.show()
    sys.exit(app.exec())
