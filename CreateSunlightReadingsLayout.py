from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import sqlite3
import sys
import datetime

class SunlightWindow(QWidget):
    """Window"""
    #constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Irigation system - Sunlight readings")

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("FlowerbedDatabase.db")
        self.db.open()

        self.create_sunlight_layout()
        self.setLayout(self.sunlight_layout)
        

    def create_sunlight_layout(self):
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select readingID from Reading where readingTypeID = 2")
            self.numReadings = len(self.cursor.fetchall())
        self.maxHeight = 115 + 30 * (self.numReadings - 3)

        self.sunlight_layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()

        self.titleFont = QFont()
        self.titleFont.setPointSize(13)
        self.titleFont.setBold(True)

        #layout 1
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
        self.sunlightTableView = QTableView()
        self.sunlightTableView.setFixedWidth(234)
        self.sunlightTableView.setMinimumHeight(112)
        self.sunlightTableView.setMaximumHeight(self.maxHeight)

        self.sunlightQuery = QSqlQuery()
        self.sunlightQuery.prepare("""SELECT
                                      date as "Date",
                                      reading as "Intensity"
                                      FROM Reading
                                      WHERE readingTypeID = 2""")
        self.sunlightQuery.exec_()
        self.sunlightModel = QSqlQueryModel()
        self.sunlightModel.setQuery(self.sunlightQuery)
        self.sunlightTableView.setModel(self.sunlightModel)

        #################
        #*****GRAPH*****#
        #*****GRAPH*****#
        #*****GRAPH*****#
        #*****GRAPH*****#
        #################

        self.layout2.addWidget(self.sunlightTableView)
        self.layout2.setAlignment(Qt.AlignLeft)
        self.layout2.setAlignment(Qt.AlignTop)


        #add layouts
        self.sunlight_layout.addLayout(self.layout1)
        self.sunlight_layout.addLayout(self.layout2)

        self.sunlight_layout_widget = QWidget()
        self.sunlight_layout_widget.setLayout(self.sunlight_layout)

        return self.sunlight_layout_widget

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
        self.newQuery = QSqlQuery()
        self.newQuery.prepare("""SELECT
                                      date as "Date",
                                      reading as "Intensity"
                                      FROM Reading
                                      WHERE readingTypeID = 2
                                      AND date > ?""")
        self.newQuery.addBindValue(self.compareDate)
        self.newQuery.exec_()
        self.sunlightModel.setQuery(self.newQuery)
        self.sunlightTableView.setModel(self.sunlightModel)

if __name__ == "__main__":
    application = QApplication(sys.argv)
    sunlightWindow = SunlightWindow()
    sunlightWindow.show()
    sunlightWindow.raise_()
    sunlightWindow.resize(600,1400)
    application.exec_()
