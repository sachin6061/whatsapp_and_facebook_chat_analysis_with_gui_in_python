import sys
import time

from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtWidgets import QFileDialog
import components
from whatsapp_grp_chat import whatsapp_grp_chat_win
from facebook_analysis import facebook_chat_win
from dynaconf import settings as set


class dashboard_win(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.tbl_data = []
        components.change_font_size(self, 16)
        size = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.resize(size.width(), size.height())
        self.hei_part = size.height() // 20
        self.width = size.width()
        self.height = size.height()
        self.wid_part = self.width // 20

        self.header_frame = components.black_frame(self, 0, 0, self.width, self.hei_part)
        self.header = components.header(self.header_frame, "Chat Analysis", self.hei_part)

        self.sub_frame = components.frame_with(self, 55, self.hei_part + 80, self.width - 150,
                                               self.height - self.hei_part * 6)

        self.lbl = components.add_lbl(self.sub_frame, self.wid_part * 5, self.hei_part * 4,
                                      "Please select your chat Type",
                                      width=500, height=40)
        components.change_font_size(self.lbl, 15)
        self.lstbox = components.add_listbox(self.sub_frame, self.wid_part * 10, self.hei_part * 4, 300, 35)
        self.lstbox.addItems(["WhatsApp Group Chat", "Facebook"])
        components.change_font_size(self.lstbox, 15)
        self.lstbox.activated.connect(self.show_btn)

        self.lbl_file = components.add_lbl(self.sub_frame, self.wid_part * 5, self.hei_part * 6,
                                           "Please select your chat file!",
                                           width=500, height=40)
        components.change_font_size(self.lbl_file, 18)

        self.file_name_lbl = components.add_lbl(self.sub_frame, self.wid_part * 2, self.hei_part * 8, "",
                                                self.wid_part * 14, height=40)
        components.change_font_size(self.file_name_lbl, 16)
        self.file_name_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.select_btn = components.add_btn(self.sub_frame, self.wid_part * 10, self.hei_part * 6, "select File", 150,
                                             40)
        self.select_btn.clicked.connect(self.openFileNameExplorer)
        self.process_btn = components.add_btn(self.sub_frame, self.wid_part * 8, self.hei_part * 10, "Process",
                                              150, 40)
        self.process_btn.clicked.connect(self.show_main)

        self.process_btn.hide()
        self.select_btn.hide()
        self.lbl_file.hide()
        self.showNormal()

    def show_btn(self):
        self.select_btn.show()
        self.lbl_file.show()

    def hide_main(self):
        self.main_frame.hide()

    def show_main(self):
        path = self.file_name_lbl.text()
        if self.lstbox.currentText() == "WhatsApp Group Chat":
            w = whatsapp_grp_chat_win(self, path)
        else:
            f = facebook_chat_win(self, path)
        self.file_name_lbl.setText("")
        self.process_btn.hide()
        self.select_btn.hide()
        self.lbl_file.hide()

    def show_sub(self):
        self.sub_frame.show()

    def hide_sub(self):
        self.sub_frame.hide()

    def openFileNameExplorer(self):
        if self.lstbox.currentText() == "WhatsApp Group Chat":
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            self.fileName, _ = QFileDialog.getOpenFileName(self, "Please select text file", "",
                                                           "text Files (*.txt)", options=options)
            if self.fileName:
                self.file_name_lbl.setText(str(self.fileName))
                self.process_btn.show()
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            self.fileName, _ = QFileDialog.getOpenFileName(self, "Please select json file", "",
                                                           "text Files (*.json)", options=options)
            if self.fileName:
                self.file_name_lbl.setText(str(self.fileName))
                self.process_btn.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = dashboard_win()
    sys.exit(app.exec_())
