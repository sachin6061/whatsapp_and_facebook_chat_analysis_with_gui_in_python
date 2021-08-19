import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from dynaconf import settings as set

pre_emp_id = ''


def header(frame, text, height, width=None):
    logo_wid = set.WID_PER * 12

    logo = QtWidgets.QLabel(frame)
    logo.setGeometry(QtCore.QRect(10, 3, logo_wid, height))

    # pixmap = QtGui.QPixmap('images/i-TEKLOGO.png')
    # pixmap = pixmap.scaledToHeight(height, QtCore.Qt.SmoothTransformation)
    # logo.setPixmap(pixmap)
    if width is not None:
        label = QtWidgets.QLabel(text, frame)
        label.setGeometry(QtCore.QRect(1, 1, width, height))
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("background-color:#000000;color:rgb(255, 255, 255)")
        change_font_size(label, 16)
    else:
        label = QtWidgets.QLabel(text, frame)
        label.setGeometry(QtCore.QRect(logo_wid, 3, set.SCREEN_WIDTH - logo_wid * 2, height))
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("color:rgb(255, 255, 255)")
        change_font_size(label, 16)

    # def clicked(i):
    #     if i.text() == "SHUT DOWN":
    #         import sys
    #         sys.exit(1)
    #
    # msg = QMessageBox(parent)
    # msg.setWindowTitle(" ")
    # msg.addButton(QtWidgets.QPushButton("SHUT DOWN"), QMessageBox.YesRole)
    # msg.addButton(QtWidgets.QPushButton("RESTART"), QMessageBox.YesRole)
    # msg.addButton(QtWidgets.QPushButton("CANCEL"), QMessageBox.RejectRole)
    # msg.buttonClicked.connect(clicked)
    # msg.hide()
    # msg.setStyleSheet(set.MSG_BOX)

    # pixmap.load('app/icons/power-button.png')
    # pixmap = pixmap.scaledToHeight(height-5, QtCore.Qt.SmoothTransformation)
    # pixmap = pixmap.scaledToWidth(set.WID_PER * 4, QtCore.Qt.SmoothTransformation)
    # pixmap.save('icons/modified/power-button.png')
    #
    # shut_down = QtWidgets.QPushButton(frame)
    # shut_down.setGeometry(QtCore.QRect(set.SCREEN_WIDTH - set.WID_PER * 6, 2, height-3, set.WID_PER * 5))
    # shut_down.clicked.connect(msg.show)
    # shut_down.setStyleSheet("background-image:url(icons/modified/power-button.png);background-color : black")


def footer(self, frame, height):
    self.label_2 = QtWidgets.QLabel("Version - 0.01 V", frame)
    self.label_2.setGeometry(QtCore.QRect(25, 3, set.WID_PER * 9, height))
    self.label_2.setStyleSheet("color:rgb(255, 255, 255)")
    change_font_size(self.label_2, 16)

    # self.time = QtWidgets.QLabel(frame)
    # self.time.setGeometry(QtCore.QRect(set.WID_PER * 10, 3, set.WID_PER * 18, height))
    # self.time.setStyleSheet("color:rgb(255, 255, 255)")
    # change_font_size(self.time, set.FONT_SIZE)

    # self.time.setText(QtCore.QDateTime.currentDateTime().toString(" dd/MM/yyyy  hh:mm:ss"))
    #
    # def showTime():
    #     self.time.setText(QtCore.QDateTime.currentDateTime().toString(" dd/MM/yyyy  hh:mm:ss"))
    #
    # timer = QtCore.QTimer(self.time)
    # timer.timeout.connect(showTime)
    # timer.start(1000)

    # self.spd = QtWidgets.QLabel("Please wait ", frame)
    # self.spd.setGeometry(QtCore.QRect(set.WID_PER * 29, 3, set.WID_PER * 9, height))
    # self.spd.setStyleSheet("color:rgb(255, 255, 255)")
    # change_font_size(self.spd, set.FONT_SIZE)
    # # speed_thread = threading.Thread(target=speed)
    # # speed_thread.start()

    self.label_3 = QtWidgets.QLabel("\u00a9www.Datamoulds.com", frame)
    self.label_3.setGeometry(QtCore.QRect(set.SCREEN_WIDTH - (set.WID_PER * 20), 3, set.WID_PER * 19, height))
    self.label_3.setStyleSheet("color:rgb(255, 255, 255)")
    change_font_size(self.label_3, 16)
    self.label_3.setAlignment(QtCore.Qt.AlignRight)


def screen_size(self):
    size = QtWidgets.QDesktopWidget().screenGeometry(-1)
    h = size.height()
    w = size.width()
    return w, h


def change_font_size(text, size=12):
    font = QtGui.QFont()
    font.setPointSize(size)
    text.setFont(font)


def add_btn(frame, x, y, text, width, height):
    btn = QtWidgets.QPushButton(text, frame)
    btn.setGeometry(QtCore.QRect(x, y, width, height))
    change_font_size(btn, 9)
    btn.setStyleSheet(set.BTN_BORDER)
    return btn


def add_radio_btn(frame, x, y, text, width, height):
    btn = QtWidgets.QRadioButton(text, frame)
    btn.setGeometry(QtCore.QRect(x, y, width, height))
    # btn.setStyleSheet(set.BTN_BORDER)
    return btn


def resize_img(icon_name):
    path = set.ICON_PATH + icon_name
    pixmap = QtGui.QPixmap()
    pixmap.load(path)
    pixmap = pixmap.scaledToHeight(set.ICON_SIZE, QtCore.Qt.SmoothTransformation)
    pixmap = pixmap.scaledToWidth(set.ICON_SIZE, QtCore.Qt.SmoothTransformation)
    pixmap.save(set.SAVE_ICON_PATH + icon_name)


def image_btn(frame, x, y, image_name):
    sacn_count = QtWidgets.QPushButton(frame)
    sacn_count.setGeometry(QtCore.QRect(x, y, set.ICON_SIZE, set.ICON_SIZE))
    change_font_size(sacn_count, 40)
    resize_img(image_name)
    style = """QPushButton{background-image:url(""" + str(set.SAVE_ICON_PATH + image_name) + """);
                border : 2px solid #FFFFFF;border-radius: 35px;}
                QPushButton::hover{border-color: #139BEF;border-width :0px 0px 8px 0px ;}"""
    sacn_count.setStyleSheet(style)
    return sacn_count


def add_messagebox(frame):
    msg_box = QMessageBox(frame)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    # msg_box.setStyleSheet(set.MSG_BOX)
    msg_box.hide()

    font = QtGui.QFont()
    font.setPointSize(15)
    msg_box.setFont(font)
    return msg_box


def add_lbl(frame, x, y, text, width=150, height=30):
    lbl = QtWidgets.QLabel(text, frame)
    lbl.setGeometry(QtCore.QRect(x, y, width, height))
    lbl.setStyleSheet(set.NONE_BORDER)
    change_font_size(lbl, 10)
    return lbl


def border_frame(parent, x, y, width, height):
    frame = QtWidgets.QFrame(parent)
    frame.setGeometry(QtCore.QRect(x, y, width, height))
    frame.setFrameShape(QtWidgets.QFrame.Box)
    frame.setStyleSheet(set.BLACK_BORDER)
    return frame


def black_frame(frame, x, y, width, height):
    frame = QtWidgets.QFrame(frame)
    frame.setGeometry(QtCore.QRect(x, y, width, height))
    frame.setStyleSheet("background-color:rgb(0, 0, 0)")
    frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
    return frame


def orange_frame(frame, x, y, width, height, text):
    frame = QtWidgets.QFrame(frame)
    frame.setGeometry(QtCore.QRect(x, y, width, height))
    frame.setStyleSheet(set.FRAME_ORANGE)

    title = QtWidgets.QLabel(text, frame)
    title.setGeometry(QtCore.QRect(2, 3, width - 10, height - 5))
    title.setAlignment(QtCore.Qt.AlignCenter)
    title.setStyleSheet(set.NONE_BORDER)
    change_font_size(title, set.FONT_SIZE)
    return frame


# def add_radio_btn(frame, x, y, text, width=150, height=40):
#     radio_btn = QtWidgets.QRadioButton(text, frame)
#     radio_btn.setGeometry(QtCore.QRect(x, y, width, height))
#     # change_font_size(radio_btn, set.FONT_SIZE)
#     # radio_btn.setStyleSheet(set.NONE_BORDER)
#     return radio_btn


def add_textbox(frame, x, y, width=300, height=30):
    textbox = QtWidgets.QLineEdit(frame)
    textbox.setGeometry(QtCore.QRect(x, y, width, height))
    change_font_size(textbox, 10)
    textbox.setStyleSheet(set.BLACK_BORDER)
    return textbox


def add_tbl(frame, x, y, width, height):
    table = QtWidgets.QTableWidget(frame)
    table.setGeometry(QtCore.QRect(x, y, width, height))
    table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
    table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
    table.setStyleSheet(set.TBL_STYLE)
    # table.verticalHeader().hide()
    return table


def add_label(frame, x, y, text, width, height=30):
    lbl = QtWidgets.QLabel(text, frame)
    lbl.setGeometry(QtCore.QRect(x, y, width, height))
    lbl.setAlignment(QtCore.Qt.AlignCenter)
    lbl.setStyleSheet(set.NONE_BORDER)
    # change_font_size(lbl, set.FONT_SIZE)
    return lbl


def add_btn_size(frame, text, x, y, width, height=50):
    btn = QtWidgets.QPushButton(text, frame)
    btn.setGeometry(QtCore.QRect(x, y, width, height))
    change_font_size(btn, 18)
    btn.setStyleSheet(set.BTN_BORDER)
    return btn


def add_listbox(frame, x, y, width=100, height=30):
    textbox = QtWidgets.QComboBox(frame)
    textbox.setGeometry(QtCore.QRect(x, y, width, height))
    # textbox.setStyleSheet(set.BLACK_BORDER)
    return textbox


def add_notification(frame, x, y, text, width, height=30):
    lbl = QtWidgets.QLabel(text, frame)
    lbl.setGeometry(QtCore.QRect(x, y, width, height))
    lbl.setAlignment(QtCore.Qt.AlignCenter)
    lbl.setStyleSheet(set.NOTIFICATION)
    return lbl


def date_picker(frame, x, y, width, height=30):
    dateedit = QtWidgets.QDateEdit(frame, calendarPopup=True)
    dateedit.setGeometry(QtCore.QRect(x, y, width, height))
    # dateedit.setDateTime(QtCore.QDateTime.currentDateTime())
    return dateedit


def add_textarea(frame, x, y, width=400, height=200):
    textbox = QtWidgets.QPlainTextEdit(frame)
    textbox.setGeometry(QtCore.QRect(x, y, width, height))
    change_font_size(textbox, 12)
    textbox.setReadOnly(True)
    textbox.setStyleSheet(set.BLACK_BORDER)
    return textbox


def _frame(parent, x, y, width, height):
    frame = QtWidgets.QFrame(parent)
    frame.setGeometry(QtCore.QRect(x, y, width, height))
    frame.setFrameShape(QtWidgets.QFrame.Box)
    frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
    frame.setLineWidth(1)
    return frame


def add_groupbox(parent, x, y, width, height):
    grpbox = QtWidgets.QGroupBox(parent)
    grpbox.setGeometry(QtCore.QRect(x, y, width, height))
    grpbox.set
    # grpbox.setFrameShape(QtWidgets.QGroupBox.Box)
    # grpbox.setFrameShape(QtWidgets.QGroupBox.StyledPanel)
    # grpbox.setLineWidth(1)
    return grpbox


def frame_with(parent, x, y, width, height):
    frame = QtWidgets.QFrame(parent)
    frame.setGeometry(QtCore.QRect(x, y, width, height))
    frame.setFrameShape(QtWidgets.QFrame.Box)
    frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
    frame.setLineWidth(1)
    return frame


def set_image(self, path, photo_lbl):
    pixmap = QtGui.QPixmap()
    pixmap.load(path)
    pixmap = pixmap.scaledToWidth(self.hei_part * 15, QtCore.Qt.SmoothTransformation)
    # pixmap = pixmap.scaledToHeight(self.hei_part * 9, QtCore.Qt.SmoothTransformation)
    photo_lbl.setPixmap(pixmap)
