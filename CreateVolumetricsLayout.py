from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import sqlite3
import sys
import datetime

class VolumetricsWindow(QWidget):
    """Window"""
    #constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Irigation system - Volumetrics")

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("FlowerbedDatabase.db")
        self.db.open()

        self.create_volumetrics_layout()
        self.setLayout(self.volumetrics_layout)

    def create_volumetrics_layout(self):
        self.volumetrics_layout = QVBoxLayout()

        self.layout1 = QHBoxLayout()
        self.layout2 = QGridLayout()
        self.layout3 = QGridLayout()
        self.layout4 = QHBoxLayout()

        self.titleFont = QFont()
        self.titleFont.setPointSize(13)
        self.titleFont.setBold(True)

        #layout 1
        self.timeframeLabel = QLabel("Timeframe")
        self.timeframeLabel.setFont(self.titleFont)
        self.timeframeLabel.setFixedWidth(95)

        self.timeframeComboBox = QComboBox()
        self.timeframeComboBox.addItem("24 hours")
        self.timeframeComboBox.addItem("7 days")
        self.timeframeComboBox.addItem("30 days")
        self.timeframeComboBox.addItem("6 months")
        self.timeframeComboBox.addItem("1 year")
        self.timeframeComboBox.addItem("all time")
        self.timeframeComboBox.setFixedWidth(80)
        self.timeframeComboBox.currentIndexChanged.connect(self.select_timeframe)

        self.totalValuesLabel = QLabel("Total Values")
        self.totalValuesLabel.setFont(self.titleFont)
        self.totalValuesLabel.setAlignment(Qt.AlignHCenter)

        self.layout1.addWidget(self.timeframeLabel)
        self.layout1.addWidget(self.timeframeComboBox)
        self.layout1.addWidget(self.totalValuesLabel)
        self.layout1.setAlignment(Qt.AlignTop)

        #layout 3
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.totalVolume = 0
            self.cursor = db2.cursor()
            self.cursor.execute("select amount from Operation")
            for each in self.cursor.fetchall():
                for each in each:
                    self.totalVolume += float(each)
            self.totalVolumeString = str(self.totalVolume) + " Litres"
                
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.totalCost = 0
            self.cursor = db2.cursor()
            self.cursor.execute("select cost from Operation")
            for each in self.cursor.fetchall():
                for each in each:
                    self.totalCost += float(each)
            self.totalCostString = "£" + str(self.totalCost)
            if self.totalCostString[-2] == ".":
                self.totalCostString += "0"
            elif len(self.totalCostString) == 2:
                self.totalCostString += ".00"
            
        self.volumeWaterLabel2 = QLabel("Volume of water used:")
        self.volumeWaterLabel2.setFixedWidth(110)

        self.volumeLineEdit2 = QLineEdit()
        self.volumeLineEdit2.setFixedWidth(100)
        self.volumeLineEdit2.setText(self.totalVolumeString)
        self.volumeLineEdit2.setReadOnly(True)

        self.costLabel2 = QLabel("Cost:")
        self.costLabel2.setAlignment(Qt.AlignLeft)

        self.costLineEdit2 = QLineEdit()
        self.costLineEdit2.setFixedWidth(100)
        self.costLineEdit2.setText(self.totalCostString)
        self.costLineEdit2.setReadOnly(True)
        
        self.layout3.addWidget(self.volumeWaterLabel2,0,2)
        self.layout3.addWidget(self.volumeLineEdit2,0,3)
        self.layout3.addWidget(self.costLabel2,1,2)
        self.layout3.addWidget(self.costLineEdit2,1,3)
        self.layout3.setAlignment(Qt.AlignLeft)

        #layout 2        
        self.volumeWaterLabel = QLabel("Volume of water used:")
        self.volumeWaterLabel.setFixedWidth(110)

        self.volumeLineEdit = QLineEdit()
        self.volumeLineEdit.setFixedWidth(100)
        self.volumeLineEdit.setText(self.totalVolumeString)
        self.volumeLineEdit.setReadOnly(True)

        self.costLabel = QLabel("Cost:")
        self.costLabel.setAlignment(Qt.AlignLeft)

        self.costLineEdit = QLineEdit()
        self.costLineEdit.setFixedWidth(100)
        self.costLineEdit.setText(self.totalCostString)
        self.costLineEdit.setReadOnly(True)

        self.layout2.addWidget(self.volumeWaterLabel,0,0)
        self.layout2.addWidget(self.volumeLineEdit,0,1)
        self.layout2.addWidget(self.costLabel,1,0)
        self.layout2.addWidget(self.costLineEdit,1,1)
        self.layout2.setAlignment(Qt.AlignLeft)

        #layout 4
        self.layout4.addLayout(self.layout2)
        self.layout4.addLayout(self.layout3)
        self.layout4.setAlignment(Qt.AlignTop)
        

        #add layouts
        self.volumetrics_layout.addLayout(self.layout1)
        self.volumetrics_layout.addLayout(self.layout4)
        self.volumetrics_layout.setAlignment(Qt.AlignTop)


        self.volumetrics_layout_widget = QWidget()
        self.volumetrics_layout_widget.setLayout(self.volumetrics_layout)

        return self.volumetrics_layout_widget

    def select_timeframe(self):
        self.currentTimeframe = self.timeframeComboBox.currentIndex()
        if self.currentTimeframe == 0:
            self.comparisonDate = datetime.timedelta(1)
        elif self.currentTimeframe == 1:
            self.comparisonDate = datetime.timedelta(7)
        elif self.currentTimeframe == 2:
            self.comparisonDate = datetime.timedelta(30)
        elif self.currentTimeframe == 3:
            self.comparisonDate = datetime.timedelta(183)
        elif self.currentTimeframe == 4:
            self.comparisonDate = datetime.timedelta(365)
        elif self.currentTimeframe == 5:
            self.comparisonDate = datetime.timedelta(99999)
        else:
            pass
        self.compareDate = datetime.datetime.today() - self.comparisonDate
        self.compareDate = self.compareDate.strftime("%Y/%m/%d")
        values = (self.compareDate,)
        
        #amount
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.totalVolume = 0
            self.cursor = db2.cursor()
            self.cursor.execute("""select amount from Operation
                                   where date > ?""",values)
            for each in self.cursor.fetchall():
                for each in each:
                    self.totalVolume += float(each)
            self.totalVolumeString = str(self.totalVolume) + " Litres"
            self.volumeLineEdit.setText(self.totalVolumeString)

        #cost
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.totalCost = 0
            self.cursor = db2.cursor()
            self.cursor.execute("""select cost from Operation
                                   where date > ?""",values)
            for each in self.cursor.fetchall():
                for each in each:
                    self.totalCost += float(each)
            self.totalCostString = "£" + str(self.totalCost)
            if self.totalCostString[-2] == ".":
                self.totalCostString += "0"
            elif len(self.totalCostString) == 2:
                self.totalCostString += ".00"
            self.costLineEdit.setText(self.totalCostString)

if __name__ == "__main__":
    application = QApplication(sys.argv)
    volumetricsWindow = VolumetricsWindow()
    volumetricsWindow.show()
    volumetricsWindow.raise_()
    volumetricsWindow.resize(800,400)
    application.exec_()
