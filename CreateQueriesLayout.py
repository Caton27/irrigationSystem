from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import sqlite3
import sys
import datetime

class QueryWindow(QWidget):
    """Window"""
    #constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Irigation system - Custom queries")

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("FlowerbedDatabase.db")
        self.db.open()

        self.create_query_layout()
        self.setLayout(self.query_layout)

    def create_query_layout(self):
        self.query_layout = QVBoxLayout()

        self.layout1 = QHBoxLayout()

        self.titleFont = QFont()
        self.titleFont.setPointSize(13)
        self.titleFont.setBold(True)


        #query
        self.queryLabel = QLabel("Query")
        self.queryLabel.setFont(self.titleFont)

        self.queryTextEdit = QTextEdit()

        self.executeQueryPushButton = QPushButton("Execute query")
        self.executeQueryPushButton.setFixedWidth(120)
        self.executeQueryPushButton.clicked.connect(self.execute_query)

        self.placefillerLabel = QLabel("")
        self.placefillerLabel.setFixedWidth(30)

        self.clearFieldPushButton = QPushButton("Clear fields")
        self.clearFieldPushButton.setFixedWidth(120)
        self.clearFieldPushButton.clicked.connect(self.clear_fields)

        self.layout1.addWidget(self.executeQueryPushButton)
        self.layout1.addWidget(self.placefillerLabel)
        self.layout1.addWidget(self.clearFieldPushButton)
        self.layout1.setAlignment(Qt.AlignLeft)


        #results
        self.resultsLabel = QLabel("Results")
        self.resultsLabel.setFont(self.titleFont)

        self.customQueryText = ""

        self.customTableView = QTableView()
        self.customQuery = QSqlQuery()
        self.customQuery.prepare(self.customQueryText)
        self.customQuery.exec_()
        self.customModel = QSqlQueryModel()
        self.customModel.setQuery(self.customQuery)
        self.customTableView.setModel(self.customModel)


        #add layouts
        self.query_layout.addWidget(self.queryLabel)
        self.query_layout.addWidget(self.queryTextEdit)
        self.query_layout.addLayout(self.layout1)
        self.query_layout.addWidget(self.resultsLabel)
        self.query_layout.addWidget(self.customTableView)

        self.query_layout_widget = QWidget()
        self.query_layout_widget.setLayout(self.query_layout)

        return self.query_layout_widget

    def execute_query(self):
        self.customQueryText = self.queryTextEdit.toPlainText()
        self.newQuery = QSqlQuery()
        self.newQuery.prepare(self.customQueryText)
        self.newQuery.exec_()
        self.customModel.setQuery(self.newQuery)
        self.customTableView.setModel(self.customModel)

    def clear_fields(self):
        self.queryTextEdit.clear()
        self.execute_query()

if __name__ == "__main__":
    application = QApplication(sys.argv)
    queryWindow = QueryWindow()
    queryWindow.show()
    queryWindow.raise_()
    queryWindow.resize(600,500)
    application.exec_()
