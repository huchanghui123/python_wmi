#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui

import sys
import hardware


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(320, 240)
        self.center()

        # 设置窗口标题
        self.setWindowTitle('硬件信息')
        self.setWindowIcon(QIcon('icons/wallpaper.ico'))

        # 设置标签
        label = QLabel('获取中...')
        # 设置标签显示在中央
        label.setAlignment(Qt.AlignCenter)

        # 将部件添加到主窗口
        self.setCentralWidget(label)

        self.show()

        self.get_hardware_info()

    def get_hardware_info(self):
        cpu_info = hardware.get_cpu_info()
        disk_info = hardware.get_disk_info()
        memory_info = hardware.get_memory_info()
        network_info = hardware.get_network_info()

        cpu_str = hardware.format_cpu_info(cpu_info)
        disk_str = hardware.format_disk_info(disk_info)
        memory_str = hardware.format_memory_info(memory_info)
        network_str = hardware.format_network_info(network_info)

        hardware_info = 'CPU信息：\n' + cpu_str + '\n硬盘信息：\n' + disk_str + '\n内存信息：\n' + memory_str + '\n网卡信息:\n' + network_str

        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(12)
        label = QLabel(hardware_info)
        label.setAlignment(Qt.AlignLeft)
        label.setFont(font)
        self.setCentralWidget(label)

    # 控制窗口显示在屏幕中心的方法
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Message',
    #                                  "Are you sure to quit?",
    #                                  QMessageBox.Yes |
    #                                  QMessageBox.No)
    #
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
