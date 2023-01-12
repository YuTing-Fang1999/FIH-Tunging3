import sys
from PyQt5.QtWidgets import (
    QTabWidget, QStatusBar, QWidget, QLabel,
    QMainWindow, QMessageBox, QToolButton,
    QVBoxLayout, QScrollArea, QSplitter, QTextEdit
)
from PyQt5.QtCore import Qt
from UI.ProjectPage.ProjectPage import ProjectPage
from UI.ROI_Page.ROI_Page import ROI_Page
from UI.ParamPage.ParamPage import ParamPage
from UI.RunPage.RunPage import RunPage
from myPackage.Setting import Setting
from myPackage.Tuning.Tuning import Tuning
from myPackage.Capture import Capture
from myPackage.Param_window import Param_window
from UI.Logger import Logger


import json


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        
    def setup_UI(self, MainWindow):
        MainWindow.setWindowTitle("FIH-Tuning")
        self.param_window = Param_window()
        
        self.central_widget = QWidget(MainWindow)
        wrapper = QVBoxLayout(self.central_widget)
        Vsplitter = QSplitter(Qt.Vertical)

        self.tabWidget = QTabWidget(MainWindow)

        self.project_page = ProjectPage()
        self.ROI_page = ROI_Page()
        self.param_page = ParamPage()
        self.run_page = RunPage()

        self.tabWidget.addTab(self.project_page, "選擇project")
        self.tabWidget.addTab(self.ROI_page, "ROI設定")
        self.tabWidget.addTab(self.param_page, "參數設定")
        self.tabWidget.addTab(self.run_page, "執行")

        Vsplitter.addWidget(self.tabWidget)

        self.logger = Logger()
        Vsplitter.addWidget(self.logger)

        wrapper.addWidget(Vsplitter)

        MainWindow.setCentralWidget(self.central_widget)

        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setStyleSheet(
            """
            * {
                background-color: rgb(124, 124, 124);
            }
            
            QMessageBox QLabel {
                font-size:12pt; font-family:微軟正黑體; color:white;
            }

            QMessageBox QPushButton{
                font-size:12pt; font-family:微軟正黑體; background-color:rgb(255, 170, 0);
            }
            """

        )

    


    



