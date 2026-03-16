# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'music_UI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(1267, 1036)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("musicdown.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(icon)

        # 왼쪽 버튼: CSV 불러오기
        self.btn_del = QtWidgets.QPushButton(dialog)
        self.btn_del.setGeometry(QtCore.QRect(100, 850, 491, 71))
        self.btn_del.setObjectName("btn_del")

        # 오른쪽 버튼: CSV 저장
        self.btn_insert = QtWidgets.QPushButton(dialog)
        self.btn_insert.setGeometry(QtCore.QRect(680, 850, 491, 71))
        self.btn_insert.setObjectName("btn_insert")

        # 왼쪽 제목
        self.db_veiw = QtWidgets.QTextBrowser(dialog)
        self.db_veiw.setGeometry(QtCore.QRect(210, 110, 256, 41))
        self.db_veiw.setObjectName("db_veiw")

        # 오른쪽 제목
        self.melon_veiw = QtWidgets.QTextBrowser(dialog)
        self.melon_veiw.setGeometry(QtCore.QRect(810, 110, 256, 41))
        self.melon_veiw.setObjectName("melon_veiw")

        # 오른쪽 리스트: 멜론 차트
        self.melon_list = QtWidgets.QTextBrowser(dialog)
        self.melon_list.setGeometry(QtCore.QRect(680, 170, 491, 661))
        self.melon_list.setObjectName("melon_list")

        # 하단 버튼: 차트 조회
        self.btn_listUp = QtWidgets.QPushButton(dialog)
        self.btn_listUp.setGeometry(QtCore.QRect(100, 940, 1071, 71))
        self.btn_listUp.setObjectName("btn_listUp")

        # 왼쪽 리스트: CSV 미리보기
        self.db_list = QtWidgets.QTextBrowser(dialog)
        self.db_list.setGeometry(QtCore.QRect(100, 170, 491, 661))
        self.db_list.setObjectName("db_list")

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "멜론 차트 CSV 저장기"))

        self.btn_del.setText(_translate("dialog", "CSV 불러오기"))
        self.btn_insert.setText(_translate("dialog", "CSV 저장"))
        self.btn_listUp.setText(_translate("dialog", "차트 조회"))

        self.db_veiw.setHtml(_translate(
            "dialog",
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
            "\"http://www.w3.org/TR/REC-html40/strict.dtd\">"
            "<html><head><meta name=\"qrichtext\" content=\"1\" />"
            "<style type=\"text/css\">"
            "p, li { white-space: pre-wrap; }"
            "</style></head>"
            "<body style=\" font-family:'Gulim'; font-size:9pt; font-weight:400; font-style:normal;\">"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
            "margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" font-size:14pt; color:#000000;\">CSV 파일 내용</span>"
            "</p></body></html>"
        ))

        self.melon_veiw.setHtml(_translate(
            "dialog",
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
            "\"http://www.w3.org/TR/REC-html40/strict.dtd\">"
            "<html><head><meta name=\"qrichtext\" content=\"1\" />"
            "<style type=\"text/css\">"
            "p, li { white-space: pre-wrap; }"
            "</style></head>"
            "<body style=\" font-family:'Gulim'; font-size:9pt; font-weight:400; font-style:normal;\">"
            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
            "margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
            "<span style=\" font-size:14pt; color:#000000;\">멜론 차트</span>"
            "</p></body></html>"
        ))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())