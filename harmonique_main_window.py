#
# Copyright 2019-2020 Manuel Barrette
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.animation as anim
import os, platform
import particle


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, Dialog, parent):

        self.figure = plt.figure()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 455)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget) # Quitter
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 10, 0, 1, 3)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget) # Exporter vidéo
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 9, 0, 1, 3)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget) # Amplitude
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(5)
        self.horizontalSlider.setPageStep(2)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout.addWidget(self.horizontalSlider, 1, 0, 1, 3)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.horizontalSlider2 = QtWidgets.QSlider(self.centralwidget) # Fréquence
        self.horizontalSlider2.setMinimum(1)
        self.horizontalSlider2.setMaximum(8)
        self.horizontalSlider2.setPageStep(4)
        self.horizontalSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider2.setObjectName("horizontalSlider2")
        self.gridLayout.addWidget(self.horizontalSlider2, 3, 0, 1, 3)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.horizontalSlider3 = QtWidgets.QSlider(self.centralwidget) # Constante de phase
        self.horizontalSlider3.setMinimum(0)
        self.horizontalSlider3.setMaximum(8)
        self.horizontalSlider3.setPageStep(4)
        self.horizontalSlider3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider3.setObjectName("horizontalSlider3")
        self.gridLayout.addWidget(self.horizontalSlider3, 5, 0, 1, 3)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)

        self.horizontalSlider4 = QtWidgets.QSlider(self.centralwidget) # Amortissement
        self.horizontalSlider4.setMinimum(0)
        self.horizontalSlider4.setMaximum(5)
        self.horizontalSlider4.setPageStep(2)
        self.horizontalSlider4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider4.setObjectName("horizontalSlider4")
        self.gridLayout.addWidget(self.horizontalSlider4, 7, 0, 1, 3)


        self.canvas = FigureCanvas(self.figure) # Graphique
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setObjectName("canvas")
        self.gridLayout.addWidget(self.canvas, 0, 3, 9, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1001, 25))
        self.menubar.setObjectName("menubar")
        self.menu_aide = QtWidgets.QMenu(self.menubar)
        self.menu_aide.setObjectName("menu_aide")
        MainWindow.setMenuBar(self.menubar)
        self.action_propos = QtWidgets.QAction(MainWindow)
        self.action_propos.setObjectName("action_propos")
        self.menu_aide.addAction(self.action_propos)
        self.menubar.addAction(self.menu_aide.menuAction())

        # Initial parameters
        self.horizontalSlider.setValue(1)
        self.horizontalSlider2.setValue(4)
        self.horizontalSlider3.setValue(0)
        self.horizontalSlider4.setValue(0)


        # Operating system detection
        self.systeme_exploitation = platform.system()
        if self.systeme_exploitation == "Darwin":
            self.pushButton.setDisabled(True)

        self.retranslateUi(MainWindow)

        # Start animation
        self.animationTempsReel()


        self.action_propos.triggered.connect(lambda: Dialog.show())
        self.horizontalSlider.valueChanged['int'].connect(lambda: self.stopAnim())
        self.horizontalSlider.valueChanged['int'].connect(lambda: self.animationTempsReel())
        self.horizontalSlider2.valueChanged['int'].connect(lambda: self.stopAnim())
        self.horizontalSlider2.valueChanged['int'].connect(lambda: self.animationTempsReel())
        self.horizontalSlider3.valueChanged['int'].connect(lambda: self.stopAnim())
        self.horizontalSlider3.valueChanged['int'].connect(lambda: self.animationTempsReel())
        self.horizontalSlider4.valueChanged['int'].connect(lambda: self.stopAnim())
        self.horizontalSlider4.valueChanged['int'].connect(lambda: self.animationTempsReel())

        self.pushButton.clicked.connect(lambda: self.stopAnim())
        self.pushButton.clicked.connect(lambda: self.exporterAnimation())
        self.pushButton_2.clicked.connect(lambda: plt.close())
        self.pushButton_2.clicked.connect(lambda: self.fermerEtAfficher(MainWindow, parent))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
#        MainWindow.setTabOrder(self.horizontalSlider, self.pushButton_2)

    def retranslateUi(self, MainWindow):
        self._translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(self._translate("MainWindow", "Mouvement harmonique"))
        self.pushButton_2.setText(self._translate("MainWindow", "Quitter"))
        self.pushButton.setText(self._translate("MainWindow", "Exporter en vidéo (.mp4)"))
        self.label.setText(self._translate("MainWindow", "Amplitude (m)"))
        self.label_2.setText(self._translate("MainWindow", "Fréquence (Hz)"))
        self.label_3.setText(self._translate("MainWindow", "Constante de phase (rad)"))
        self.label_4.setText(self._translate("MainWindow", "Amortissement (Hz)"))

        self.menu_aide.setTitle(self._translate("MainWindow", "Aide"))
        self.action_propos.setText(self._translate("MainWindow", "À propos"))

    def disableAll(self, boolean):
        self.horizontalSlider.setDisabled(boolean)
        self.horizontalSlider2.setDisabled(boolean)
        self.horizontalSlider3.setDisabled(boolean)
        self.horizontalSlider4.setDisabled(boolean)
        self.pushButton.setDisabled(boolean)
        self.pushButton_2.setDisabled(boolean)
        self.menu_aide.setDisabled(boolean)
        self.label.setDisabled(boolean)
        self.label_2.setDisabled(boolean)

    def fermerEtAfficher(self, MainWindow, window_autre):
#        if window_autre:
#            window_autre.show()
        app = QtWidgets.QApplication.instance()
        app.closeAllWindows()

    def stopAnim(self):
        self.oscillation.event_source.stop()

    def enregistrer(self):
        if self.systeme_exploitation == 'Windows':
            fichier = QtWidgets.QFileDialog.getSaveFileName(None, self._translate("MainWindow", "Enregister sous..."), os.getenv('HOMEPATH'), 'Vidéos (*.mp4)')
        elif self.systeme_exploitation == 'Darwin' or 'Linux':
            fichier = QtWidgets.QFileDialog.getSaveFileName(None, self._translate("MainWindow", "Enregister sous..."), os.getenv('HOME'), 'Vidéos (*.mp4)')
        else:
            print("Système non supporté officiellement.  Enregistrement dans le dossier de travail sous le nom 'animation.mp4'.")
            fichier = ['animation', None]
        return fichier[0]

    def exporterAnimation(self):
        nom_anim = self.enregistrer()
        if nom_anim[-4:] != ".mp4":
            nom_anim = nom_anim + ".mp4"
        self.oscillation.save(nom_anim)
        self.animationTempsReel()


    def initAnimation(self):
        """ Define parameters and setup the base graphic """

        self.figure.clear()

        # Important parameters
        amplitude = self.horizontalSlider.value()
        omega = self.horizontalSlider.value()*np.pi/8
        constante = self.horizontalSlider.value()*np.pi/8
        amortissement = self.horizontalSlider.value()

        nb_particules_hor = 2
        longueur = 20
        num_frames = 45
        period = 30
#        omega = 2*np.pi/period
        grilley = [0]

        grillex = np.linspace(0, longueur, 100)

        self.ax1 = self.figure.add_subplot(211)
        self.ax2 = self.figure.add_subplot(212, sharex=self.ax1)

        self.ax1.axis([-1, longueur + 1, -1, 1])

        self.ax2.axis([-1, longueur + 1, -1, 1])

        self.ax1.set_xlabel(self._translate("MainWindow", "Temps (s)"))
        self.ax2.set_ylabel(self._translate("MainWindow", "Position (m)"))

#        self.ax1.yaxis.set_label_coords(-0.06, 0.5)
        self.ax1.xaxis.set_label_coords(0.5, -1.1)
        self.ax2.yaxis.set_label_coords(-0.1, 0.5)

        self.ax1.set_yticks([])
#        self.ax2.set_yticks([0])

#        self.ax2.set_yticklabels([r"$0$"])

        self.ax2.grid(True)

#        self.ax1.set_xticks([])

        # Creation of the particle
        intervalle = longueur/(nb_particules_hor)
#        k = 2*np.pi/periode
        balls = []
        for i in range(0, nb_particules_hor-1):
            x_eq = i*intervalle
#            amplitude = 0.5*np.sin(k*(x_eq - node))
            balls.append(particle.Particule(x_eq, amplitude))

        return num_frames, period, omega, balls, grilley, grillex


    def animationTempsReel(self):
        """ Display the animation in real time """

        [num_frames, period, omega, balls, grilley, grillex] = self.initAnimation()

        # Displacement and pressure functions

        deplacement_pos = np.sin(omega*grillex)

        # Plot maximum and minimum curves
#        self.ax2.plot(grillex, deplacement_pos, 'b--')
#        self.ax2.plot(grillex, -deplacement_pos, 'b--')

        graph2, = self.ax2.plot(grillex, 0*deplacement_pos, color='k')

        tempss = np.linspace(0, period-period/num_frames, num_frames)
        self.frames_particles = []

        def update(i):
            for frame in self.frames_particles:
                frame.remove()
            self.frames_particles = []
            temps = tempss[i]
            x = np.sin(omega*temps)
#            deplacement = np.sin(omega*temps)*deplacement_pos
#            graph2.set_ydata(deplacement)
            for ball in balls:
                position = ball.update_position(x)
                for y in grilley:
                    self.frames_particles.append(self.ax1.scatter(position, y, s=150, color='k'))

        self.oscillation = anim.FuncAnimation(self.figure, update, frames=num_frames, repeat=True, interval=40)
        self.canvas.draw()