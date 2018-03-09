#!/usr/bin/env python
#!/usr/bin/python3

import socket
import json
import argparse
import sys
import os

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon


global dinoMasterManifesto

class Dino():

    def __init__(self,keyValue):

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


class AddWindow(QWidget):
    def __init__(self, dinotype):
        super().__init__()
        self.initAddWindow()
        self.dinotype = dinotype

    def initAddWindow(self):
        self.mainLayout = QVBoxLayout()
        self.TopLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.TopLayout)
        self.nameLayout = QHBoxLayout()
        self.nameLabel = QLabel("Name:")
        self.nameText = QLineEdit()
        self.nameLayout.addWidget(self.nameLabel)
        self.nameLayout.addWidget(self.nameText)
        self.mainLayout.addLayout(self.nameLayout)
        self.Tamed = QRadioButton("Tamed")
        self.Bred = QRadioButton("Bred")
        self.TopLayout.addWidget(self.Tamed)
        self.TopLayout.addWidget(self.Bred)
        self.fatherLabel = QLabel("Father:")
        self.motherLabel = QLabel("Mother:")
        self.motherDrop = QComboBox()
        self.fatherDrop = QComboBox()
        self.fatherLayout = QVBoxLayout()
        self.motherLayout = QVBoxLayout()
        self.fatherLayout.addWidget(self.fatherLabel)
        self.fatherLayout.addWidget(self.fatherDrop)
        self.motherLayout.addWidget(self.motherLabel)
        self.motherLayout.addWidget(self.motherDrop)
        self.paternityLayout = QHBoxLayout()
        self.paternityLayout.addLayout(self.fatherLayout)
        self.paternityLayout.addLayout(self.motherLayout)
        self.mainLayout.addLayout(self.paternityLayout)
        self.Tamed.toggled.connect(self.originCheck)

        self.stats = StatsTable(10,2)
        self.stats.removeRow(9)
        self.stats.removeRow(8)
        self.statsLayout = QHBoxLayout()
        self.maleButtLayout = QVBoxLayout()
        self.femaleButtLayout = QVBoxLayout()
        self.statsLayout.addWidget(self.stats)
        self.statsLayout.addLayout(self.maleButtLayout)
        self.statsLayout.addLayout(self.femaleButtLayout)
        self.mainLayout.addLayout(self.statsLayout)
        self.maleButtList = []
        self.femaleButtList = []
        self.maleButtLayout.addStretch()
        self.femaleButtLayout.addStretch()
        for x in range(6):
            tempM = QPushButton("D")
            self.maleButtLayout.addWidget(tempM)
            tempF = QPushButton("M")
            self.femaleButtLayout.addWidget(tempF)
            self.maleButtList.append(tempM)
            self.femaleButtList.append(tempF)

        self.SaveCancelLayout = QHBoxLayout()
        self.saveButt = QPushButton("Save")
        self.cancelButt = QPushButton("Cancel")
        self.SaveCancelLayout.addWidget(self.saveButt)
        self.SaveCancelLayout.addWidget(self.cancelButt)
        self.mainLayout.addLayout(self.SaveCancelLayout)

        self.saveButt.clicked.connect(self.addDino)
        self.cancelButt.clicked.connect(self.cancelAdd)

    def cancelAdd(self,Qitem):
        self.close()

    def addDino(self,Qitem):
        dino = Dino({"name":self.nameText.text(),\
            "type": self.dinotype,\
            "level":float(self.stats.item(0,1).text()),\
            "stats": [float(self.stats.item(2,1).text()),\
                        float(self.stats.item(3,1).text()),\
                        float(self.stats.item(4,1).text()),\
                        float(self.stats.item(5,1).text()),\
                        float(self.stats.item(6,1).text()),\
                        float(self.stats.item(7,1).text())],\
            "sex":self.stats.item(1,1).text(),\
            "mother": "wild",\
            "father": "wild"})
        dinoMasterManifesto.append(dino)
        self.close()

    def originCheck(self, Qitem):
        if (self.Tamed.isChecked()):
            self.motherDrop.setEnabled(False)
            self.fatherDrop.setEnabled(False)
            
        elif (self.Bred.isChecked()):
            self.motherDrop.setEnabled(True)
            self.fatherDrop.setEnabled(True)

        


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
        pass

class ArkBreedingTracker(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global dinoMasterManifesto
        try:
            dinoMasterManifesto = self.load_data(os.getcwd()+'\dinomanifesto.json')
        except Exception as e:
            print(f'Unable to load: Dinomanifesto.json\r\n{e}')
            dinoMasterManifesto = []

        self.ActiveDinos = None
        self.mainLayout = QVBoxLayout()
        self.setGeometry(100,100,450,780)
        self.setWindowTitle('ArkBreedingTracker')
        self.setWindowIcon(QIcon('web.png'))
        self.setLayout(self.mainLayout)
        self.table = StatsTable(10,2)
        self.combo1 = DinoSelect()
        self.mainLayout.addWidget(self.combo1)
        self.combo2 = Dinos()
        self.mainLayout.addWidget(self.combo2)

        self.mainLayout.addWidget(self.table)

        self.AddButton = QPushButton("Add")
        self.DeleteButton = QPushButton("Delete")

        self.buttLayout = QHBoxLayout()
        self.buttLayout.addStretch()
        self.buttLayout.addWidget(self.AddButton)
        self.buttLayout.addWidget(self.DeleteButton)
        self.mainLayout.addLayout(self.buttLayout)


        self.combo1.currentTextChanged.connect(self.UpdateDinoNames)
        self.combo2.currentTextChanged.connect(self.UpdateStats)
        self.AddButton.clicked.connect(self.addDino)
        #self.table.itemChanged.connect(self.checkNumeric)

        self.show()

    def load_data(self,file):
        with open(file, 'r') as content_file:
            content = content_file.read()
            dinos = json.loads(content, object_hook=Dino)
        return dinos

    def addDino(self, Qitem):
        self.addWindow = AddWindow(self.combo1.currentText())
        self.addWindow.show()


    def UpdateStats(self,Qitem):
        global dinoMasterManifesto
        dinoStats = list(filter(lambda x: x.type == self.combo1.currentText() and x.name == self.combo2.currentText(), dinoMasterManifesto))
        for x in range(6):
            hitem = QTableWidgetItem(str(dinoStats[0].stats[x]))
            self.table.setItem(x+2,1,hitem)
        dino = list(filter(lambda x: x.type == self.combo1.currentText() and x.name == self.combo2.currentText(), dinoMasterManifesto))
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
        self.ActiveDinos = list(filter(lambda x: x.type == Qitem, dinoMasterManifesto))
        for dino in self.ActiveDinos:
            self.combo2.addItem(dino.name)

    def closeEvent(self, event):
        try:
            self.saveData()
            event.accept()
        except Exception as e:
            print("Could not save the manifesto")
            event.accept()

    def saveData(self):
        global dinoMasterManifesto
        lines = []
        for dino in dinoMasterManifesto:
            lines.append(json.dumps(dino, default=lambda o: o.__dict__))
        combined = ','.join(lines)
        with open(os.getcwd()+'\dinomanifesto.json', 'w') as file:
            file.write(f'[{combined}]')

    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    abt = ArkBreedingTracker()

    sys.exit(app.exec_())

