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
        main_widget.resize(871, 825)
        main_widget.setStyleSheet("background: rgb(3, 74, 89);")
        self.main_layout = QtWidgets.QGridLayout(main_widget)
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setObjectName("main_layout")
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
"}")
        self.edit_area.setObjectName("edit_area")
        self._ = QtWidgets.QWidget()
        self._.setObjectName("_")
        self.edit_area.addWidget(self._)
        self.__ = QtWidgets.QWidget()
        self.__.setObjectName("__")
        self.edit_area.addWidget(self.__)
        self.main_layout.addWidget(self.edit_area, 0, 1, 1, 1)
        self.notes_list = QtWidgets.QWidget(main_widget)
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
        self.notes_list_layout.setContentsMargins(0, 0, 0, 0)
        self.notes_list_layout.setSpacing(0)
        self.notes_list_layout.setObjectName("notes_list_layout")
        self.create_note_button = QtWidgets.QPushButton(self.notes_list)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.create_note_button.sizePolicy().hasHeightForWidth())
        self.create_note_button.setSizePolicy(sizePolicy)
        self.create_note_button.setSizeIncrement(QtCore.QSize(0, 0))
        self.create_note_button.setStyleSheet("")
        self.create_note_button.setObjectName("create_note_button")
        self.notes_list_layout.addWidget(self.create_note_button)
        self.main_layout.addWidget(self.notes_list, 0, 0, 1, 1)

        self.retranslateUi(main_widget)
        QtCore.QMetaObject.connectSlotsByName(main_widget)

    def retranslateUi(self, main_widget):
        _translate = QtCore.QCoreApplication.translate
        main_widget.setWindowTitle(_translate("main_widget", "Form"))
        self._.setWhatsThis(_translate("main_widget", "<html><head/><body><p>dasf</p></body></html>"))
        self.create_note_button.setText(_translate("main_widget", "..."))
