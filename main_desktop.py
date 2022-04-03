import datetime
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QMouseEvent, QFont, QIcon
from PyQt5.QtWidgets import QMenu, QDialog, QColorDialog, QSystemTrayIcon, QAction, QStyle, QApplication

from PyQt5.QtCore import Qt, QTimer, QPoint, pyqtSignal
from Theme_Setting import Ui_Theme
from desktop_ui import Ui_Form


class WelcomeForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(WelcomeForm, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        time1 = datetime.datetime.now()
        # self.setWindowOpacity(0.4)  # 设置窗口透明度
        st = datetime.datetime.strftime(time1, '%Y-%m-%d %H:%M:%S').split(' ')
        self.label.setText(st[1])
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(1)
        self.label.contextMenuEvent = self.mouse_menu
        self.context_menu = QMenu(self)
        self.init_menu()
        self._padding = 5  # 设置边界宽度为5
        # self.label.setGeometry(QRect(328, 240, 329, 27 * 4))
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignTop)
        self.label.mouseDoubleClickEvent = self.hide_titlebar
        self.is_hide = False
        self.tp = QSystemTrayIcon(app)
        self.tp.setIcon(QIcon('favicon.ico'))
        # tp.setIcon(QIcon('d:/img/png/star.png'))
        # 设置系统托盘图标的菜单
        a2 = QAction('退出', self)  # 直接退出可以用qApp.quit
        a2.triggered.connect(QApplication.instance().quit)
        tpMenu = QMenu()
        tpMenu.addAction(a2)
        self.tp.setContextMenu(tpMenu)
        # 不调用show不会显示系统托盘
        self.tp.show()

        self.font_size = 80

    def mouse_menu(self, event):
        self.context_menu.exec_(event.globalPos())

    def hide_titlebar(self, event):
        if not self.is_hide:
            print('safd')
            self.is_hide = True
        else:
            self.is_hide = False

    def resizeEvent(self, QResizeEvent):
        try:
            font_size = QFont()
            font_size.setPointSize(100)
            self.label.setFont(font_size)
        except Exception as e:
            print(e)

    def init_menu(self):
        # 背景透明
        self.context_menu.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框、去掉自带阴影
        self.context_menu.setWindowFlags(
            self.context_menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        # 模拟菜单项
        font_ = QFont()
        font_.setFamily("宋体")
        font_.setPointSize(14)
        self.action1 = self.context_menu.addAction('设置主题', self.set_theme)
        self.action1.setFont(font_)
        self.action2 = self.context_menu.addAction('退出程序', self.close_app)
        self.action2.setFont(font_)

    def close_app(self):
        QApplication.instance().quit()
        sys.exit(app.exec_())

    def system_atry(self):
        self.tp = QSystemTrayIcon(app)
        self.tp.setIcon(
            self.style().standardIcon(QStyle.SP_ComputerIcon))
        # tp.setIcon(QIcon('d:/img/png/star.png'))
        # 设置系统托盘图标的菜单
        a2 = QAction('退出', self)  # 直接退出可以用qApp.quit
        a2.triggered.connect(QApplication.instance().quit)
        tpMenu = QMenu()
        tpMenu.addAction(a2)
        self.tp.setContextMenu(tpMenu)
        # 不调用show不会显示系统托盘
        self.tp.show()

    def set_theme(self):
        try:
            self.setting = Theme_Setting()
            self.setting.show()
            self.setting.signal.connect(self.real_setting)
            self.setting.signal_color.connect(self.color_set)
            self.setting.signal_font.connect(self.font_set)
        except Exception as e:
            print(e)

    def font_set(self, font):
        font_ = QFont(font, self.font_size)
        self.label.setFont(font_)

    def color_set(self, qss):
        print(qss)
        self.label.setStyleSheet(qss)

    def real_setting(self, opacity, font_size):
        self.font_size = font_size
        if opacity != -1:
            print("sfd")
            op = QtWidgets.QGraphicsOpacityEffect()
            # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
            op.setOpacity(opacity / 100)
            self.label.setGraphicsEffect(op)
        if font_size != -1:
            font_ = QFont()
            font_.setPointSize(font_size)
            self.label.setFont(font_)
        # self.setWindowOpacity(opacity / 100)

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def timer_event(self):
        time1 = datetime.datetime.now()
        st = datetime.datetime.strftime(time1, '%Y-%m-%d %H:%M:%S').split(' ')
        self.label.setText(st[1])

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tp.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )


class Theme_Setting(QtWidgets.QWidget, Ui_Theme):
    signal = pyqtSignal(int, int)
    signal_color = pyqtSignal(str)
    signal_font = pyqtSignal(str)

    def __init__(self):
        super(Theme_Setting, self).__init__()
        self.setupUi(self)
        self.fontComboBox.currentFontChanged.connect(self.onFontChanged)
        self.fontComboBox.setCurrentFont(self.font())

    def trans_set(self):
        self.signal.emit(self.horizontalSlider.value(), -1)

    def onFontChanged(self, font):
        print(type(font.family()))
        self.signal_font.emit(font.family())

    def font_set(self):
        pass

    def get_Color(self):
        col = QColorDialog.getColor()
        print(col.name(), "\n")
        if col.isValid():
            self.signal_color.emit('QLabel{color:%s;}' % col.name())

    def font_size_set(self):
        self.signal.emit(-1, self.spinBox.value())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywin = WelcomeForm()
    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    mywin.show()
    QApplication.setQuitOnLastWindowClosed(False)
    sys.exit(app.exec_())
