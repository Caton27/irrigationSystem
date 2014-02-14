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

        self.temp = QLabel("")
        self.temp.setFixedWidth(2)
        
        self.layout1_1 = QVBoxLayout()
        self.layout1_1.addWidget(self.sensorTypeLabel)
        self.layout1_1.addWidget(self.sensorTypeComboBox)
        self.layout1_1.addWidget(self.saveChangesPushButton)
        self.layout1_1.setAlignment(Qt.AlignLeft)
        
        self.layout1_2 = QVBoxLayout()
        self.layout1_2.addWidget(self.flowerbedLabel)
        self.layout1_2.addWidget(self.flowerbedComboBox)
        self.layout1_2.addWidget(self.temp)
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

        self.temp = QLabel("")
        self.temp.setFixedWidth(2)
        
        self.pushButtonsLayout = QHBoxLayout()
        self.pushButtonsLayout.addWidget(self.saveChangesPushButton2)
        self.pushButtonsLayout.addWidget(self.temp)
        self.pushButtonsLayout.setAlignment(Qt.AlignLeft)

        self.layout2.addWidget(self.addValveLabel)
        self.layout2.addWidget(self.flowerbedLabel2)
        self.layout2.addWidget(self.flowerbedComboBox2)
        self.layout2.addLayout(self.pushButtonsLayout)
        self.layout2.setAlignment(Qt.AlignVCenter)


        #layout 3
        self.layout3.addWidget(self.addSensorLabel)
        self.layout3.addLayout(self.layout1)
        self.layout3.setAlignment(Qt.AlignTop)


        #divider
        self.divider = QFrame()
        self.divider.setFrameShape(0x0004)

        
        #add layouts
        self.hardware_layout.addLayout(self.layout3)
        self.hardware_layout.addWidget(self.divider)
        self.hardware_layout.addLayout(self.layout2)

        self.hardware_layout_widget = QWidget()
        self.hardware_layout_widget.setLayout(self.hardware_layout)

        return self.hardware_layout_widget
    

    def save_changes_sensor(self):
        self.sensorTypeText = self.sensorTypeComboBox.currentIndex()
        self.flowerbedText = self.flowerbedComboBox.currentIndex()
        if self.sensorTypeText == 1 and self.flowerbedText == 0:
            message = """The following errors occurred when processing the entered values:
> No flowerbed ID number was selected (Required for moisture sensors)"""
            self.message_box(message)
            
        elif self.sensorTypeText == 1:
            with sqlite3.connect("FlowerbedDatabase.db") as db2:
                self.cursor = db2.cursor()
                values = (int(self.flowerbedText),)
                self.cursor.execute("""select sensorID from Sensor
                                        where flowerbedID = ?""", values)
                if len(self.cursor.fetchall()) < 3:
                    with sqlite3.connect("FlowerbedDatabase.db") as db2:
                        self.cursor = db2.cursor()
                        values = (1,int(self.flowerbedText))
                        self.cursor.execute("""insert into Sensor(
                                               sensorTypeID, flowerbedID)
                                               values(?,?)""", values)
                        db2.commit()
                        message = "New moisture sensor added to flowerbed number {0}".format(self.flowerbedText)
                        self.message_box(message)

##                        with sqlite3.connect("FlowerbedDatabase.db") as db2:
##                            self.cursor = db2.cursor()
##                            self.cursor.execute("select sensorID from Sensor")
##                        moisture_sensors_layout_widget_with_scroll_area.moistureSensorsComboBox.addItem(str(self.cursor.fetchall()[-1][0]))

                else:
                    message = """The following errors occurred when processing the entered values:
> Flowerbed number {0} already has the maximum number of moisture sensors"""
                    self.message_box(message)
                
                
        elif self.sensorTypeText == 2:
            with sqlite3.connect("FlowerbedDatabase.db") as db2:
                self.cursor = db2.cursor()
                values = (2,0)
                self.cursor.execute("""insert into Sensor(
                                       sensorTypeID, flowerbedID)
                                       values(?,?)""", values)
                db2.commit()
                message = "New sunlight sensor added"
                self.message_box(message)
                
        elif self.sensorTypeText == 3:
            with sqlite3.connect("FlowerbedDatabase.db") as db2:
                self.cursor = db2.cursor()
                values = (3,0)
                self.cursor.execute("""insert into Sensor(
                                       sensorTypeID, flowerbedID)
                                       values(?,?)""", values)
                db2.commit()
                message = "New rain sensor added"
                self.message_box(message)                        
                    
        else:
            message = """The following errors occurred when processing the entered values:
> No values were entered"""
            self.message_box(message)


    def save_changes_valve(self):
        self.flowerbedText = self.flowerbedComboBox2.currentIndex()
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            values = (self.flowerbedText,)
            self.cursor.execute("select valveID from Valve where flowerbedID = ?", values)
            results = self.cursor.fetchall()
            if self.flowerbedText == 0:
                message = """The following errors occurred when processing the entered values:
> No flowerbed ID number selected""".format(self.flowerbedText)
                self.message_box(message)
            elif len(results) != 0:
                message = """The following errors occurred when processing the entered values:
> Flowerbed number {0} already has an attached valve""".format(self.flowerbedText)
                self.message_box(message)
            else:
                self.cursor.execute("insert into Valve(flowerbedID) values(?)",values)
                message = "New valve added to flowerbed number {0}".format(self.flowerbedText)
                self.message_box(message)
                
            
                

    def message_box(self, message):
        self.message = QMessageBox()
        self.message.setText(message)
        self.message.exec_()


if __name__ == "__main__":
    application = QApplication(sys.argv)
    hardwareWindow = HardwareWindow()
    hardwareWindow.show()
    hardwareWindow.raise_()
    hardwareWindow.resize(400,300)
    application.exec_()

