#!/usr/bin/env python
#!/usr/bin/python3

import socket
import json
import argparse
import sys
import os

from PyQt5.QtWidgets import QTableWidget, QApplication, QWidget, QMainWindow, QTableWidgetItem, QComboBox, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon

class Dino():

    def __init__(self, keyValue):

        # import ipdb; ipdb.set_trace()
        self.name = keyValue['name']
        self.level = keyValue['level']
        self.type = keyValue['type']
        self.stats = keyValue['stats']
        self.sex = keyValue['sex']
        self.mother = keyValue['mother']
        self.father = keyValue['father']

class StatsTable(QTableWidget):

    def __init__(self, r, c):
        super().__init__(r, c)
        self.initStatsTable()

    def initStatsTable(self):
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

        self.statList = ['Tamed at Level','Sex','Health','Stamina','Oxygen','Food','Weight','Damage','Mother','Father']
        
        for x in range(len(self.statList)):
            hitem = QTableWidgetItem(self.statList[x])
            hitem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.setItem(x,0,hitem)

class DinoSelect(QComboBox):

    def __init__(self):
        super().__init__()
        self.initDinoSelect()

    def initDinoSelect(self):
        filepath = 'dinoList.txt'
        with open(filepath) as fp:
            self.dinolist = fp.readlines()
        for dino in self.dinolist:
            self.addItem(dino.strip())
        
class Dinos(QComboBox):

    def __init__(self):
        super().__init__()
        self.initDinos()

    def initDinos(self):
        self.dinos =None
        try:
            self.dinos = self.load_data(os.getcwd()+'\dinomanifesto.json')
        except Exception as e:
            print(f'Unable to load: Dinomanifesto.json\r\n{e}')
            return

    def load_data(self,file):
        with open(file, 'r') as content_file:
            content = content_file.read()
            dinos = json.loads(content, object_hook=Dino)
        return dinos

class ArkBreedingTracker(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.ActiveDinos = None
        self.layout = QGridLayout()
        self.setGeometry(100,100,450,780)
        self.setWindowTitle('ArkBreedingTracker')
        self.setWindowIcon(QIcon('web.png'))
        self.setLayout(self.layout)
        self.table = StatsTable(10,2)
        self.layout.addWidget(self.table,3,1)
        self.combo1 = DinoSelect()
        self.layout.addWidget(self.combo1,1,1)
        self.combo2 = Dinos()
        self.layout.addWidget(self.combo2,2,1)
        
        self.combo1.currentTextChanged.connect(self.UpdateDinoNames)
        self.combo2.currentTextChanged.connect(self.UpdateStats)
        #self.table.itemChanged.connect(self.checkNumeric)

        self.show()

    def UpdateStats(self,Qitem):
        dinoStats = list(filter(lambda x: x.type == self.combo1.currentText() and x.name == self.combo2.currentText(), self.combo2.dinos))
        for x in range(6):
            hitem = QTableWidgetItem(str(dinoStats[0].stats[x]))
            self.table.setItem(x+2,1,hitem)
        dino = list(filter(lambda x: x.type == self.combo1.currentText() and x.name == self.combo2.currentText(), self.combo2.dinos))
        dinoStats = QTableWidgetItem(str(dino[0].sex))
        self.table.setItem(1,1,dinoStats)

        dinoStats = QTableWidgetItem(str(dino[0].level))
        self.table.setItem(0,1,dinoStats)

        dinoStats = QTableWidgetItem(str(dino[0].mother))
        self.table.setItem(8,1,dinoStats)
        dinoStats = QTableWidgetItem(str(dino[0].father))
        self.table.setItem(9,1,dinoStats)
        
    def checkNumeric(self,Qitem):
        try:
            test = float(Qitem.text())
    
        except ValueError:
                Qitem.setText("")
    
    def UpdateDinoNames(self,Qitem):
        self.combo2.clear()
        self.ActiveDinos = list(filter(lambda x: x.type == Qitem, self.combo2.dinos))
        for dino in self.ActiveDinos:
            self.combo2.addItem(dino.name)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    abt = ArkBreedingTracker()

    sys.exit(app.exec_())
