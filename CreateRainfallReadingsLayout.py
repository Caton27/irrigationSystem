from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import sqlite3
import sys
import datetime

class RainfallWindow(QWidget):
    """Window"""
    #constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Irigation system - Rainfall readings")

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("FlowerbedDatabase.db")
        self.db.open()

        self.create_rainfall_layout()
        self.setLayout(self.rainfall_layout)


    def create_rainfall_layout(self):
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select readingID from Reading where readingTypeID = 3")
            self.numReadings = len(self.cursor.fetchall())
        self.maxHeight = 115 + 30 * (self.numReadings - 3)

        self.rainfall_layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()

        self.titleFont = QFont()
        self.titleFont.setPointSize(13)
        self.titleFont.setBold(True)

        #layout1
        self.timeframeLabel = QLabel("Timeframe")
        self.timeframeLabel.setFont(self.titleFont)
        self.timeframeLabel.setFixedWidth(100)

        self.timeframeComboBox = QComboBox()
        self.timeframeComboBox.addItem("24 hours")
        self.timeframeComboBox.addItem("7 days")
        self.timeframeComboBox.addItem("30 days")
        self.timeframeComboBox.addItem("6 months")
        self.timeframeComboBox.addItem("1 year")
        self.timeframeComboBox.addItem("all time")
        self.timeframeComboBox.setFixedWidth(80)
        self.timeframeComboBox.currentIndexChanged.connect(self.select_timeframe)

        self.layout1.addWidget(self.timeframeLabel)
        self.layout1.addWidget(self.timeframeComboBox)
        self.layout1.setAlignment(Qt.AlignTop)

        #layout 2
        self.rainfallTableView = QTableView()
        self.rainfallTableView.setFixedWidth(434)
        self.rainfallTableView.setMinimumHeight(112)
        self.rainfallTableView.setMaximumHeight(self.maxHeight)

        self.rainfallQuery = QSqlQuery()
        self.rainfallQuery.prepare("""SELECT
                                      date as "Date",
                                      time as "Time",
                                      reading as "Duration",
                                      averageReading as "Depth"
                                      FROM Reading
                                      WHERE readingTypeID = 3""")
        self.rainfallQuery.exec_()
        self.rainfallModel = QSqlQueryModel()
        self.rainfallModel.setQuery(self.rainfallQuery)
        self.rainfallTableView.setModel(self.rainfallModel)

        self.layout2.addWidget(self.rainfallTableView)
        self.layout2.setAlignment(Qt.AlignLeft)
        self.layout2.setAlignment(Qt.AlignTop)


        #add layouts
        self.rainfall_layout.addLayout(self.layout1)
        self.rainfall_layout.addLayout(self.layout2)

        self.rainfall_layout_widget = QWidget()
        self.rainfall_layout_widget.setLayout(self.rainfall_layout)

        return self.rainfall_layout_widget


    def select_timeframe(self):
        #datetime & PyQtSql
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
        self.newQuery = QSqlQuery()
        self.newQuery.prepare("""SELECT
                                      date as "Date",
                                      time as "Time",
                                      reading as "Duration",
                                      averageReading as "Depth"
                                      FROM Reading
                                      WHERE readingTypeID = 3
                                      AND date > ?""")
        self.newQuery.addBindValue(self.compareDate)
        self.newQuery.exec_()
        self.rainfallModel.setQuery(self.newQuery)
        self.rainfallTableView.setModel(self.rainfallModel)



if __name__ == "__main__":
    application = QApplication(sys.argv)
    rainfallWindow = RainfallWindow()
    rainfallWindow.show()
    rainfallWindow.raise_()
    rainfallWindow.resize(500,400)
    application.exec_()
