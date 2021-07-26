from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from notes_ui import Ui_main_widget
import sqlite3
import sys

SELECTED_NOTE_COLOR = 'rgb(3, 74, 89)'
UNSELECTED_NOTE_COLOR = 'rgb(10, 70, 83)'


class MainWidget(QWidget):
    def __init__(self, db_name="notes.db"):
        super().__init__(flags=Qt.Window)
        self.setWindowState(Qt.WindowMaximized)
        self.ui = Ui_main_widget()
        self.ui.setupUi(self)
        self.ui_correction()
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.opened_notes = dict()
        self.notes = list()
        self.next_id = 1
        self.read_all_notes()
        self.show()

    def ui_correction(self):
        self.ui.notes_list_layout.setAlignment(Qt.AlignTop)
        self.ui.create_note_button.setText("+")
        self.ui.create_note_button.setWhatsThis("0")
        self.ui.create_note_button.clicked.connect(self.open_note)

    def closeEvent(self, a0: QCloseEvent) -> None:
        for key, value in self.opened_notes.items():
            if value.update:
                request = """UPDATE Notes
                         SET header = "{}", body = "{}"
                         WHERE id = {}""".format(value.header_view.text(), value.body_view.toPlainText(), key)
            else:
                request = """INSERT INTO Notes(id, header, body) VALUES({}, "{}", "{}")"""\
                          .format(key, value.header_view.text(), value.body_view.toPlainText())

            self.cursor.execute(request)

        self.connection.commit()

    def read_all_notes(self):
        request = """SELECT * FROM Notes"""
        response = self.cursor.execute(request).fetchall()
        self.next_id = len(response) + 1
        for note in response:
            note = list(note)
            note_button = QPushButton(note[1])
            note_button.setWhatsThis("{}".format(note[0]))
            note_button.clicked.connect(self.open_note)
            self.ui.notes_list_layout.insertWidget(1, note_button)
            self.notes.append(note_button)

    def open_note(self):
        note_id = int(self.sender().whatsThis())
        if note_id not in self.opened_notes.keys():
            if note_id == 0:
                note_button = QPushButton()
                note_widget = Note(note_button)
                note_button.setWhatsThis("{}".format(self.next_id))
                self.next_id += 1
                note_button.clicked.connect(self.open_note)
                self.ui.notes_list_layout.insertWidget(1, note_button)
                self.notes.append(note_button)

            else:
                request = """SELECT * FROM Notes WHERE id=?"""
                response = self.cursor.execute(request, (note_id, )).fetchone()
                note_button = self.ui.notes_list_layout.itemAt(self.next_id - note_id).widget()
                note_widget = Note(note_button, note_id, response[1], response[2], True)

            self.ui.edit_area.addWidget(note_widget)
            self.opened_notes.update({note_widget.id: note_widget})
        else:
            note_widget = self.opened_notes[note_id]
            note_button = self.ui.notes_list_layout.itemAt(self.next_id - note_id).widget()
        note_widget.header_view.textChanged.connect(note_widget.note_button_update)
        self.ui.edit_area.setCurrentWidget(note_widget)

        for button in self.notes:
            button.setStyleSheet(open("./styles/note_button.css").read() + "}")

        note_button.setStyleSheet(open("./styles/note_button.css").read() + "\n background: rgb(3, 74, 89);\n"
                                                                            "border: 1px solid rgb(255, 255, 255);}")

    # def sync_with_db(self):


class Note(QWidget):
    def __init__(self, note_button: QPushButton, note_id=0, header="", text="", update=False):
        super().__init__()
        self.header_view = QLineEdit()
        self.body_view = QTextEdit()
        self.layout = QVBoxLayout()
        self.id = note_id
        self.update = update
        self.note_button = note_button

        self.setup_widgets(header, text)

    def setup_widgets(self, header, text):
        if header == "":
            self.header_view.setPlaceholderText("Header here...")
            self.header_view.setMaxLength(50)
        else:
            self.header_view.setText(header)

        if text == "":
            self.body_view.setPlaceholderText("Type here...")
        else:
            self.body_view.setText(text)
        self.layout.addWidget(self.header_view)
        self.layout.addWidget(self.body_view)

        self.setLayout(self.layout)

    def note_button_update(self):
        if len(self.header_view.text()) < 16:
            self.note_button.setText(self.header_view.text())
        else:
            self.note_button.setText(self.header_view.text()[:13] + "...")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    sys.exit(app.exec())
