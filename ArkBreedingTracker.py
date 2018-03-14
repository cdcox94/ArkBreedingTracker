#!/usr/bin/env python
#!/usr/bin/python3

import socket
import json
import argparse
import sys
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon


global dinoMasterManifesto

class Dino():

    def __init__(self,keyValue):

        # import ipdb; ipdb.set_trace()
        self.name = keyValue['name']
        self.level = keyValue['level']
        self.type = keyValue['type']
        self.health = keyValue['health']
        self.stamina = keyValue['stamina']
        self.oxygen = keyValue['oxygen']
        self.food = keyValue['food']
        self.weight = keyValue['weight'] 
        self.damage = keyValue['damage']
        self.sex = keyValue['sex']
        self.mother = keyValue['mother']
        self.father = keyValue['father']

class AddWindow(QWidget):

    closeTrigger = pyqtSignal()
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

        self.stats = QTableWidget(8,1)
        self.stats.setVerticalHeaderLabels(['Tamed at Level','Sex','Health','Stamina','Oxygen','Food','Weight','Damage'])
        self.stats.horizontalHeader().hide()
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
            "level":float(self.stats.item(0,0).text()),\
            "health": float(self.stats.item(2,0).text()),\
            "stamina":float(self.stats.item(3,0).text()),\
            "oxygen":float(self.stats.item(4,0).text()),\
            "food":float(self.stats.item(5,0).text()),\
            "weight":float(self.stats.item(6,0).text()),\
            "damage":float(self.stats.item(7,0).text()),\
            "sex":self.stats.item(1,0).text(),\
            "mother": "wild",\
            "father": "wild"})
        dinoMasterManifesto.append(dino)
        self.closeTrigger.emit()
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
        self.parentList = []
        self.ActiveDinos = []
        self.mainLayout = QVBoxLayout()
        self.setGeometry(100,100,1280,720)
        self.setWindowTitle('ArkBreedingTracker')
        self.setWindowIcon(QIcon('web.png'))
        self.setLayout(self.mainLayout)
        self.combo1 = DinoSelect()
        self.mainLayout.addWidget(self.combo1)
        self.squareLayout = QHBoxLayout()
        self.DinoTable = QTableWidget(0,11)
        self.DinoTable.setHorizontalHeaderLabels(['Name', 'Tamed at Level','Sex','Health','Stamina','Oxygen','Food','Weight','Damage','Mother','Father'])
        self.UpdateStats(self.combo1)
        self.dinoTreeLayout = QGridLayout()
        self.dinoTreeLayout.addWidget(QLabel("Dino1"),1,1)
        self.squareLayout.addLayout(self.dinoTreeLayout)
        self.squareLayout.addWidget(self.DinoTable)
        
        # for x in range(len(self.statList)):
        #     hitem = QTableWidgetItem(self.statList[x])
        #     hitem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        #     self.setItem(x,0,hitem)

        #self.table = StatsTable(10,2)
        #self.combo2 = Dinos()
        #self.mainLayout.addWidget(self.combo2)


        self.mainLayout.addLayout(self.squareLayout)

        self.AddButton = QPushButton("Add")
        self.DeleteButton = QPushButton("Delete")

        self.buttLayout = QHBoxLayout()
        self.buttLayout.addStretch()
        self.buttLayout.addWidget(self.AddButton)
        self.buttLayout.addWidget(self.DeleteButton)
        self.mainLayout.addLayout(self.buttLayout)


        self.combo1.currentTextChanged.connect(self.UpdateStats)
        #self.combo2.currentTextChanged.connect(self.UpdateStats)
        self.AddButton.clicked.connect(self.addDino)
        self.DeleteButton.clicked.connect(self.maxDinoAlgo)
        #self.table.itemChanged.connect(self.checkNumeric)

        self.show()

    def load_data(self,file):
        with open(file, 'r') as content_file:
            content = content_file.read()
            dinos = json.loads(content, object_hook=Dino)
        return dinos

    def addDino(self, Qitem):
        self.addWindow = AddWindow(self.combo1.currentText())
        self.addWindow.closeTrigger.connect(self.UpdateStats)
        self.addWindow.show()

    def UpdateStats(self,Qitem=None):
        global dinoMasterManifesto
        self.DinoTable.clearContents()
        self.DinoTable.setRowCount(0)
        dinoList = list(filter(lambda x: x.type == self.combo1.currentText(), dinoMasterManifesto))
        for dino in dinoList:
            self.DinoTable.insertRow(self.DinoTable.rowCount())
            self.DinoTable.setItem(self.DinoTable.rowCount()-1,0,QTableWidgetItem(str(dino.name)))
            self.DinoTable.setItem(self.DinoTable.rowCount()-1,1,QTableWidgetItem(str(dino.level)))
            self.DinoTable.setItem(self.DinoTable.rowCount()-1,2,QTableWidgetItem(dino.sex))
            self.DinoTable.setItem(self.DinoTable.rowCount()-1,3,QTableWidgetItem(str(dino.health)))
            self.DinoTable.setItem(self.DinoTable.rowCount()-1,4,QTableWidgetItem(str(dino.health)))
            self.DinoTable.setItem(self.DinoTable.rowCount()-1,5,QTableWidgetItem(str(dino.health)))
            self.DinoTable.setItem(self.DinoTable.rowCount()-1,6,QTableWidgetItem(str(dino.health)))
            self.DinoTable.setItem(self.DinoTable.rowCount()-1,7,QTableWidgetItem(str(dino.health)))
            self.DinoTable.setItem(self.DinoTable.rowCount()-1,8,QTableWidgetItem(str(dino.health)))
            self.DinoTable.setItem(self.DinoTable.rowCount()-1,9,QTableWidgetItem(dino.mother))
            self.DinoTable.setItem(self.DinoTable.rowCount()-1,10,QTableWidgetItem(dino.father))
        
    def checkNumeric(self,Qitem):
        try:
            test = float(Qitem.text())
    
        except ValueError:
                Qitem.setText("")

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

    def maxDinoAlgo(self):
        global dinoMasterManifesto
        dinoList = list(filter(lambda x: x.type == self.combo1.currentText(), dinoMasterManifesto))
        for dino in dinoList

        print(seq)
        





if __name__ == '__main__':
    app = QApplication(sys.argv)

    abt = ArkBreedingTracker()

    sys.exit(app.exec_())
