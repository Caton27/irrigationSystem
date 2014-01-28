from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import sqlite3
import sys
import datetime

class HelpWindow(QWidget):
    """Window"""
    #constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Irigation system - Help")

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("FlowerbedDatabase.db")
        self.db.open()

        self.create_help_layout()
        self.setLayout(self.help_layout)

    def create_help_layout(self):
        self.help_layout = QVBoxLayout()

        self.titleFont = QFont()
        self.titleFont.setPointSize(13)
        self.titleFont.setBold(True)

        self.subtitleFont = QFont()
        self.subtitleFont.setPointSize(11)
        self.subtitleFont.setUnderline(True)

        #title
        self.faqLabel = QLabel("""F.A.Q
""")
        self.faqLabel.setFont(self.titleFont)
        self.help_layout.addWidget(self.faqLabel)

        #faq
        self.questions = []
        self.questions.append("Question 1")
        self.questions.append("Question 2")
        self.questions.append("Question 3")
        self.questions.append("Question 4")
        self.questions.append("Question 5")

        self.answers = []
        self.answers.append("""This piece of text represents the answer to question 1

""")
        self.answers.append("""This piece of text represents the answer to question 2

""")
        self.answers.append("""This piece of text represents the answer to question 3

""")
        self.answers.append("""This piece of text represents the answer to question 4

""")
        self.answers.append("""This piece of text represents the answer to question 5

""")

        num = 0
        for each in self.questions:
            self.questionLabel = QLabel("{0}. {1}:".format(num + 1, each))
            self.questionLabel.setFont(self.subtitleFont)
            
            self.answerLabel = QLabel(self.answers[num])
            self.answerLabel.setWordWrap(True)
            num += 1

            self.faqLayout = QVBoxLayout()
            self.faqLayout.addWidget(self.questionLabel)
            self.faqLayout.addWidget(self.answerLabel)
            self.help_layout.addLayout(self.faqLayout)


        self.help_layout.setAlignment(Qt.AlignTop)


        self.help_layout_widget = QWidget()
        self.help_layout_widget.setLayout(self.help_layout)

        return self.help_layout_widget


if __name__ == "__main__":
    application = QApplication(sys.argv)
    helpWindow = HelpWindow()
    helpWindow.show()
    helpWindow.raise_()
    helpWindow.resize(600,500)
    application.exec_()
