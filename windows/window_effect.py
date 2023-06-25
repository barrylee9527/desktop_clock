# coding:utf-8

from ctypes import POINTER, WinDLL, byref, c_bool, c_int, pointer, sizeof
from ctypes.wintypes import DWORD, LONG, LPCVOID

import win32api, win32gui
from win32.lib import win32con

from .c_structures import (ACCENT_POLICY, ACCENT_STATE, DWMNCRENDERINGPOLICY,
                           DWMWINDOWATTRIBUTE, MARGINS,
                           WINDOWCOMPOSITIONATTRIB,
                           WINDOWCOMPOSITIONATTRIBDATA)


class WindowEffect:
    """ 调用windows api实现窗口效果 """

    def __init__(self):
        # 调用api
        self.user32 = WinDLL("user32")
        self.dwmapi = WinDLL("dwmapi")
        self.SetWindowCompositionAttribute = self.user32.SetWindowCompositionAttribute
        self.DwmExtendFrameIntoClientArea = self.dwmapi.DwmExtendFrameIntoClientArea
        self.DwmSetWindowAttribute = self.dwmapi.DwmSetWindowAttribute
        self.SetWindowCompositionAttribute.restype = c_bool
        self.DwmExtendFrameIntoClientArea.restype = LONG
        self.DwmSetWindowAttribute.restype = LONG
        self.SetWindowCompositionAttribute.argtypes = [
            c_int,
            POINTER(WINDOWCOMPOSITIONATTRIBDATA),
        ]
        self.DwmSetWindowAttribute.argtypes = [c_int, DWORD, LPCVOID, DWORD]
        self.DwmExtendFrameIntoClientArea.argtypes = [c_int, POINTER(MARGINS)]
        # 初始化结构体
        # self.accentPolicy = ACCENT_POLICY()
        # self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        # self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value[
        #     0
        # ]
        # self.winCompAttrData.SizeOfData = sizeof(self.accentPolicy)
        # self.winCompAttrData.Data = pointer(self.accentPolicy)

    @staticmethod
    def addWindowAnimation(hWnd):
        """ 打开窗口动画效果

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            窗口句柄
        """
        style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            hWnd,
            win32con.GWL_STYLE,
            style
            | win32con.WS_MAXIMIZEBOX
            | win32con.WS_CAPTION
            | win32con.CS_DBLCLKS
            | win32con.WS_THICKFRAME,
        )


if __name__ == "__main__":
    w = WindowEffect()
    # w.addWindowAnimation(0x00)
    # w.addWindowAnimation(0x01)
    # w.addWindowAnimation(0x02)
    # w.addWindowAnimation(0x03)
    # w.addWindowAnimation(0x04)
    # w.addWindowAnimation(0x05)
    # w.addWindowAnimation(0x06)
    # w.addWindowAnimation(0x07)
    # w.addWindowAnimation(0x08)
    # w.addWindowAnimation(0x09)
    # w.addWindowAnimation(0x0a)
    # w.addWindowAnimation(0x0b)
    # w.addWindowAnimation(0x0c)
    # w.addWindowAnimation(0x0d)
    # w.addWindowAnimation(0x0e)
    # w.addWindowAnimation(0x0f)
    # w.addWindowAnimation(0x10)
    # w.addWindowAnimation(0x11)
    # w.addWindowAnimation(0x12)
    # w.addWindowAnimation(0x13)
    # w.addWindowAnimation(0x14)
    # w.addWindowAnimation(0x15)
    # w.addWindowAnimation(0x16)
    # w.addWindowAnimation(0x17)
    # w.addWindowAnimation(0x18)
    # w.addWindowAnimation(0x19)
    # w.addWindowAnimation(0x1a)
    # w.addWindowAnimation(0x1b)
    # w.addWindowAnimation(0x1c)
    # w.addWindowAnimation(0x1d)
    # w.addWindowAnimation(0x1e)
    # w.addWindowAnimation(0x1f)
    # w.addWindowAnimation(0x20)
    # w.addWindowAnimation(0x21)
    # w.addWindowAnimation(0x22)
    # w.addWindowAnimation(0x23)
    # w.addWindowAnimation(
