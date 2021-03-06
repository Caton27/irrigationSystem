from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import sqlite3
import sys
import datetime

class FlowerbedsWindow(QWidget):
    """Window"""
    #constructor
    def __init__(self, delegate):
        super().__init__()
        self.delegate = delegate
        self.setWindowTitle("Irigation system - Flowerbeds")

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("FlowerbedDatabase.db")
        self.db.open()

        #describes how much water is needed to water the flowerbed
        #so that the moisture reading increases by 1
        self.universalVolume = 15.0

        self.create_flowerbeds_layout()
        self.setLayout(self.flowerbeds_layout)


    def create_flowerbeds_layout(self):
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select flowerbedID from Flowerbed")
            flowerbedList = []
            for each1 in self.cursor.fetchall():
                for each2 in each1:
                    #flowerbedList includes all current flowerbedIDs
                    flowerbedList.append(each2)

        self.flowerbeds_layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()
        self.layout4 = QHBoxLayout()

        self.titleFont = QFont()
        self.titleFont.setPointSize(13)
        self.titleFont.setBold(True)

        
        #layout 1
        self.flowerbedLabel = QLabel("Flowerbed")
        self.flowerbedLabel.setFont(self.titleFont)
        self.flowerbedLabel.setFixedWidth(100)

        self.flowerbedsComboBox = QComboBox()
        for each in flowerbedList:
            self.flowerbedsComboBox.addItem(str(each))
        self.flowerbedsComboBox.setFixedWidth(50)
        self.flowerbedsComboBox.currentIndexChanged.connect(self.select_flowerbed)

        self.addFlowerbedButton = QPushButton("Add new flowerbed")
        self.addFlowerbedButton.clicked.connect(self.add_flowerbed)
        self.addFlowerbedButton.setFixedWidth(120)
        self.flowerbedButtonLayout = QHBoxLayout()
        self.flowerbedButtonLayout.addWidget(self.addFlowerbedButton)
        self.flowerbedButtonLayout.setAlignment(Qt.AlignRight)
        
        self.layout1.addWidget(self.flowerbedLabel)
        self.layout1.addWidget(self.flowerbedsComboBox)
        self.layout1.addLayout(self.flowerbedButtonLayout)
        self.layout1.setAlignment(Qt.AlignTop)

        #layout 2
        self.flowerbedTableView = QTableView()
        self.currentFlowerbedID = self.flowerbedsComboBox.currentIndex() + 1
        self.maxHeight = 295
        self.flowerbedQuery = QSqlQuery()
        self.flowerbedQuery.prepare("""SELECT
                                       plantGrowing as "Plant",
                                       datePlanted as "Date Planted",
                                       waterNeed as "Water Need",
                                       notes as "Notes"
                                       FROM Plant
                                       WHERE FlowerbedID = ?""")
        self.flowerbedQuery.addBindValue(self.currentFlowerbedID)
        self.flowerbedQuery.exec_()
        self.flowerbedModel = QSqlQueryModel()
        self.flowerbedModel.setQuery(self.flowerbedQuery)
        self.flowerbedTableView.setModel(self.flowerbedModel)
        self.flowerbedTableView.setColumnWidth(3,400)

        self.flowerbedTableView.setFixedWidth(434)
        self.flowerbedTableView.setMaximumWidth(734)
        self.flowerbedTableView.setMinimumHeight(115)
        self.flowerbedTableView.setMaximumHeight(self.maxHeight)
        
        self.layout2.addWidget(self.flowerbedTableView)
        self.layout2.setAlignment(Qt.AlignLeft)
        self.layout2.setAlignment(Qt.AlignTop)


        #layout 3
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
        self.timeframeComboBox.setCurrentIndex(5)
        self.timeframeComboBox.currentIndexChanged.connect(self.select_timeframe)
        
        self.layout3.addWidget(self.timeframeLabel)
        self.layout3.addWidget(self.timeframeComboBox)
        self.layout3.setAlignment(Qt.AlignTop)

        #layout 4
        self.operationTableView = QTableView()
        self.operationQuery = QSqlQuery()
        #the following query uses cross joins to get 2 different
        #readings from the same table with different foreign keys
        self.operationQuery.prepare("""SELECT
                                       Operation.date as "Date",
                                       Operation.time as "Time",
                                       Operation.duration as "Duration (s)",
                                       Operation.amount as "Amount (L)",
                                       Operation.cost as "Cost (£)",
                                       reading_before.reading as "1st Reading",
                                       reading_after.reading as "2nd Reading"
                                       FROM Operation
                                       CROSS JOIN reading as reading_before
                                       CROSS JOIN reading as reading_after
                                       WHERE Operation.flowerbedID = ?
                                       AND Operation.readingBeforeID = reading_before.readingID
                                       AND Operation.readingAfterID = reading_after.readingID""")

        self.operationQuery.addBindValue(self.currentFlowerbedID)
        self.operationQuery.exec_()
        
        self.operationModel = QSqlQueryModel()
        self.operationModel.setQuery(self.operationQuery)
        self.operationTableView.setModel(self.operationModel)
        
        self.operationTableView.setFixedWidth(734)
        self.operationTableView.setMinimumHeight(115)
        self.operationTableView.setMaximumHeight(self.maxHeight)
        
        self.layout4.addWidget(self.operationTableView)
        self.layout4.setAlignment(Qt.AlignLeft)
        self.layout4.setAlignment(Qt.AlignTop)

        
        #flowerbed links
        self.infoFont = QFont()
        self.infoFont.setPointSize(8)
        self.flowerbedLinks = QLabel()
        self.get_linked()
        self.flowerbedLinks.setFont(self.infoFont)
        self.flowerbedLinks.setAlignment(Qt.AlignBottom)
        
        #add layouts
        self.flowerbeds_layout.addLayout(self.layout1)
        self.flowerbeds_layout.addLayout(self.layout2)
        self.flowerbeds_layout.addLayout(self.layout3)
        self.flowerbeds_layout.addLayout(self.layout4)
        self.flowerbeds_layout.addWidget(self.flowerbedLinks)

        self.flowerbeds_layout_widget = QWidget()
        self.flowerbeds_layout_widget.setLayout(self.flowerbeds_layout)

        return self.flowerbeds_layout_widget

    def select_flowerbed(self):
        #plants
        self.currentFlowerbedID = self.flowerbedsComboBox.currentIndex() + 1
        self.newQuery1 = QSqlQuery()
        self.newQuery1.prepare("""SELECT
                                 plantGrowing as "Plant",
                                 datePlanted as "Date Planted",
                                 waterNeed as "Water Need",
                                 notes as "Notes"
                                 FROM Plant
                                 WHERE FlowerbedID = ?""")
        self.newQuery1.addBindValue(self.currentFlowerbedID)
        self.newQuery1.exec_()
        self.flowerbedModel.setQuery(self.newQuery1)
        self.flowerbedTableView.setModel(self.flowerbedModel)
        #operations
        self.newQuery2 = QSqlQuery()
        self.newQuery2.prepare("""SELECT
                                  Operation.date as "Date",
                                  Operation.time as "Time",
                                  Operation.duration as "Duration (s)",
                                  Operation.amount as "Amount (L)",
                                  Operation.cost as "Cost (£)",
                                  reading_before.reading as "1st Reading",
                                  reading_after.reading as "2nd Reading"
                                  FROM Operation
                                  CROSS JOIN reading as reading_before
                                  CROSS JOIN reading as reading_after
                                  WHERE Operation.flowerbedID = ?
                                  AND Operation.readingBeforeID = reading_before.readingID
                                  AND Operation.readingAfterID = reading_after.readingID""")
        self.newQuery2.addBindValue(self.currentFlowerbedID)
        self.newQuery2.exec_()
        self.operationModel.setQuery(self.newQuery2)
        self.operationTableView.setModel(self.operationModel)
        self.get_linked()
        self.timeframeComboBox.setCurrentIndex(5)



    def select_timeframe(self):
        #datetime & SQLite
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
        self.newQuery3 = QSqlQuery()
        self.newQuery3.prepare("""SELECT
                                  Operation.date as "Date",
                                  Operation.time as "Time",
                                  Operation.duration as "Duration (s)",
                                  Operation.amount as "Amount (L)",
                                  Operation.cost as "Cost (£)",
                                  reading_before.reading as "1st Reading",
                                  reading_after.reading as "2nd Reading"
                                  FROM Operation
                                  CROSS JOIN reading as reading_before
                                  CROSS JOIN reading as reading_after
                                  WHERE Operation.flowerbedID = ?
                                  AND Operation.readingBeforeID = reading_before.readingID
                                  AND Operation.readingAfterID = reading_after.readingID
                                  AND Operation.date > ? """)
        self.newQuery3.addBindValue(self.currentFlowerbedID)
        self.newQuery3.addBindValue(self.compareDate)
        self.newQuery3.exec_()
        self.operationModel.setQuery(self.newQuery3)
        self.operationTableView.setModel(self.operationModel)
        

    #retives relationships between the current flowerbed and which sensors have it as a foreign key
    def get_linked(self):
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            values = (self.currentFlowerbedID,)
            self.cursor.execute("select sensorID from Sensor where flowerbedID = ? and sensorTypeID = 1",values)
            temp = self.cursor.fetchall()
            self.linked = []
            for each in temp:
                for each in each:
                    self.linked.append(each)
            while len(self.linked) < 3:
                self.linked.append("<N/A>")
        self.flowerbedLinks.setText("This flowerbed is currently linked to moisture sensors number {0}, {1} and {2}.".format(self.linked[0],self.linked[1],self.linked[2]))


    #adding a new flowerbed to the database
    def add_flowerbed(self):
        with sqlite3.connect("FlowerbedDatabase.db") as db2:
            self.cursor = db2.cursor()
            self.cursor.execute("select flowerbedID from Flowerbed")
            try:
                newID = ((int(self.cursor.fetchall()[-1][0]) + 1),)
            except IndexError:
                newID = (1,)
            self.cursor.execute("insert into Flowerbed(volume) values(?)",(self.universalVolume,))
            db2.commit()
        self.confirmMessage = QMessageBox()
        self.confirmMessage.setText("New flowerbed with ID no. {0} has been created".format(newID[0]))
        self.confirmMessage.exec_()
        self.flowerbedsComboBox.addItem(str(newID[0]))

        #references a function in RunMe that refreshes flowerbed combo boxes
        self.delegate.refresh_combo_boxes_flowerbed()


if __name__ == "__main__":
    application = QApplication(sys.argv)
    flowerbedsWindow = FlowerbedsWindow()
    flowerbedsWindow.show()
    flowerbedsWindow.raise_()
    flowerbedsWindow.resize(800,550)
    application.exec_()
