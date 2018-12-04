import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, \
    QAction, QTabWidget, QVBoxLayout, QFrame, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QRect
from functools import partial
from daeshin import Daeshin


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 300
        self.top = 300
        self.width = 1000
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # create frame for a set of checkbox
        self.frame1 = QFrame(self)
        self.frame1.setGeometry(QRect(40, 40, 250, 80))
        # push button to display output on label
        self.btn2 = QPushButton(self.frame1, text="Submit")
        # location of btn relative to frame2 i.e. (40+0, 40+20)
        self.btn2.move(100, 30)
        a = Daeshin()
        logincheck = a.login()
        self.btn2.clicked.connect(partial(self.calluser, logincheck))

        # selected value will be displayed on label
        self.label2 = QLabel(self.frame1)
        self.label2.move(0, 40)
        self.label2.setText("로그인 확인")

        self.label3 = QLabel(self.frame1)
        self.label3.move(250, 40)

        # Add tabs
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)

        # Create Second tab
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(self.frame1)
        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def calluser(self, name):
        self.label3.setText(str(name))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())