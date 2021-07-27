from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from notes_ui import Ui_main_widget
from typing import *
import sqlite3
import sys


NOTES_START_INDEX = 2


def delete_button_from_list(note_id, buttons_list: List[QPushButton]):
    for i, button in enumerate(buttons_list):
        if int(button.whatsThis()) == note_id:
            buttons_list.pop(i)


def search_button(note_id, buttons_list: List[QPushButton]) -> QPushButton:
    for button in buttons_list:
        if int(button.whatsThis()) == note_id:
            return button


def clear_layout(layout: QLayout, start_index: int):
    while layout.count() > start_index:
        item = layout.itemAt(start_index)
        widget = item.widget()
        layout.removeItem(item)
        layout.removeWidget(widget)
        widget.setParent(QWidget())


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
        self.notes_buttons_list = list()
        self.next_id = 1
        self.read_all_notes()
        self.show()

    def ui_correction(self):
        self.ui.notes_list_layout.setAlignment(Qt.AlignTop)
        self.ui.create_note_button.setText("+")
        self.ui.create_note_button.setWhatsThis("0")
        self.ui.create_note_button.clicked.connect(self.open_note)
        self.ui.menu_button.clicked.connect(self.hide_menu)
        self.ui.menu_button_layout.setAlignment(Qt.AlignLeft)
        empty_edit_area = EmptyEditArea()
        self.ui.edit_area.addWidget(empty_edit_area)
        self.ui.edit_area.setCurrentWidget(empty_edit_area)
        self.ui.delete_button = QPushButton("🗑")
        self.ui.delete_button.clicked.connect(self.delete_note)
        self.ui.tool_bar_layout.addWidget(self.ui.delete_button, alignment=Qt.AlignRight)

    def closeEvent(self, a0: QCloseEvent) -> None:
        for key, value in self.opened_notes.items():
            request = """UPDATE Notes
                         SET header = "{}", body = "{}"
                         WHERE id = {}""".format(value.header_view.text(), value.body_view.toPlainText(), key)

            self.cursor.execute(request)

        self.connection.commit()

    def read_all_notes(self):
        request = """SELECT * FROM Notes"""
        response = self.cursor.execute(request).fetchall()
        for note in response:
            note = list(note)
            note_button = QPushButton(note[1])
            note_button.setWhatsThis("{}".format(note[0]))
            note_button.clicked.connect(self.open_note)
            self.ui.notes_list_layout.insertWidget(NOTES_START_INDEX, note_button)
            self.notes_buttons_list.append(note_button)

            if note[0] > self.next_id:
                self.next_id = note[0]

        self.next_id += 1

    def update_notes_list_view(self):
        for note_button in self.notes_buttons_list:
            self.ui.notes_list_layout.insertWidget(NOTES_START_INDEX, note_button)

    def open_note(self):
        note_id = int(self.sender().whatsThis())
        if note_id not in self.opened_notes.keys():
            if note_id == 0:
                note_id = self.next_id
                self.next_id += 1

                note_button = QPushButton()
                note_button.clicked.connect(self.open_note)

                note_widget = Note(note_button, note_id)

                self.ui.notes_list_layout.insertWidget(NOTES_START_INDEX, note_button)
                self.notes_buttons_list.append(note_button)

                request = """INSERT INTO Notes(id, header, body) Values({}, '', '')""".format(note_id)
                self.cursor.execute(request)

                self.connection.commit()

            else:
                request = """SELECT * FROM Notes WHERE id=?"""
                response = self.cursor.execute(request, (note_id,)).fetchone()

                note_button = search_button(note_id, self.notes_buttons_list)
                note_widget = Note(note_button, note_id, response[1], response[2], True)

            note_button.setWhatsThis("{}".format(note_id))
            self.ui.edit_area.addWidget(note_widget)
            self.opened_notes.update({note_widget.id: note_widget})
        else:
            note_widget = self.opened_notes[note_id]
            note_button = search_button(note_id, self.notes_buttons_list)

        note_widget.header_view.textChanged.connect(note_widget.note_button_update)
        self.ui.edit_area.setCurrentWidget(note_widget)

        for button in self.notes_buttons_list:
            button.setStyleSheet(open("./styles/note_button.css").read() + "}")

        note_button.setStyleSheet(open("./styles/note_button.css").read() + "\n background: rgb(3, 74, 89);\n"
                                                                            "border: 1px solid rgb(255, 255, 255);}")

    def hide_menu(self):
        if self.ui.scroll_notes_list_area.isHidden():
            self.ui.scroll_notes_list_area.show()
        else:
            self.ui.scroll_notes_list_area.hide()

    def delete_note(self) -> None:
        yes_no_dialog = QMessageBox(QMessageBox.Information, "Удалить",
                                    "Вы действительно хотите удалить эту заметку?",
                                    QMessageBox.Yes | QMessageBox.No)
        yes_no_dialog.setStyleSheet(open("./styles/QMessageBox.css").read())
        yes_no_dialog.setIcon(QMessageBox.NoIcon)

        note_id = self.ui.edit_area.currentWidget().id

        if note_id == -1:
            return

        if QMessageBox.Yes == yes_no_dialog.exec():
            self.opened_notes.pop(note_id)
            clear_layout(self.ui.notes_list_layout, NOTES_START_INDEX)
            empty_edit_area = EmptyEditArea()
            self.ui.edit_area.addWidget(empty_edit_area)
            self.ui.edit_area.setCurrentWidget(empty_edit_area)

            request = """DELETE from Notes WHERE id = ?"""
            self.cursor.execute(request, (note_id, ))
            self.connection.commit()

            self.notes_buttons_list.clear()
            self.read_all_notes()
            print(self.notes_buttons_list)


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


class EmptyEditArea(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Создайте новую заметку или откройте старую")
        self.label.setStyleSheet("color: rgb(255, 255, 255);\nfont-size: 30px;")
        self.id = -1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    sys.exit(app.exec())
