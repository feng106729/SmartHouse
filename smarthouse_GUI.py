# from PyQt5.uic.properties import QtGui
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from matplotlib import pyplot

from main import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
 # from PyQt5.QtCore import *
# from epics import PV


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import random

import matplotlib.pyplot as plt
import numpy as np







class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'smarthouse'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()
        # self.dialog = Second(self)


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # creo font bold per label title
        myFont = QtGui.QFont()
        myFont.setBold(True)

        # label titolo
        title = QLabel('SmartHouse',self)
        title.move(350, 10)
        title.setFont(myFont)


        choose = QLabel('Choose a Dataset:', self)
        choose.move(340, 60)


        # bottoni per scegliere il dataset
        button1 = QPushButton('Dataset A', self)
        button1.move(290, 100)
        button1.clicked.connect(lambda: self.on_button(1))

        button2 = QPushButton('Dataset B', self)
        button2.move(410, 100)
        button2.clicked.connect(lambda: self.on_button(2))


        # RESULTS
        self.truth_label = QLabel('Ground truth:', self)
        self.truth_label.move(20, 150)
        self.truth_label.setFont(myFont)
        self.truth_label.hide()

        self.truth_states_label = QLabel(self)
        self.truth_states_label.move(20, 170)

        self.pred_label = QLabel('Predicted: ', self)
        self.pred_label.move(20,300)
        self.pred_label.setFont(myFont)
        self.pred_label.hide()

        self.pred_states_label = QLabel(self)
        self.pred_states_label.move(20, 320)


        self.accuracy_label = QLabel('Accuracy: ', self)
        self.accuracy_label.move(20, 450)
        self.accuracy_label.setFont(myFont)
        self.accuracy_label.hide()

        self.accuracy_value_label = QLabel(self)
        self.accuracy_value_label.move(20, 470)

        self.show()







    def show_results(self, list_truth, list_pred, accuracy):
        self.truth_label.show()

        self.truth_states_label.setText(str(list_truth))
        self.truth_states_label.adjustSize()

        self.pred_label.show()

        self.pred_states_label.setText(str(list_pred))
        self.pred_states_label.adjustSize()

        self.accuracy_label.show()

        self.accuracy_value_label.setText(str(accuracy) + " %")
        self.accuracy_value_label.adjustSize()



    def hide_results(self):
        self.truth_label.hide()
        self.pred_label.hide()
        self.truth_states_label.hide()
        self.pred_states_label.hide()
        self.accuracy_label.hide()





    def on_button(self, n):

        # controllo se è il primo avvio
        first_start = True
        # se non è il primo avvio nascondo tutte le label dei risultati
        if not first_start:
            self.hide_results()

        list_pred, pred, list_truth, n_states, accuracy = calculate(n)

        self.show_results(list_truth, list_pred, accuracy)

        first_start = False







# Finestra di visualizzazione delle matrici di probabilità
# class Second(QMainWindow):
#     def __init__(self, parent=App):
#         super(Second, self).__init__(parent)
#         self.title = 'smarthouse'
#         self.left = 100
#         self.top = 100
#         self.width = 400
#         self.height = 200
#         self.initUI()
#
#     def initUI(self):
#         l1 = QLabel('SmartHouse', self)
#         l1.move(150, 10)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
