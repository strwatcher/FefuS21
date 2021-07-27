from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from notes_ui import Ui_main_widget
from typing import *
from functools import partial
import hashlib
import sqlite3
import sys
import os
from os.path import expanduser
INDEX_WHERE_NOTES_START = 1
NORMAL_STATE = 1
DELETED_STATE = 2
SECURED_STATE = 3
SHOWED_HEADER_LEN = 20
HEADER_MAX_LEN = 50

NOTE_ID_INDEX = 0
NOTE_HEADER_INDEX = 1
NOTE_BODY_INDEX = 2
NOTE_STATE_INDEX = 3

APP_ENV = expanduser('~') + '/.NOtes'
DB_PATH = APP_ENV + '/NOtes.db'
PASS_FILE_PATH = APP_ENV + '/password.txt'


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


def get_password():
    password_hash = open("password.txt", 'r').read()
    if password_hash.strip() == "":
        return None
    return password_hash


class MainWidget(QWidget):
    def __init__(self):
        super().__init__(flags=Qt.Window)
        self.setWindowState(Qt.WindowMaximized)

        self.empty_edit_area = QWidget()

        self.db = DataBase()

        self.opened_notes = dict()
        self.notes_buttons_list = list()
        self.next_id = 1

        self.ui = Ui_main_widget()
        self.ui.setupUi(self)
        self.ui_correction()

        self.cur_state = NORMAL_STATE
        self.tool_bars = {NORMAL_STATE: self.ui.normal_tool_bar, SECURED_STATE: self.ui.secured_tool_bar}

        self.read_all_notes()
        self.show()

    def ui_correction(self):
        self.ui.notes_list_layout.setAlignment(Qt.AlignTop)

        self.ui.create_note_button.setText("+")
        self.ui.create_note_button.setWhatsThis("0")
        self.ui.create_note_button.clicked.connect(self.open_note)

        self.ui.menu_button.clicked.connect(self.hide_menu)
        self.ui.menu_button_layout.setAlignment(Qt.AlignLeft)

        self.ui.edit_area.addWidget(self.empty_edit_area)
        self.ui.edit_area.setCurrentWidget(self.empty_edit_area)

        self.ui.delete_button.clicked.connect(self.delete_note)
        switch_to_secured_state = partial(self.change_state, SECURED_STATE)
        self.ui.closed_storage_button.clicked.connect(switch_to_secured_state)
        move_note_to_closed_storage = partial(self.move_note_to_some_storage, SECURED_STATE)
        self.ui.add_to_closed_button.clicked.connect(move_note_to_closed_storage)
        self.ui.normal_tool_bar_layout.setAlignment(Qt.AlignRight)

        self.ui.delete_button_2.clicked.connect(self.delete_note)
        switch_to_default_state = partial(self.change_state, NORMAL_STATE)
        move_note_to_default_storage = partial(self.move_note_to_some_storage, NORMAL_STATE)
        self.ui.remove_from_closed_button.clicked.connect(move_note_to_default_storage)
        self.ui.default_storage_button.clicked.connect(switch_to_default_state)
        self.ui.secured_tool_bar_layout.setAlignment(Qt.AlignRight)
        self.ui.stacked_tool_bar.setCurrentWidget(self.ui.normal_tool_bar)

        self.ui.search_line.setAlignment(Qt.AlignBaseline)
        self.ui.search_line.textChanged.connect(self.search_some_notes)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.sync_with_db()

    def read_notes(self, request):
        self.notes_buttons_list.clear()
        clear_layout(self.ui.notes_list_layout, INDEX_WHERE_NOTES_START)
        response = self.db.cursor.execute(request).fetchall()
        for note in response:
            note = list(note)
            note_button = QPushButton(note[NOTE_HEADER_INDEX])
            note_button.setWhatsThis("{}".format(note[NOTE_ID_INDEX]))
            note_button.clicked.connect(self.open_note)
            self.ui.notes_list_layout.insertWidget(INDEX_WHERE_NOTES_START, note_button)
            self.notes_buttons_list.append(note_button)
            if note[NOTE_ID_INDEX] in self.opened_notes.keys():
                self.opened_notes[note[NOTE_ID_INDEX]].note_button = note_button
        return response

    def read_all_notes(self):
        request = """SELECT * FROM Notes WHERE state = {}""".format(self.cur_state)
        response = self.read_notes(request)
        for note in response:
            note = list(note)
            if note[NOTE_ID_INDEX] > self.next_id:
                self.next_id = note[NOTE_ID_INDEX]

        self.next_id += 1

    def search_some_notes(self):
        request = """SELECT * FROM Notes WHERE header like '{}%' AND  state = {}""" \
            .format(self.ui.search_line.text(), self.cur_state)
        self.read_notes(request)

    def update_notes_list_view(self):
        for note_button in self.notes_buttons_list:
            self.ui.notes_list_layout.insertWidget(INDEX_WHERE_NOTES_START, note_button)

    def open_note(self):
        note_id = int(self.sender().whatsThis())
        if note_id not in self.opened_notes.keys():
            if note_id == 0:
                note_id = self.next_id
                self.next_id += 1

                header = self.ui.search_line.text()
                note_button = QPushButton(header)
                note_button.clicked.connect(self.open_note)

                note_widget = Note(note_button, note_id, header)

                self.ui.notes_list_layout.insertWidget(INDEX_WHERE_NOTES_START, note_button)
                self.notes_buttons_list.append(note_button)
                request = """INSERT INTO Notes(id, header, body, state) Values({}, '{}', '', {})""" \
                    .format(note_id, header, self.cur_state)
                self.db.cursor.execute(request)

                self.db.connection.commit()

            else:
                request = """SELECT * FROM Notes WHERE id=?"""
                response = self.db.cursor.execute(request, (note_id,)).fetchone()

                note_button = search_button(note_id, self.notes_buttons_list)
                note_widget = Note(note_button, note_id, response[NOTE_HEADER_INDEX], response[NOTE_BODY_INDEX])

            note_button.setWhatsThis("{}".format(note_id))
            self.ui.edit_area.addWidget(note_widget)
            self.opened_notes.update({note_widget.id: note_widget})
        else:
            note_widget = self.opened_notes[note_id]
            note_button = search_button(note_id, self.notes_buttons_list)

        note_widget.header_view.textChanged.connect(note_widget.note_button_update)
        note_widget.header_view.textChanged.connect(self.sync_with_db)
        note_widget.body_view.textChanged.connect(self.sync_with_db)
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
            self.ui.edit_area.setCurrentWidget(self.empty_edit_area)

            request = """DELETE from Notes WHERE id = ?"""
            self.db.cursor.execute(request, (note_id,))
            self.db.connection.commit()

            self.read_all_notes()

    def move_note_to_some_storage(self, storage_state):
        note_id = self.ui.edit_area.currentWidget().id
        request = """UPDATE Notes SET state = {} WHERE id = {}""".format(storage_state, note_id)
        self.db.cursor.execute(request)
        self.db.connection.commit()
        self.search_some_notes()
        self.ui.edit_area.setCurrentWidget(self.empty_edit_area)

    def change_state(self, state):
        if state == SECURED_STATE:

            if not self.db.password:
                i, ok_pressed = QInputDialog.getText(self, "Придумайте пароль",
                                                     "Чтобы пользоваться закрытым хранилищем,"
                                                     " необходимо создать пароль")
                if ok_pressed:
                    self.db.password = hashlib.sha1(bytes(i.strip(), encoding='utf-8')).hexdigest()
                    open(PASS_FILE_PATH, 'w').write(self.db.password)
                else:
                    return

            i, ok_pressed = QInputDialog.getText(self, "Закрытое храниллище", "Введите пароль")

            if ok_pressed and hashlib.sha1(bytes(i.strip(), encoding='utf-8')).hexdigest() == self.db.password:
                self.cur_state = state

        else:
            self.cur_state = state

        self.ui.stacked_tool_bar.setCurrentWidget(self.tool_bars[self.cur_state])
        self.ui.edit_area.setCurrentWidget(self.empty_edit_area)
        self.ui.search_line.setText("")
        self.search_some_notes()

    def sync_with_db(self):
        for key, value in self.opened_notes.items():
            request = """UPDATE Notes
                                 SET header = "{}", body = "{}"
                                 WHERE id = {}""".format(value.header_view.text(), value.body_view.toPlainText(), key)

            self.db.cursor.execute(request)

        self.db.connection.commit()


class Note(QWidget):
    def __init__(self, note_button: QPushButton, note_id=0, header="", text=""):
        super().__init__()
        self.header_view = QLineEdit()
        self.body_view = QTextEdit()
        self.layout = QVBoxLayout()
        self.id = note_id
        self.note_button = note_button
        self.setup_widgets(header, text)

    def setup_widgets(self, header, text):
        if header == "":
            self.header_view.setPlaceholderText("Header here...")
            self.header_view.setMaxLength(HEADER_MAX_LEN)
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
        try:
            if len(self.header_view.text()) < SHOWED_HEADER_LEN:
                self.note_button.setText(self.header_view.text())
            else:
                self.note_button.setText(self.header_view.text()[:SHOWED_HEADER_LEN - 3] + "...")
        except RuntimeError:
            pass


def dir_exists():
    return os.path.exists(APP_ENV)


def password_file_exists():
    return os.path.exists(PASS_FILE_PATH)


class DataBase:
    def __init__(self):
        self.connection = None
        self.cursor = None

        if not dir_exists():
            os.mkdir(APP_ENV)

        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "Notes"  (
        "id" INTEGER NOT NULL UNIQUE,
        "header" TEXT, 
        "body" TEXT, 
        "state" INTEGER DEFAULT 1, 
        PRIMARY KEY("id" AUTOINCREMENT)
        )""")

        self.connection.commit()

        if not password_file_exists():
            create_pass_file = open(PASS_FILE_PATH, 'w')
            create_pass_file.close()

        opened_pass_file = open(PASS_FILE_PATH, 'r')
        self.password = opened_pass_file.read().strip()

        if self.password == "":
            self.password = None

        opened_pass_file.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    sys.exit(app.exec())
