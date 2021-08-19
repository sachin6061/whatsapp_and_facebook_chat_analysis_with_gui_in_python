import sys
from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel
import components
import sqlite3
import pandas as pd
from facebook_ana import facebook_data


class facebook_chat_win(QtWidgets.QDialog):
    def __init__(self, parent, path):
        super().__init__(parent)
        self.msgbox = components.add_messagebox(self)
        self.msgbox.hide()
        self.analysis = facebook_data()
        self.analysis.read_file(path)
        size = QtWidgets.QDesktopWidget().screenGeometry(-1)

        self.hei_part = size.height() // 20
        self.height = size.height()
        self.width = size.width()
        self.wid_part = self.width // 18

        self.txtbx_size = self.wid_part * 2
        self.lbl_size = self.wid_part + 20
        self.x_pos = self.wid_part * 2 + (self.wid_part // 2)

        self.resize(size.width(), self.height)

        self.file_path = ''

        self.header_frame = components.black_frame(self, 0, 0, self.width, self.hei_part)

        self.header = components.header(self.header_frame, "Facebook Chat Analysis", self.hei_part)

        # self.scroll_area = components.border_frame(self, 10, hei_part + 10, width - 20, (height - 20) - hei_part)

        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(QtCore.QRect(10, self.hei_part + 10, self.width - 20, (self.height - self.hei_part * 4)))
        components.change_font_size(self.tabs, 12)
        self.tab1 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(self.width - 20, (self.height - self.hei_part * 3))

        # Add tabs
        self.tabs.addTab(self.tab1, "Basic Details")
        self.tabs.addTab(self.tab3, "message per person analysis")
        self.tabs.addTab(self.tab4, "Active  group member analysis")
        txt = 'Total group members ' + str(len(self.analysis.df.Author.unique()))
        # total_messages = self.analysis.df.shape[0]
        # print('Total number of messages', total_messages)
        self.fname_lbl = components.add_lbl(self.tab1, self.wid_part * 8, self.hei_part, txt, self.wid_part * 6,
                                            40)
        components.change_font_size(self.fname_lbl, 18)
        txt = self.analysis.find_top_most_active()
        self.top_most_fac_active = components.add_textarea(self.tab1, self.wid_part * 2, self.hei_part * 3,
                                                           self.wid_part * 4,
                                                           self.hei_part * 5)
        self.top_most_fac_active.setPlainText(str(txt))

        txt = self.analysis.find_top_5_photos()

        self.top_most_media = components.add_textarea(self.tab1, self.wid_part * 7, self.hei_part * 3,
                                                      self.wid_part * 4,
                                                      self.hei_part * 5)
        self.top_most_media.setPlainText(str(txt))

        txt = self.analysis.find_top_5_sticker()

        self.top_most_links = components.add_textarea(self.tab1, self.wid_part * 12, self.hei_part * 3,
                                                      self.wid_part * 4, self.hei_part * 5)
        self.top_most_links.setPlainText(str(txt))

        txt = self.analysis.find_top_5_reactions()

        self.top_most_links_user = components.add_textarea(self.tab1, self.wid_part * 2, self.hei_part * 9,
                                                           self.wid_part * 4, self.hei_part * 5)
        self.top_most_links_user.setPlainText(str(txt))

        txt = self.analysis.find_top_5_videos()

        self.top_most_emoji_user = components.add_textarea(self.tab1, self.wid_part * 7, self.hei_part * 9,
                                                           self.wid_part * 4, self.hei_part * 5)
        self.top_most_emoji_user.setPlainText(str(txt))

        txt = self.analysis.find_top_5_gifs()

        self.top_most_emoji_user = components.add_textarea(self.tab1, self.wid_part * 12, self.hei_part * 9,
                                                           self.wid_part * 4, self.hei_part * 5)
        self.top_most_emoji_user.setPlainText(str(txt))

        self.sel_y_lbl = components.add_lbl(self.tab3, self.wid_part * 6, self.hei_part, "Select Year -",
                                            self.wid_part * 2,
                                            40)
        components.change_font_size(self.sel_y_lbl, 15)

        list_years = self.analysis.list_of_years()
        list_years.append('All')
        self.lyears = components.add_listbox(self.tab3, self.wid_part * 8, self.hei_part, self.wid_part * 2, 40)

        for year in list_years:
            self.lyears.addItem(str(year))

        self.lyears.activated.connect(self.show_tab3)

        self.sel_y_lbl = components.add_lbl(self.tab4, self.wid_part * 6, self.hei_part, "Select Year -",
                                            self.wid_part * 2,
                                            40)
        components.change_font_size(self.sel_y_lbl, 15)
        list_years = self.analysis.list_of_years()
        self.lyearstab4 = components.add_listbox(self.tab4, self.wid_part * 8, self.hei_part, self.wid_part * 2, 40)
        for year in list_years:
            self.lyearstab4.addItem(str(year))

        self.lyearstab4.activated.connect(self.show_tab4)

        try:
            self.analysis.chart()

        except Exception as e:
            print(e)
        self.monthchartlbl = components.add_lbl(self.tab3, 20, self.hei_part * 2, "",
                                                self.wid_part * 10, self.hei_part * 12)

        components.set_image(self, 'faclinechartpermonth.png', self.monthchartlbl)

        self.monthbarchartlbl = components.add_lbl(self.tab3, self.wid_part * 9, self.hei_part * 2, "",
                                                   self.wid_part * 10, self.hei_part * 12)

        self.activedayslbl = components.add_lbl(self.tab4, 20, self.hei_part * 2, "",
                                                self.wid_part * 10, self.hei_part * 12)

        self.activehourslbl = components.add_lbl(self.tab4, self.wid_part * 9, self.hei_part * 2, "",
                                                 self.wid_part * 10, self.hei_part * 12)

        self.show()

    def show_tab3(self):
        try:
            self.analysis.charts(self.lyears.currentText())
            components.set_image(self, 'facbarchartpermonth.png', self.monthbarchartlbl)

        except Exception as e:
            self.msgbox.setText('Unable to analysis Data, please check yours txt file')
            self.msgbox.show()

    def show_tab4(self):
        try:
            self.analysis.active_days(int(self.lyearstab4.currentText()))
            self.analysis.active_hours(int(self.lyearstab4.currentText()))
            components.set_image(self, 'facactivedaysmonth.png', self.activedayslbl)
            components.set_image(self, 'facactivehoursmonth.png', self.activehourslbl)

        except Exception as e:
            self.msgbox.setText('Unable to analysis Data, please check yours txt file')
            self.msgbox.show()
