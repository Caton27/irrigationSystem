from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import sqlite3
import sys
import datetime

class RelationshipsWindow(QWidget):
    """Window"""
    #constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Irigation system - Relationships")

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("FlowerbedDatabase.db")
        self.db.open()

        self.create_relationships_layout()
        
        self.setLayout(self.relationships_layout)


    def create_relationships_layout(self):
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select flowerbedID from Flowerbed")
            self.flowerbedList = []
            for each1 in self.cursor.fetchall():
                for each2 in each1:
                    self.flowerbedList.append(each2)

        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select valveID from Valve")
            self.valveList = []
            for each1 in self.cursor.fetchall():
                for each2 in each1:
                    self.valveList.append(each2)

        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select sensorID from Sensor where sensorTypeID = 1")
            sensorList = []
            for each1 in self.cursor.fetchall():
                for each2 in each1:
                    sensorList.append(each2)

        self.relationships_layout = QVBoxLayout()
        self.layouts = []
        for each in self.flowerbedList:
            self.layouts.append(QHBoxLayout())

        self.titleFont = QFont()
        self.titleFont.setPointSize(13)
        self.titleFont.setBold(True)

        self.relationshipsLabel = QLabel("Relationships")
        self.relationshipsLabel.setFont(self.titleFont)
        self.relationshipsLabel.setAlignment(Qt.AlignTop)
        self.relationshipsLabel.setAlignment(Qt.AlignLeft)

        self.confirmChangesPushButton = QPushButton("Confirm changes")
        self.confirmChangesPushButton.clicked.connect(self.temp)

        self.clearChangesPushButton = QPushButton("Clear changes")
        self.clearChangesPushButton.clicked.connect(self.update_values)

        self.headingLayout = QHBoxLayout()
        self.headingLayout.addWidget(self.relationshipsLabel)
        self.headingLayout.addWidget(self.confirmChangesPushButton)
        self.headingLayout.addWidget(self.clearChangesPushButton)
        

        #creating the layouts
        num = 0
        for each in self.layouts:
            self.title = "Flowerbed " + str(self.flowerbedList[num]) + ": "
            self.relationshipsGroupBox = QGroupBox(self.title)
            
            self.relationshipsLayout = QHBoxLayout()

            #valves
            self.valveLabel = QLabel("Valve")
            self.valveLabel.setFixedWidth(40)
            self.valveComboBox = QComboBox()
            self.valveComboBox.addItem("-")
            for each2 in self.valveList:
                self.valveComboBox.addItem(str(each2))
            self.valveComboBox.setFixedWidth(30)
            self.valves = QHBoxLayout()
            self.valves.addWidget(self.valveLabel)
            self.valves.addWidget(self.valveComboBox)
<<<<<<< HEAD
            self.valves.addSpacing(130)

=======
            self.get_linked_valves(num)
            
>>>>>>> Scroll bars and resizing completed
            #moisture sensors
            self.sensors = QGridLayout()
            
            self.moistureSensorLabel1 = QLabel("Moisture sensor")
            self.moistureSensorLabel1.setFixedWidth(100)
            self.moistureSensorComboBox1 = QComboBox()
            self.moistureSensorComboBox1.addItem("-")
            for each2 in sensorList:
                self.moistureSensorComboBox1.addItem(str(each2))
            self.moistureSensorComboBox1.setFixedWidth(30)
            self.sensors.addWidget(self.moistureSensorLabel1,0,0)
            self.sensors.addWidget(self.moistureSensorComboBox1,0,1)

            self.moistureSensorLabel2 = QLabel("Moisture sensor")
            self.moistureSensorLabel2.setFixedWidth(100)
            self.moistureSensorComboBox2 = QComboBox()
            self.moistureSensorComboBox2.addItem("-")
            for each2 in sensorList:
                self.moistureSensorComboBox2.addItem(str(each2))
            self.moistureSensorComboBox2.setFixedWidth(30)
            self.sensors.addWidget(self.moistureSensorLabel2,1,0)
            self.sensors.addWidget(self.moistureSensorComboBox2,1,1)

            self.moistureSensorLabel3 = QLabel("Moisture sensor")
            self.moistureSensorLabel3.setFixedWidth(100)
            self.moistureSensorComboBox3 = QComboBox()
            self.moistureSensorComboBox3.addItem("-")
            for each2 in sensorList:
                self.moistureSensorComboBox3.addItem(str(each2))
            self.moistureSensorComboBox1.setFixedWidth(30)
            self.sensors.addWidget(self.moistureSensorLabel3,2,0)
            self.sensors.addWidget(self.moistureSensorComboBox3,2,1)

            self.get_linked_sensors(num)


            self.relationshipsLayout.addSpacing(40)
            self.relationshipsLayout.addLayout(self.valves)
            self.relationshipsLayout.addSpacing(100)
            self.relationshipsLayout.addLayout(self.sensors)
<<<<<<< HEAD
            self.relationshipsLayout.addSpacing(20)
=======
            self.relationshipsLayout.addSpacing(40)
>>>>>>> Scroll bars and resizing completed
            
            
            self.relationshipsGroupBox.setLayout(self.relationshipsLayout)
            each.addWidget(self.relationshipsGroupBox)

            num += 1

        
        #add layouts
        self.relationships_layout.addLayout(self.headingLayout)
        for each in self.layouts:
            self.relationships_layout.addLayout(each)
        

        self.relationships_layout_widget = QWidget()
        self.relationships_layout_widget.setLayout(self.relationships_layout)
        return self.relationships_layout_widget

    def temp(self):
        pass

    def get_linked_valves(self,num):
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            values = (self.flowerbedList[num],)
            self.cursor.execute("select valveID from Valve where flowerbedID = ?", values)
            for each1 in self.cursor.fetchall():
                for each2 in each1:
                    self.valveComboBox.setCurrentIndex(int(each2))

    def get_linked_sensors(self,num):
         with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            values = (self.flowerbedList[num],)
            self.cursor.execute("select sensorID from Sensor where flowerbedID = ?",values)
            temp = self.cursor.fetchall()
            try:
                for each in temp[0]:
                    self.moistureSensorComboBox1.setCurrentIndex(int(each)-2)
                for each in temp[1]:
                    self.moistureSensorComboBox2.setCurrentIndex(int(each)-2)
                for each in temp[2]:
                    self.moistureSensorComboBox3.setCurrentIndex(int(each)-2)
            except IndexError:
                pass

    def update_values(self):
        pass
            

    
if __name__ == "__main__":
    application = QApplication(sys.argv)
    relationshipsWindow = RelationshipsWindow()
    relationshipsWindow.show()
    relationshipsWindow.raise_()
    relationshipsWindow.resize(500,600)
    application.exec_()

