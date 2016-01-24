import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class WindowWidget(QMainWindow, QObject):
    '''При инициализации передаются именованные аргументы geometry, title, icon, tip.
    geometry = (x, y, width, height)
    title = "Заголовок"
    icon = "Путь/к/файлу/с/иконкой"
    tip = "Подсказка, которая будет выдаваться при наведении." Здесь можно использовать html-теги, главное, в меру.
    '''
    def __init__(self, geometry=(300, 300, 300, 220), title="Title", icon=None, tip=None):  # geometry = (x, y, width, height), icon = name of icon
        QMainWindow.__init__(self)
        super(WindowWidget, self).__init__()
        self.initUI(geometry=geometry, title=title, icon=icon, tip=tip)

    def initUI(self, geometry=(300, 300, 300, 220), title="Title", icon=None, tip=None):
        self.setGeometry(*geometry)
        self.setWindowTitle(title)
        if icon:
            self.setWindowIcon(QIcon(icon))
        # Setting menubar
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        editMenu = menubar.addMenu('&Edit')
        editMenu = QAction

        self.statusbar = self.statusBar()

        self.scan_button = QPushButton("Start scan", self)
        self.scan_button.setToolTip("Press this button to start scanning.")
        self.scan_button.move(10, 33)
        self.scan_button.clicked.connect(self.showThatScanIsStarted)
        self.scan_button.clicked.connect(self.progress)

        self.progressbar = QProgressBar(self)
        self.progressbar.setGeometry(15, geometry[3] - 45, geometry[2] - 20, 15)
        self.progressbar.progress = 0
        self.progressbar.step = 1

        self.ip1 = QLineEdit(self)
        self.ip1.move(130, 33)
        self.ip1.setText("127.0.0.1")
        self.ip2 = QLineEdit(self)
        self.ip2.move(130, 65)
        self.ip2.setText("127.0.0.5")

        self.log = QTextEdit(self)
        self.log.setGeometry(250, 33, 800, 500)
        self.log.blocked = False

        self.show()

    def append(self, text):
        while self.log.blocked:
            pass
        self.log.blocked = True
        tmp = str(self.log.toPlainText()) + "\n" + str(text)
        self.log.setText(tmp)
        self.log.blocked = False

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Title", "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def progress(self, event):
        if self.progressbar.progress < 100:
            self.progressbar.progress = self.progressbar.progress + self.progressbar.step
            if self.progressbar.progress > 100:
                self.progressbar.progress = 100
        else:
            self.scan_button.setText("Scan finished!")
        self.progressbar.setValue(self.progressbar.progress)

    def showThatScanIsStarted(self, event):
        self.statusbar.showMessage("Started scanning!")
        # self.scan_button.
