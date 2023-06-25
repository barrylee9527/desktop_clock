import datetime
import sys
from ctypes import POINTER, cast
from ctypes.wintypes import MSG

import win32api
import win32con
import win32gui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QRect, QPointF, QEvent
from PyQt5.QtGui import QMouseEvent, QFont, QIcon, QPainter, QColor, QWheelEvent
from PyQt5.QtWidgets import QMenu, QColorDialog, QSystemTrayIcon, QAction, QStyle, QApplication, QWidget
from qframelesswindow import FramelessWindow

from Theme_Setting import Ui_Theme
from desktop_ui import Ui_Form
from windows.c_structures import MINMAXINFO, NCCALCSIZE_PARAMS
from windows.com_widget import MoveEnum, ComWidget
from windows.window_effect import WindowEffect


class WelcomeForm(QWidget, Ui_Form):
    def __init__(self):
        super(WelcomeForm, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        time1 = datetime.datetime.now()
        self.current_width = self.width() * self.height()
        self.orgin_width = self.width() * self.height()
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
        self.curIndex = 0
        self.painter = QPainter(self.label)
        self.font = QFont("宋体", 70, QFont.Bold)
        self.painter.setFont(self.font)
        self.charWidth = 14
        self.is_locked = False
        self.time_counter = 0
        self.timeout = QTimer()
        self.timeout.timeout.connect(self.show_timeout)
        self.timeout.start(1000)
        self.m_nBorder = 10
        self.setMouseTracking(True)
        self.m_bPress = False
        self.m_area = 0
        self.m_currentPos = 0
        self.isWin = False
        self.__monitorInfo = None
        self.windowEffect = WindowEffect()
        self.windowEffect.addWindowAnimation(self.winId())
        # 修复多屏不同 dpi 的显示问题
        self.windowHandle().screenChanged.connect(self.__onScreenChanged)
        self.setAttribute(Qt.WA_Hover, True)
        self.label.setStyleSheet("color:rgb(169, 183, 198);")
        # 设置label字体大小随窗口大小变化
        self.installEventFilter(self)
        self.label.setFont(self.font)
        self.label.update()

    def mouse_menu(self, event):
        self.context_menu.exec_(event.globalPos())

    def hide_titlebar(self, event):
        if not self.is_hide:
            self.is_hide = True
        else:
            self.is_hide = False

    def init_menu(self):
        # 背景透明
        # self.context_menu.setAttribute(Qt.WA_TranslucentBackground)
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
        self.font = font_
        self.label.setFont(font_)

    def color_set(self, qss):
        print(qss)
        self.label.setStyleSheet(qss)

    def real_setting(self, opacity, font_size):
        self.font_size = font_size
        if opacity != -1:
            op = QtWidgets.QGraphicsOpacityEffect()
            # 设置透明度的值，0.0到1.0，最小值0很透明，1是不透明
            op.setOpacity(opacity / 100)
            self.label.setGraphicsEffect(op)
        if font_size != -1:
            font_ = QFont(self.font.family(), font_size)
            self.font = font_
            self.label.setFont(font_)
        # self.setWindowOpacity(opacity / 100)

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

    def show_timeout(self):
        self.time_counter += 1
        if self.time_counter >= 2:
            self.label.show()
            # self.setStyleSheet(''' #Desktop_lyric{background-color: rgba(0, 0, 0, 0);}''')
            self.widget.setStyleSheet('''#widget{
            	background-color: rgba(13, 13, 13,0);
            	border-radius:8px;
            }''')
            self.time_counter = 0

    def updateIndex(self):
        # print(self.curIndex)
        self.label.update()
        self.curIndex = self.curIndex + 1
        if self.curIndex * self.charWidth > self.label.width():
            self.curIndex = 0

    def lock(self):
        if self.is_locked:
            self.is_locked = False
        else:
            self.is_locked = True

    def enterEvent(self, e):
        self.timeout.stop()
        self.time_counter = 0
        if self.is_locked:
            # self.pushButton_6.setFont(QFont("楷体", 12, QFont.Bold))
            return
        else:
            self.widget.show()
            self.widget.setStyleSheet('''#widget{
            	background-color: rgba(13, 13, 13,80);
            	border-radius:8px;
            }''')

    def leaveEvent(self, e):
        self.timeout.start(1000)

    def nativeEvent(self, eventType, message):
        if eventType == "windows_generic_MSG":
            """ 处理windows消息 """
            msg = MSG.from_address(message.__int__())
            if msg.message == win32con.WM_NCCALCSIZE:
                if self._isWindowMaximized(msg.hWnd):
                    print("最大化")
                    self.__monitorNCCALCSIZE(msg)
                return True, 0
            elif msg.message == win32con.WM_GETMINMAXINFO:
                if self._isWindowMaximized(msg.hWnd):
                    window_rect = win32gui.GetWindowRect(msg.hWnd)
                    if not window_rect:
                        return False, 0
                    # 获取显示器句柄
                    monitor = win32api.MonitorFromRect(window_rect)
                    if not monitor:
                        return False, 0
                    # 获取显示器信息
                    __monitorInfo = win32api.GetMonitorInfo(monitor)
                    monitor_rect = __monitorInfo['Monitor']
                    work_area = __monitorInfo['Work']
                    # 将lParam转换为MINMAXINFO指针
                    info = cast(msg.lParam, POINTER(MINMAXINFO)).contents
                    # 调整窗口大小
                    info.ptMaxSize.x = work_area[2] - work_area[0]
                    info.ptMaxSize.y = work_area[3] - work_area[1]
                    info.ptMaxTrackSize.x = info.ptMaxSize.x
                    info.ptMaxTrackSize.y = info.ptMaxSize.y
                    # 修改左上角坐标
                    info.ptMaxPosition.x = abs(window_rect[0] - monitor_rect[0])
                    info.ptMaxPosition.y = abs(window_rect[1] - monitor_rect[1])
                    return True, 1
        return QWidget.nativeEvent(self, eventType, message)

    def setMouseStyle(self, moveArea):
        if moveArea == MoveEnum.LEFT_TOP.value:
            self.setCursor(Qt.SizeFDiagCursor)
        elif moveArea == MoveEnum.TOP.value:
            self.setCursor(Qt.ArrowCursor)
        elif moveArea == MoveEnum.RIGHT_TOP.value:
            self.setCursor(Qt.SizeBDiagCursor)
        elif moveArea == MoveEnum.LEFT.value:
            self.setCursor(Qt.SizeHorCursor)
        elif moveArea == MoveEnum.CENTER.value:
            self.setCursor(Qt.ArrowCursor)
        elif moveArea == MoveEnum.RIGHT.value:
            self.setCursor(Qt.SizeHorCursor)
        elif moveArea == MoveEnum.LEFT_BOTTOM.value:
            self.setCursor(Qt.SizeBDiagCursor)
        elif moveArea == MoveEnum.BOTTOM.value:
            self.setCursor(Qt.SizeVerCursor)
        elif moveArea == MoveEnum.RIGHT_BOTTOM.value:
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        if self.isWin:
            return QWidget.mousePressEvent(self, event)
        area = ComWidget.moveArea(self.width(), self.height(), event.pos())
        self.setMouseStyle(area)
        if self.m_bPress:
            # print(event.globalPos())
            # print(self.m_currentPos)
            tempPos = event.globalPos() - self.m_currentPos

            # if self.m_area == MoveEnum.TOP.value:
            if self.m_area == MoveEnum.TOP.value or self.m_area == MoveEnum.CENTER.value:
                self.move(self.pos() + tempPos)
                self.m_currentPos = event.globalPos()
                return

            else:
                tl = self.mapToGlobal(self.rect().topLeft())
                rb = self.mapToGlobal(self.rect().bottomRight())
                gloPoint = event.globalPos()
                rMove = QRect(tl, rb)
                if self.m_area == MoveEnum.LEFT_TOP.value:
                    if rb.x() - gloPoint.x() <= self.minimumWidth():
                        rMove.setX(tl.x())
                    else:
                        rMove.setX(gloPoint.x())
                    if rb.y() - gloPoint.y() <= self.minimumHeight():
                        rMove.setY(tl.y())
                    else:
                        rMove.setY(gloPoint.y())
                elif self.m_area == MoveEnum.RIGHT_TOP.value:
                    rMove.setWidth(gloPoint.x() - tl.x())
                    rMove.setY(gloPoint.y())
                elif self.m_area == MoveEnum.LEFT.value:
                    if rb.x() - gloPoint.x() <= self.minimumWidth():
                        rMove.setX(tl.x())
                    else:
                        rMove.setX(gloPoint.x())
                elif self.m_area == MoveEnum.RIGHT.value:
                    rMove.setWidth(gloPoint.x() - tl.x())
                elif self.m_area == MoveEnum.LEFT_BOTTOM.value:
                    rMove.setX(gloPoint.x())
                    rMove.setHeight(gloPoint.y() - tl.y())
                elif self.m_area == MoveEnum.BOTTOM.value:
                    rMove.setHeight(gloPoint.y() - tl.y())
                elif self.m_area == MoveEnum.RIGHT_BOTTOM.value:
                    rMove.setWidth(gloPoint.x() - tl.x())
                    rMove.setHeight(gloPoint.y() - tl.y())
                # print(rMove)
                self.setGeometry(rMove)
            # event.accept()

    def mousePressEvent(self, event):
        if self.isWin:
            return QWidget.mousePressEvent(self, event)
        area = self.moveArea(event.pos())
        self.setMouseStyle(area)
        if event.buttons() == Qt.LeftButton:
            self.m_bPress = True
            self.m_area = area
            self.m_currentPos = event.globalPos()
            # event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.isWin:
            return QWidget.mouseReleaseEvent(self, event)
        self.m_bPress = False
        self.setCursor(Qt.ArrowCursor)

    def _isWindowMaximized(self, hWnd) -> bool:
        """ 判断窗口是否最大化 """
        # 返回指定窗口的显示状态以及被恢复的、最大化的和最小化的窗口位置，返回值为元组
        windowPlacement = win32gui.GetWindowPlacement(hWnd)

        if not windowPlacement:
            return False
        return windowPlacement[1] == win32con.SW_MAXIMIZE

    def wheelEvent(self, a0: QWheelEvent) -> None:
        font_size = a0.angleDelta().y() * 0.02 + self.font.pointSize()
        self.font = QFont(self.font.family(), int(font_size))
        self.label.setFont(self.font)
        self.label.update()


    def __monitorNCCALCSIZE(self, msg: MSG):
        """ 调整窗口大小 """
        print("__monitorNCCALCSIZE")
        monitor = win32api.MonitorFromWindow(msg.hWnd)
        # 如果没有保存显示器信息就直接返回，否则接着调整窗口大小
        if monitor is None and not self.__monitorInfo:
            return
        elif monitor is not None:
            self.__monitorInfo = win32api.GetMonitorInfo(monitor)

    def __onScreenChanged(self):
        print("__onScreenChanged")
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)

    def moveArea(self, pos: QPointF):
        if pos.y() < self.m_nBorder:
            k = 10
        elif pos.y() > self.height() - self.m_nBorder:
            k = 30
        else:
            k = 20

        if pos.x() < self.m_nBorder:
            v = 1
        elif pos.x() > self.width() - self.m_nBorder:
            v = 3
        else:
            v = 2
        return k + v

    def eventFilter(self, obj, e):
        if not self.m_bPress:
            if e.type() == QEvent.HoverEnter or e.type() == QEvent.HoverLeave or e.type() == QEvent.HoverMove:
                self.mouseMoveEvent(e)
        return QWidget.eventFilter(self, obj, e)


class Theme_Setting(FramelessWindow, Ui_Theme):
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
