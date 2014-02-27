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
        self.get_the_values()

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
        self.confirmChangesPushButton.clicked.connect(self.update_values)

        self.clearChangesPushButton = QPushButton("Revert changes")
        self.clearChangesPushButton.clicked.connect(self.revert_values)

        self.headingLayout = QHBoxLayout()
        self.headingLayout.addWidget(self.relationshipsLabel)
        self.headingLayout.addWidget(self.confirmChangesPushButton)
        self.headingLayout.addWidget(self.clearChangesPushButton)
        

        #creating the layouts
        #num used to reference the number of group boxes being populated
        num = 0

        #a list is created for each widget that is present for each flowerbed
        self.titleList = []
        self.relationshipsGroupBoxList = []
        self.relationshipsLayoutList = []
        self.valveLabelList = []
        self.valveComboBoxList = []
        self.valvesList = []
        self.sensorsList = []
        self.moistureSensorLabel1List = []
        self.moistureSensorComboBox1List = []
        self.moistureSensorLabel2List = []
        self.moistureSensorComboBox2List = []
        self.moistureSensorLabel3List = []
        self.moistureSensorComboBox3List = []
        
        for each in self.layouts:
            #creates the title widget for group box (num) and added to the list
            self.titleList.append("Flowerbed " + str(self.flowerbedList[num]) + ": ")
            self.relationshipsGroupBoxList.append(QGroupBox(self.titleList[num]))

            #creates the overall QHBoxLayout for group box (num) and added to the list
            self.relationshipsLayoutList.append(QHBoxLayout())

            #valves
            #creates the valve label for group box (num) and added to the list
            self.valveLabelList.append(QLabel("Valve"))
            self.valveLabelList[num].setFixedWidth(40)
            #creates the valve combo box for group box (num) and added to the list
            self.valveComboBoxList.append(QComboBox())
            self.valveComboBoxList[num].addItem("-")
            for each2 in self.valveList:
                self.valveComboBoxList[num].addItem(str(each2))
            self.valveComboBoxList[num].setFixedWidth(50)
            #creates the valve QHBoxLayout for group box (num) and added to the list
            self.valvesList.append(QHBoxLayout())
            self.valvesList[num].addWidget(self.valveLabelList[num])
            self.valvesList[num].addWidget(self.valveComboBoxList[num])
            #calls the function that sets the valve combo box to the correct index based on (num)
            self.get_linked_valves(num)
            
            #moisture sensors
            #creates the sensors grid layout for group box (num) and added to the list
            self.sensorsList.append(QGridLayout())
            
            #creates the first moisture sensor label for group box (num) and added to the list
            self.moistureSensorLabel1List.append(QLabel("Moisture sensor"))
            self.moistureSensorLabel1List[num].setFixedWidth(100)
            #creates the first moisture sensor combo box for group box (num) and added to the list
            self.moistureSensorComboBox1List.append(QComboBox())
            self.moistureSensorComboBox1List[num].addItem("-")
            for each2 in self.sensorList:
                self.moistureSensorComboBox1List[num].addItem(str(each2))
            self.moistureSensorComboBox1List[num].setFixedWidth(50)
            #adds the label and combo box to the layout
            self.sensorsList[num].addWidget(self.moistureSensorLabel1List[num],0,0)
            self.sensorsList[num].addWidget(self.moistureSensorComboBox1List[num],0,1)
            
            #creates the second moisture sensor label for group box (num) and added to the list
            self.moistureSensorLabel2List.append(QLabel("Moisture sensor"))
            self.moistureSensorLabel2List[num].setFixedWidth(100)
            #creates the second moisture sensor combo box for group box (num) and added to the list
            self.moistureSensorComboBox2List.append(QComboBox())
            self.moistureSensorComboBox2List[num].addItem("-")
            for each2 in self.sensorList:
                self.moistureSensorComboBox2List[num].addItem(str(each2))
            self.moistureSensorComboBox2List[num].setFixedWidth(50)
            #adds the label and combo box to the layout
            self.sensorsList[num].addWidget(self.moistureSensorLabel2List[num],1,0)
            self.sensorsList[num].addWidget(self.moistureSensorComboBox2List[num],1,1)
            
            #creates the third moisture sensor label for group box (num) and added to the list
            self.moistureSensorLabel3List.append(QLabel("Moisture sensor"))
            self.moistureSensorLabel3List[num].setFixedWidth(100)
            #creates the third moisture sensor combo box for group box (num) and added to the list
            self.moistureSensorComboBox3List.append(QComboBox())
            self.moistureSensorComboBox3List[num].addItem("-")
            for each2 in self.sensorList:
                self.moistureSensorComboBox3List[num].addItem(str(each2))
            self.moistureSensorComboBox1List[num].setFixedWidth(50)
            #adds the label and combo box to the layout
            self.sensorsList[num].addWidget(self.moistureSensorLabel3List[num],2,0)
            self.sensorsList[num].addWidget(self.moistureSensorComboBox3List[num],2,1)

            #calls the function that sets the moisture sensor combo boxes to the correct index based on (num)
            self.get_linked_sensors(num)

            #adds the 2 layout seperated by spaces to the overall layout
            self.relationshipsLayoutList[num].addSpacing(40)
            self.relationshipsLayoutList[num].addLayout(self.valvesList[num])
            self.relationshipsLayoutList[num].addSpacing(100)
            self.relationshipsLayoutList[num].addLayout(self.sensorsList[num])
            self.relationshipsLayoutList[num].addSpacing(40)
            
            #sets the layout of the group box
            self.relationshipsGroupBoxList[num].setLayout(self.relationshipsLayoutList[num])
            each.addWidget(self.relationshipsGroupBoxList[num])

            #increments the number
            num += 1

        
        #add layouts
        self.relationships_layout.addLayout(self.headingLayout)
        for each in self.layouts:
            self.relationships_layout.addLayout(each)
        

        self.relationships_layout_widget = QWidget()
        self.relationships_layout_widget.setLayout(self.relationships_layout)
        return self.relationships_layout_widget
    

    def get_linked_valves(self,num):
        #this function gets the valveID from the database for a specific flowerbedID
        #then sets the valve combo box based on (num) to the returned value
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            values = (self.flowerbedList[num],)
            self.cursor.execute("select valveID from Valve where flowerbedID = ?", values)
            for each1 in self.cursor.fetchall():
                for each2 in each1:
                    self.valveComboBoxList[num].setCurrentIndex(int(each2))

    def get_linked_sensors(self,num):
        #this function gets the sensorIDs from the database for a specific flowerbedID
        #then sets the 3 moisture sensor combo boxes based on (num) to the returned values
         with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            values = (self.flowerbedList[num],)
            self.cursor.execute("select sensorID from Sensor where flowerbedID = ?",values)
            temp = self.cursor.fetchall()
            #gotTo holds the number of combo boxes that have been asigned sensorIDs
            gotTo = 0
            try:
                for each in temp[0]:
                    num1 = 1
                    for each2 in self.sensorList:
                        if int(each) == int(each2):
                            #the first combo box has its index set
                            self.moistureSensorComboBox1List[num].setCurrentIndex(num1)
                        num1 += 1
                gotTo += 1
                for each in temp[1]:
                    num1 = 1
                    for each2 in self.sensorList:
                        if int(each) == int(each2):
                            #the second combo box has its index set
                            self.moistureSensorComboBox2List[num].setCurrentIndex(num1)
                        num1 += 1
                gotTo += 1
                for each in temp[2]:
                    num1 = 1
                    for each2 in self.sensorList:
                        if int(each) == int(each2):
                            #the third combo box has its index set
                            self.moistureSensorComboBox3List[num].setCurrentIndex(num1)
                        num1 += 1
                gotTo += 1
            except IndexError:
                #the index error occurs if there is less than 3 sensorIDs for the flowerbed
                pass
            #gotTo defines which of the combo boxes get their index set to 0 ("-")
            if gotTo == 3:
                pass
            elif gotTo == 2:
                self.moistureSensorComboBox3List[num].setCurrentIndex(0)
            elif gotTo == 1:
                self.moistureSensorComboBox2List[num].setCurrentIndex(0)
                self.moistureSensorComboBox3List[num].setCurrentIndex(0)
            elif gotTo == 0:
                self.moistureSensorComboBox1List[num].setCurrentIndex(0)
                self.moistureSensorComboBox2List[num].setCurrentIndex(0)
                self.moistureSensorComboBox3List[num].setCurrentIndex(0)

    def get_the_values(self):
        #this function queries the database for all flowerbedIDs, valveIDs and sensorIDs
        #then puts this data into 3 different lists
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select flowerbedID from Flowerbed")
            self.flowerbedList = []
            for each1 in self.cursor.fetchall():
                for each2 in each1:
                    #list holding all flowerbedIDs
                    self.flowerbedList.append(each2)

        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select valveID from Valve")
            self.valveList = []
            for each1 in self.cursor.fetchall():
                for each2 in each1:
                    #list holding all valveIDs
                    self.valveList.append(each2)

        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select sensorID from Sensor where sensorTypeID = 1")
            self.sensorList = []
            for each1 in self.cursor.fetchall():
                for each2 in each1:
                    #list holding all sensorIDs
                    self.sensorList.append(each2)

    def update_values(self):
        #this function updates the relationships based on the combo boxes the user has changed
        num = 0
        self.get_the_values()
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            for each in self.layouts:
                sensors = []
                flowerbed = num + 1
                valve = self.valveComboBoxList[num].currentText()
                sensors.append(self.moistureSensorComboBox1List[num].currentText())
                sensors.append(self.moistureSensorComboBox2List[num].currentText())
                sensors.append(self.moistureSensorComboBox3List[num].currentText())
                values = (flowerbed,valve)
                self.cursor.execute("update Valve set flowerbedID = ? where valveID = ?", values)
                db2.commit()
                for each in sensors:
                    values = (flowerbed, each)
                    self.cursor.execute("update Sensor set flowerbedID = ? where sensorID = ?", values)
                    db2.commit()
                num += 1
        #message box created and shown informing the user the relationships have been updated
        messageBox = QMessageBox()
        messageBox.setText("Relationships updated")
        messageBox.exec_()
        

    def revert_values(self):
        #this function reverts all combo boxes to the current relationships
        num = 0
        self.get_the_values()
        for each in self.layouts:
            self.get_linked_valves(num)
            self.get_linked_sensors(num)
            num += 1
            
    
if __name__ == "__main__":
    application = QApplication(sys.argv)
    relationshipsWindow = RelationshipsWindow()
    relationshipsWindow.show()
    relationshipsWindow.raise_()
    relationshipsWindow.resize(500,600)
    application.exec_()

