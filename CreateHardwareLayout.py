from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import sqlite3
import sys
import datetime

class HardwareWindow(QWidget):
    """Window"""
    #constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Irigation system - New hardware")

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("FlowerbedDatabase.db")
        self.db.open()

        self.create_hardware_layout()
        self.setLayout(self.hardware_layout)

    def create_hardware_layout(self):
        self.hardware_layout = QVBoxLayout()

        self.layout1 = QHBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QVBoxLayout()
        self.layout4 = QVBoxLayout()

        self.titleFont = QFont()
        self.titleFont.setPointSize(13)
        self.titleFont.setBold(True)

        self.subtitleFont = QFont()
        self.subtitleFont.setPointSize(11)


        #layout 1
        self.addSensorLabel = QLabel("Add new sensor")
        self.addSensorLabel.setFont(self.titleFont)
        self.addSensorLabel.setAlignment(Qt.AlignTop)
        self.addSensorLabel.setAlignment(Qt.AlignLeft)
        
        self.sensorTypeLabel = QLabel("Sensor type")
        self.sensorTypeLabel.setFixedWidth(200)
        self.sensorTypeLabel.setFont(self.subtitleFont)

        self.flowerbedLabel = QLabel("Flowerbed")
        self.flowerbedLabel.setFixedWidth(200)
        self.flowerbedLabel.setFont(self.subtitleFont)

        self.sensorTypeComboBox = QComboBox()
        self.sensorTypeComboBox.setFixedWidth(70)
        self.sensorTypeComboBox.addItem("-")
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select sensorType from Sensor_Type")
            for each in self.cursor.fetchall():
                for each in each:
                    self.sensorTypeComboBox.addItem(each)

        self.flowerbedComboBox = QComboBox()
        self.flowerbedComboBox.setFixedWidth(30)
        self.flowerbedComboBox.addItem("-")
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select flowerbedID from Flowerbed")
            for each in self.cursor.fetchall():
                for each in each:
                    self.flowerbedComboBox.addItem(str(each))

        self.saveChangesPushButton = QPushButton("Save changes")
        self.saveChangesPushButton.setFixedWidth(100)
        self.saveChangesPushButton.clicked.connect(self.save_changes_sensor)

        self.clearChangesPushButton = QPushButton("Clear changes")
        self.clearChangesPushButton.setFixedWidth(100)
        self.clearChangesPushButton.clicked.connect(self.clear_changes_sensor)

        self.layout1_1 = QVBoxLayout()
        self.layout1_1.addWidget(self.sensorTypeLabel)
        self.layout1_1.addWidget(self.sensorTypeComboBox)
        self.layout1_1.addWidget(self.saveChangesPushButton)
        self.layout1_1.setAlignment(Qt.AlignLeft)
        
        self.layout1_2 = QVBoxLayout()
        self.layout1_2.addWidget(self.flowerbedLabel)
        self.layout1_2.addWidget(self.flowerbedComboBox)
        self.layout1_2.addWidget(self.clearChangesPushButton)
        self.layout1_2.setAlignment(Qt.AlignLeft)

        self.layout1.addLayout(self.layout1_1)
        self.layout1.addLayout(self.layout1_2)
        self.layout1.setAlignment(Qt.AlignTop)


        #layout 2
        self.addValveLabel = QLabel("Add new valve")
        self.addValveLabel.setFont(self.titleFont)
        self.addValveLabel.setAlignment(Qt.AlignTop)
        self.addValveLabel.setAlignment(Qt.AlignLeft)

        self.flowerbedLabel2 = QLabel("Flowerbed")
        self.flowerbedLabel2.setFixedWidth(200)
        self.flowerbedLabel2.setFont(self.subtitleFont)

        self.flowerbedComboBox2 = QComboBox()
        self.flowerbedComboBox2.setFixedWidth(30)
        self.flowerbedComboBox2.addItem("-")
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select flowerbedID from Flowerbed")
            for each in self.cursor.fetchall():
                for each in each:
                    self.flowerbedComboBox2.addItem(str(each))

        self.saveChangesPushButton2 = QPushButton("Save changes")
        self.saveChangesPushButton2.setFixedWidth(100)
        self.saveChangesPushButton2.clicked.connect(self.save_changes_valve)

        self.clearChangesPushButton2 = QPushButton("Clear changes")
        self.clearChangesPushButton2.setFixedWidth(100)
        self.clearChangesPushButton2.clicked.connect(self.clear_changes_valve)
        
        self.pushButtonsLayout = QHBoxLayout()
        self.pushButtonsLayout.addWidget(self.saveChangesPushButton2)
        self.pushButtonsLayout.addWidget(self.clearChangesPushButton2)
        self.pushButtonsLayout.setAlignment(Qt.AlignLeft)

        self.layout2.addWidget(self.flowerbedLabel2)
        self.layout2.addWidget(self.flowerbedComboBox2)
        self.layout2.addLayout(self.pushButtonsLayout)
        self.layout2.setAlignment(Qt.AlignTop)


        #layout 3
        self.layout3.addWidget(self.addSensorLabel)
        self.layout3.addLayout(self.layout1)
        self.layout3.setAlignment(Qt.AlignTop)


        #layout 4
        self.layout4.addWidget(self.addValveLabel)
        self.layout4.addLayout(self.layout2)
        self.layout4.setAlignment(Qt.AlignTop)

        
        #add layouts
        self.hardware_layout.addLayout(self.layout3)
        self.hardware_layout.addLayout(self.layout4)

        self.hardware_layout_widget = QWidget()
        self.hardware_layout_widget.setLayout(self.hardware_layout)

        return self.hardware_layout_widget

    def temp(self):
        pass

    def save_changes_sensor(self):
        pass

    def clear_changes_sensor(self):
        self.sensorTypeComboBox.setCurrentIndex(0)
        self.flowerbedComboBox.setCurrentIndex(0)

    def save_changes_valve(self):
        pass

    def clear_changes_valve(self):
        self.flowerbedComboBox2.setCurrentIndex(0)



if __name__ == "__main__":
    application = QApplication(sys.argv)
    hardwareWindow = HardwareWindow()
    hardwareWindow.show()
    hardwareWindow.raise_()
    hardwareWindow.resize(800,400)
    application.exec_()

