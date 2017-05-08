#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui, QtCore
from _Controller import Controller
from netCDF4 import Dataset, num2date

styleData = \
    """
QWidget
{
    color: #000000;
    background-color: #77a0a9;
}
QPushButton:pressed
{
    color: #b1b1b1;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
     stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929,
     stop: 0.9 #282828, stop: 1 #252525);
}
QPushButton
{
    color: #ffffff;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
     stop: 0 #565656, stop: 0.1 #525252,
     stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
    border-width: 1px;
    border-color: #1e1e1e;
    border-style: solid;
    border-radius: 8;
    padding: 3px;
    font-size: 12px;
    padding-left: 5px;
    padding-right: 5px;
}
"""


class MainWindow(QtGui.QMainWindow):

    Ws = 1366  # sceen width
    Hs = 768  # sceen Height
    Wa = 720  # app width
    Ha = 480  # app Height

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setCentralWidget(FormWidget(self))
        self.initUI(self.Ws, self.Hs, self.Wa, self.Ha)

    def initUI(self, Ws, Hs, Wa, Ha):

        # set app window position and size

        self.setGeometry((Ws - Wa) / 2, (Hs - Ha) / 2, Wa, Ha)
        self.setWindowTitle('Climate Change')
        self.setWindowIcon(QtGui.QIcon('icon-water.png'))
        self.show()


class FormWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.path = 'jsonFile/_grib2netcdf-Lh8VbrAverage4.json'
        self.data = Controller()
        self.data.default()
        self.__createWidget()
        self.__layout()

    def __createWidget(self):
        self.__plotWidget()
        self.__controlWidget()

    def __plotWidget(self):

        # ================= create Title label =============================

        self.tempAppNameLabel1 = QtGui.QLabel(' ')
        self.appNameLabel = QtGui.QLabel('Climate Change')
        font = self.appNameLabel.font()
        font.setPointSize(33)
        self.appNameLabel.setFont(font)

        # ================= create open button =============================

        self.openFileButton = QtGui.QPushButton('Open', self)
        self.openFileButton.released.connect(self.open)  # pressed

        DefaultPath = '.../jsonFile/_grib2netcdf-Lh8VbrAverage4.json'
        self.pathFileLineEdit = QtGui.QLineEdit(DefaultPath)

        # ================= create ploting Tab =============================

        self.plotingTab = QtGui.QTabWidget()
        plotingTabWidget = [QtGui.QWidget(), QtGui.QWidget(),
                            QtGui.QWidget()]
        self.plotingTab.addTab(plotingTabWidget[0], 'Measurement')
        self.plotingTab.addTab(plotingTabWidget[1], 'Map')
        self.plotingTab.addTab(plotingTabWidget[2], 'Graph')
        self.plotingTab.setCurrentIndex(1)

        self.plotingVbox1 = QtGui.QVBoxLayout(plotingTabWidget[0])
        self.plotingVbox2 = QtGui.QVBoxLayout(plotingTabWidget[1])
        self.plotingVbox3 = QtGui.QVBoxLayout(plotingTabWidget[2])

        # ================= create name table =============================

        self.measurementTable = QtGui.QTableWidget()
        self.measurementTable.setColumnCount(1)
        self.measurementTable.setRowCount(0)
        self.measurementTable.setHorizontalHeaderLabels(['Name'])
        header = self.measurementTable.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.Stretch)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)

    def __controlWidget(self):

        # ========================== Time Tab ===============================

        self.topTab = QtGui.QTabWidget()
        self.topTab.setMaximumWidth(MainWindow.Wa * 2 / 7)

        topTabWidget = [QtGui.QWidget(), QtGui.QWidget()]

        self.topVbox1 = QtGui.QVBoxLayout(topTabWidget[0])
        self.settingVbox = QtGui.QVBoxLayout(topTabWidget[1])

        self.topTab.addTab(topTabWidget[0], 'Time')
        self.topTab.addTab(topTabWidget[1], 'Setting')

        self.dateLabel1 = QtGui.QLabel('Begin Time :')
        self.dateLabel2 = QtGui.QLabel('End Time :')
        self.timeComboBox1 = QtGui.QComboBox(self)
        self.timeComboBox2 = QtGui.QComboBox(self)

        self.timeComboBox2.setMinimumWidth(MainWindow.Wa / 4)

        # =========================== Setting ==============================

        self.shapeLabel = QtGui.QLabel('Shape :')
        self.shapeBox = QtGui.QComboBox(self)
        self.shapeBox.addItem('curve')
        self.shapeBox.addItem('grid')

        self.resolutionLabel = QtGui.QLabel('Resolution :')
        self.resolutionBox = QtGui.QComboBox(self)
        self.resolutionBox.addItem('low')
        self.resolutionBox.addItem('medium')
        self.resolutionBox.addItem('high')

        # ========================== Coordination ===========================

        self.coordinateLabel = QtGui.QLabel('Coordination')
        self.coordinateLabel.font().setPointSize(13)
        self.coordinateLabel.setFont(self.coordinateLabel.font())
        self.coordinateLabel.setMaximumHeight(30)

        self.coTab = QtGui.QTabWidget()
        self.coTab.setMaximumWidth(MainWindow.Wa * 2 / 7)
        coTabWidget = [QtGui.QWidget(), QtGui.QWidget(),
                       QtGui.QWidget()]

        self.coVbox1 = QtGui.QVBoxLayout(coTabWidget[0])
        self.indexVbox = QtGui.QVBoxLayout(coTabWidget[1])

        self.coTab.addTab(coTabWidget[0], 'Edge')
        self.coTab.addTab(coTabWidget[1], 'Indices')

        # ============================= CoVBox1 ===============================

        self.latitudeLabel = QtGui.QLabel('Latitude')
        self.longtitudeLabel = QtGui.QLabel('longtitude')

        # =========== latitude ==============

        self.coLatSlide1 = QtGui.QSlider()
        self.coLatSlide1.setOrientation(QtCore.Qt.Horizontal)
        self.coLatSlide1.setMinimum(-90)
        self.coLatSlide1.setMaximum(90)
        self.coLatSlide2 = QtGui.QSlider()
        self.coLatSlide2.setOrientation(QtCore.Qt.Horizontal)
        self.coLatSlide2.setMinimum(-90)
        self.coLatSlide2.setMaximum(90)

        # =========== longtitude ==============

        self.coLonSlide1 = QtGui.QSlider()
        self.coLonSlide1.setOrientation(QtCore.Qt.Horizontal)
        self.coLonSlide1.setMinimum(0)
        self.coLonSlide1.setMaximum(360)
        self.coLonSlide2 = QtGui.QSlider()
        self.coLonSlide2.setOrientation(QtCore.Qt.Horizontal)
        self.coLonSlide2.setMinimum(0)
        self.coLonSlide2.setMaximum(360)

        # =========== set Default ==============

        self.coLatSlide1.setValue(-90)
        self.coLatSlide2.setValue(90)
        self.coLonSlide2.setValue(360)

        self.coLatHbox = QtGui.QHBoxLayout()
        self.coLonHbox = QtGui.QHBoxLayout()

        # --------------------------------------------------------------------

        self.avgRadioHbox = QtGui.QHBoxLayout()

        self.minRadio = QtGui.QRadioButton('min')
        self.avgRadio = QtGui.QRadioButton('avg')
        self.maxRadio = QtGui.QRadioButton('max')
        self.avgRadio.setChecked(True)

        self.plotButton = QtGui.QPushButton('Create Plot', self)
        self.plotButton.setMinimumHeight(30)
        self.plotButton.pressed.connect(self.createMap)

        # ============================= Index ==============================

        self.indexLabel = QtGui.QLabel('Index List :')
        self.indexLabel.setMaximumHeight(10)
        self.indexBox = QtGui.QComboBox(self)
        self.indexBox.addItem('frost days')
        self.indexBox.addItem('summer days')
        self.indexBox.addItem('icing days')
        self.indexBox.addItem('tropical nights')
        self.indexBox.addItem('R10mm')
        self.indexBox.addItem('R20mm')

        self.indexButtonHbox = QtGui.QHBoxLayout()
        self.mapIndexButton = QtGui.QPushButton('Map', self)
        self.graphIndexButton = QtGui.QPushButton('Index', self)
        self.mapIndexButton.setMinimumHeight(30)
        self.graphIndexButton.setMinimumHeight(30)
        self.mapIndexButton.released.connect(self.createIndexMap)
        self.graphIndexButton.released.connect(self.createGraph)

    def __layout(self):

        # ========================= Ploting ================================

        self.plotingVbox1.addWidget(self.measurementTable)
        self.plotingVbox2.addWidget(self.data.getMap())
        self.plotingVbox2.addWidget(self.data.getToolbar())
        self.plotingVbox3.addWidget(self.data.getGraph('frost days'))
        self.plotingVbox3.addWidget(self.data.getIndexToolbar())

        # ========================= Right Top ================================

        self.topVbox1.addWidget(self.dateLabel1)
        self.topVbox1.addWidget(self.timeComboBox1)
        self.topVbox1.addWidget(self.dateLabel2)
        self.topVbox1.addWidget(self.timeComboBox2)

        # ======================= Right Button ===============================

        self.coLatHbox.addWidget(self.coLatSlide1)
        self.coLatHbox.addWidget(self.coLatSlide2)

        self.coLonHbox.addWidget(self.coLonSlide1)
        self.coLonHbox.addWidget(self.coLonSlide2)

        self.avgRadioHbox.addWidget(self.minRadio)
        self.avgRadioHbox.addWidget(self.avgRadio)
        self.avgRadioHbox.addWidget(self.maxRadio)

        self.coVbox1.addWidget(self.latitudeLabel)
        self.coVbox1.addLayout(self.coLatHbox)
        self.coVbox1.addWidget(self.longtitudeLabel)
        self.coVbox1.addLayout(self.coLonHbox)
        self.coVbox1.addLayout(self.avgRadioHbox)
        self.coVbox1.addWidget(self.plotButton)

        self.indexVbox.addWidget(self.indexLabel)
        self.indexVbox.addWidget(self.indexBox)
        self.indexButtonHbox.addWidget(self.mapIndexButton)
        self.indexButtonHbox.addWidget(self.graphIndexButton)
        self.indexVbox.addLayout(self.indexButtonHbox)

        self.settingVbox.addWidget(self.shapeLabel)
        self.settingVbox.addWidget(self.shapeBox)
        self.settingVbox.addWidget(self.resolutionLabel)
        self.settingVbox.addWidget(self.resolutionBox)

        # ========================= init =========================

        self.vbox1 = QtGui.QVBoxLayout()  # largest up
        self.grid1 = QtGui.QGridLayout()  # Title
        self.hbox2 = QtGui.QHBoxLayout()  # manage frame
        self.vbox2 = QtGui.QVBoxLayout()  # left big ----------
        self.vbox3 = QtGui.QVBoxLayout()  # right big
        self.grid2 = QtGui.QGridLayout()  # open text ---------
        self.vbox5 = QtGui.QVBoxLayout()  # plot map

        # ======================== Ploting ===========================

        self.grid1.addWidget(self.tempAppNameLabel1, 0, 0)
        self.grid1.addWidget(self.tempAppNameLabel1, 0, 2)
        self.grid1.addWidget(self.appNameLabel, 0, 1)

        self.grid2.addWidget(self.openFileButton, 0, 0)
        self.grid2.addWidget(self.pathFileLineEdit, 0, 1)

        self.vbox5.addWidget(self.plotingTab)

        # self.setTable()

        # ======================== control ===========================

        self.vbox3.addWidget(self.topTab)

        self.vbox3.addWidget(self.coordinateLabel)
        self.vbox3.addWidget(self.coTab)

        self.vbox2.addLayout(self.grid2)  # open text -> left big
        self.vbox2.addLayout(self.vbox5)  # plotTab -> left big
        self.hbox2.addLayout(self.vbox2)  # left big -> manage frame
        self.hbox2.addLayout(self.vbox3)  # right big -> manage frame
        self.vbox1.addLayout(self.grid1)  # title -> largest
        self.vbox1.addLayout(self.hbox2)  # manage frame -> largest
        self.setLayout(self.vbox1)  # set all layout

    def createMap(self):

        # get duration of index

        first_index = self.timeComboBox1.currentIndex()
        last_index = self.timeComboBox2.currentIndex()

        # get long_name of value

        row = self.measurementTable.currentRow()
        if row == -1:
            long_name = '2 metre temperature'
        else:
            long_name = str(self.measurementTable.item(row, 0).text())

        # ================== set figure of map =========================

        self.data.setFirstIndex(first_index)
        self.data.setLastIndex(last_index)
        self.data.setLowerlat(self.coLatSlide1.value())
        self.data.setUpperlat(self.coLatSlide2.value())
        self.data.setLowerlon(self.coLonSlide1.value())
        self.data.setUpperlon(self.coLonSlide2.value())
        self.data.setResolution(str(self.resolutionBox.currentText()))
        self.data.setShape(str(self.shapeBox.currentText()))

        if self.minRadio.isChecked():
            _method = 'min'
        elif self.maxRadio.isChecked():
            _method = 'max'
        else:
            _method = 'avg'

        # ========= delete old widget (old map & toobar) =================

        self.clearLayout(self.plotingVbox2)
        self.clearLayout(self.plotingVbox2)

        # ========= set new widget (new map & toobar) ====================

        self.plotingVbox2.addWidget(self.data.setPlotMapValue('nc',
                                    _method,
                                    self.data.setKey(long_name)))
        self.plotingVbox2.addWidget(self.data.getToolbar())
        self.plotingTab.setCurrentIndex(1)

    def createIndexMap(self):

        # ========= delete old widget (old map & toobar) =================

        self.clearLayout(self.plotingVbox2)
        self.clearLayout(self.plotingVbox2)

        # ================== set figure of map =========================

        self.data.setLowerlat(self.coLatSlide1.value())
        self.data.setUpperlat(self.coLatSlide2.value())
        self.data.setLowerlon(self.coLonSlide1.value())
        self.data.setUpperlon(self.coLonSlide2.value())
        self.data.setResolution(str(self.resolutionBox.currentText()))
        self.data.setShape(str(self.shapeBox.currentText()))

        # ========= set new widget (new map & toobar) ====================

        index_name = str(self.indexBox.currentText())
        self.plotingVbox2.addWidget(self.data.setPlotMapValue('json',
                                    0, self.data.setKey(index_name)))
        self.plotingVbox2.addWidget(self.data.getToolbar())
        self.plotingTab.setCurrentIndex(1)

    def createGraph(self):

        # ========= delete old widget (old map & toobar) =================

        self.clearLayout(self.plotingVbox3)
        self.clearLayout(self.plotingVbox3)

        # ========= set new widget (new map & toobar) ====================

        index_name = str(self.indexBox.currentText())
        self.plotingTab.setCurrentIndex(2)
        graph = self.data.getGraph(index_name)
        self.plotingVbox3.addWidget(graph)
        self.plotingVbox3.addWidget(self.data.getIndexToolbar())

    # ============== delete widget in layout method ======================

    def clearLayout(self, layout):

        # platform of deleting widget in layout --- from stackoverflow ---

        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

        if isinstance(item, QtGui.QWidgetItem):
            print 'widget' + str(item)
            item.widget().close()
        elif isinstance(item, QtGui.QSpacerItem):

            print 'spacer ' + str(item)
        else:
            print 'layout ' + str(item)
            self.clearLayout(item.layout())
        layout.removeItem(item)

    def open(self):

        # get path file

        self.path = str(QtGui.QFileDialog.getOpenFileName(self,
                        'OpenFile'))
        self.data.setPath(self.path)
        self.pathFileLineEdit.setText(self.path)  # set path file

        # ========== set new control button ============

        self.setCoordinate()
        self.setTable()
        self.plotingTab.setCurrentIndex(0)

    def setTable(self):

        # ========== set new table ============

        keys = self.data.getKeys().keys()
        self.measurementTable.setRowCount(len(keys))
        for x in xrange(0, len(keys)):
            self.measurementTable.setItem(x, 0, QtGui.QTableWidgetItem(keys[x]))
        self.plotingVbox1.addWidget(self.measurementTable)

    def setCoordinate(self):

        # ============== delete old date ================

        self.timeComboBox1.clear()
        self.timeComboBox2.clear()
        time = self.data.getTime()
        for x in xrange(len(time)):
            self.timeComboBox1.addItem(str(time[x][0]))
            self.timeComboBox2.addItem(str(time[x][0]))

        lat = self.data.getlat()
        lon = self.data.getlon()

        # ============== set slidebar ================

        self.coLatSlide1.setMinimum(lat[0])
        self.coLatSlide1.setMaximum(lat[-1])
        self.coLatSlide1.setValue(lat[0])

        self.coLatSlide2.setMinimum(lat[0])
        self.coLatSlide2.setMaximum(lat[-1])
        self.coLatSlide2.setValue(lat[-1])

        self.coLonSlide1.setMinimum(lon[0])
        self.coLonSlide1.setMaximum(lon[-1])
        self.coLonSlide1.setValue(lon[0])

        self.coLonSlide2.setMinimum(lon[0])
        self.coLonSlide2.setMaximum(lon[-1])
        self.coLonSlide2.setValue(lon[-1])


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    climateChangeApp = MainWindow()
    climateChangeApp.setStyleSheet(styleData)
    sys.exit(app.exec_())
