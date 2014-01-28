from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import sqlite3
import sys

class InitialLayoutWindow(QWidget):
    """Window"""
    #constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Irigation system")

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("FlowerbedDatabase.db")
        self.db.open()

        self.create_initial_layout()
        self.setLayout(self.initial_layout)
        

    def create_initial_layout(self):
        self.initial_layout = QVBoxLayout()

        self.welcomeLabel = QLabel("Welcome")
        self.welcomeFont = QFont()
        self.welcomeFont.setPointSize(20)
        self.welcomeFont.setBold(True)
        self.welcomeLabel.setFont(self.welcomeFont)
        self.welcomeLabel.setAlignment(Qt.AlignHCenter|Qt.AlignBottom)
        
        self.messageLabel = QLabel("Select an option from the menu bar to begin using the program")
        self.messageFont = QFont()
        self.messageFont.setPointSize(10)
        self.messageLabel.setFont(self.messageFont)
        self.messageLabel.setAlignment(Qt.AlignHCenter)

        self.initial_layout.addWidget(self.welcomeLabel)
        self.initial_layout.addWidget(self.messageLabel)

        self.initial_layout_widget = QWidget()
        self.initial_layout_widget.setLayout(self.initial_layout)

        return self.initial_layout_widget

if __name__ == "__main__":
    application = QApplication(sys.argv)
    initialWindow = InitialLayoutWindow()
    initialWindow.show()
    initialWindow.raise_()
    initialWindow.resize(600,350)
    application.exec_()
