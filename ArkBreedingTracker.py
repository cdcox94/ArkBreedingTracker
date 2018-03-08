#!/usr/bin/env python
#!/usr/bin/python3

import socket
import json
import argparse
import sys

from PyQt5.QtWidgets import QTableWidget, QApplication, QWidget, QMainWindow, QTableWidgetItem
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon


class StatsTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.initStatsTable()


    def initStatsTable(self):
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        statList = ['Tamed At','Sex','Health','Stamina','Oxygen','Food','Weight','Damage','Mother','Father']
        
        for x in range(len(statList)):
            hitem = QTableWidgetItem(statList[x])
            hitem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.setItem(x,0,hitem)

class ArkBreedingTracker(QMainWindow):
    """docstring for ArkBreedingTracker"""
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(100,100,1440,720)
        self.setWindowTitle('ArkBreedingTracker')
        self.setWindowIcon(QIcon('web.png'))
        
        self.table = StatsTable(10,2)
        self.setCentralWidget(self.table)

        self.table.itemChanged.connect(checkNumeric)

        self.show()

def checkNumeric(Qitem):
    try:
        test = float(Qitem.text())

    except ValueError:
            Qitem.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    abt = ArkBreedingTracker()

    sys.exit(app.exec_())