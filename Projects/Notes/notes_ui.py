# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notes.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_widget(object):
    def setupUi(self, main_widget):
        main_widget.setObjectName("main_widget")
        main_widget.resize(644, 825)
        main_widget.setStyleSheet("QWidget {\n"
"    background: rgb(3, 74, 89);\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"      width: 20px;\n"
"    margin: 20px 0 20px 0;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    min-height: 10px;\n"
"     background: rgba(255, 255, 255, 0.7);\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"    background: none;\n"
"   height: 45px;\n"
"    border-radius: 20px;\n"
"   subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"    background: none;\n"
"    border-radius: 20px;\n"
"    height: 45px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"\n"
"QMessageBox {\n"
"    background: rgb(70, 94, 116)\n"
"}")
        self.main_layout = QtWidgets.QGridLayout(main_widget)
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setObjectName("main_layout")
        self.tool_bar = QtWidgets.QWidget(main_widget)
        self.tool_bar.setStyleSheet("QWidget {\n"
"    background: rgb(10, 70, 83);\n"
"}\n"
"\n"
"QPushButton {\n"
"    color: rgb(94, 92, 100);\n"
"    border: none;\n"
"    font-size: 30px;\n"
"    background: rgb(10, 70, 83);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: rgb(237, 51, 59)\n"
"}")
        self.tool_bar.setObjectName("tool_bar")
        self.tool_bar_layout = QtWidgets.QHBoxLayout(self.tool_bar)
        self.tool_bar_layout.setObjectName("tool_bar_layout")
        self.main_layout.addWidget(self.tool_bar, 0, 1, 1, 1)
        self.menu_button_wrapper = QtWidgets.QWidget(main_widget)
        self.menu_button_wrapper.setStyleSheet("QWidget {\n"
"    background: rgb(10, 70, 83);\n"
"}")
        self.menu_button_wrapper.setObjectName("menu_button_wrapper")
        self.menu_button_layout = QtWidgets.QHBoxLayout(self.menu_button_wrapper)
        self.menu_button_layout.setContentsMargins(9, 9, 9, 9)
        self.menu_button_layout.setSpacing(0)
        self.menu_button_layout.setObjectName("menu_button_layout")
        self.menu_button = QtWidgets.QPushButton(self.menu_button_wrapper)
        self.menu_button.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    color: rgb(154, 153, 150);\n"
"    font-size: 30px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: rgb(255, 255, 255)\n"
"}")
        self.menu_button.setFlat(False)
        self.menu_button.setObjectName("menu_button")
        self.menu_button_layout.addWidget(self.menu_button)
        self.main_layout.addWidget(self.menu_button_wrapper, 0, 0, 1, 1)
        self.scroll_notes_list_area = QtWidgets.QScrollArea(main_widget)
        self.scroll_notes_list_area.setMaximumSize(QtCore.QSize(250, 16777215))
        self.scroll_notes_list_area.setStyleSheet("QScrollArea {\n"
"    border: none;\n"
"}")
        self.scroll_notes_list_area.setWidgetResizable(True)
        self.scroll_notes_list_area.setObjectName("scroll_notes_list_area")
        self.notes_list = QtWidgets.QWidget()
        self.notes_list.setGeometry(QtCore.QRect(0, 0, 250, 763))
        self.notes_list.setStyleSheet("QWidget#notes_list {\n"
"    background: rgb(10, 70, 83);\n"
"    padding-right: 20px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    border: none;\n"
"    border-bottom: 1px solid rgb(4, 29, 38);    \n"
"    color: rgb(255, 255, 255);\n"
"    background: rgb(10, 70, 83);\n"
"    padding: 15px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 1px solid rgb(255, 255, 255);\n"
"}")
        self.notes_list.setObjectName("notes_list")
        self.notes_list_layout = QtWidgets.QVBoxLayout(self.notes_list)
        self.notes_list_layout.setObjectName("notes_list_layout")
        self.create_note_button = QtWidgets.QPushButton(self.notes_list)
        self.create_note_button.setObjectName("create_note_button")
        self.notes_list_layout.addWidget(self.create_note_button)
        self.scroll_notes_list_area.setWidget(self.notes_list)
        self.main_layout.addWidget(self.scroll_notes_list_area, 1, 0, 1, 1)
        self.edit_area = QtWidgets.QStackedWidget(main_widget)
        self.edit_area.setStyleSheet("QStackedWidget {\n"
"    background: rgb(3, 74, 89);\n"
"}\n"
"\n"
"QTextEdit {\n"
"    border: none;\n"
"    color: rgb(255, 255, 255);\n"
"    font-size: 20px;\n"
"    margin: 20px\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: none;\n"
"    color: rgb(255, 255, 255);\n"
"    font-size: 30px;\n"
"    margin: 10px;\n"
"}\n"
"\n"
"")
        self.edit_area.setObjectName("edit_area")
        self._ = QtWidgets.QWidget()
        self._.setObjectName("_")
        self.edit_area.addWidget(self._)
        self.__ = QtWidgets.QWidget()
        self.__.setObjectName("__")
        self.edit_area.addWidget(self.__)
        self.main_layout.addWidget(self.edit_area, 1, 1, 1, 1)

        self.retranslateUi(main_widget)
        QtCore.QMetaObject.connectSlotsByName(main_widget)

    def retranslateUi(self, main_widget):
        _translate = QtCore.QCoreApplication.translate
        main_widget.setWindowTitle(_translate("main_widget", "Form"))
        self.menu_button.setText(_translate("main_widget", "☰"))
        self.create_note_button.setText(_translate("main_widget", "PushButton"))
        self._.setWhatsThis(_translate("main_widget", "<html><head/><body><p>dasf</p></body></html>"))
