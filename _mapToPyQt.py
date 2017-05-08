#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import sys
import numpy as np


class mapToPyQt(QtGui.QDialog):

    def buildMap(self, name, value, lat, lon, shape, resolution):

        # ================ set figure =====================

        self.figure = plt.figure(figsize=(1, 1))
        ax = self.figure.add_subplot(111)
        m = Basemap(
            projection='cyl',
            llcrnrlat=self.lowlat,
            resolution=resolution,
            urcrnrlat=self.uplat,
            llcrnrlon=self.lowlon,
            urcrnrlon=self.uplon,
            ax=ax,
            )

        # ================ set title =====================

        try:
            ax.set_title(name)
        except:
            ax.set_title('Average 2 metre temperature')

        # ================ set meshgrid =====================

        _lats = lat
        _lons = lon

        (lon, lat) = np.meshgrid(_lons, _lats)
        (xi, yi) = m(lon, lat)

        # ================ set color =====================

        data_color = {
            'frost days': 'Blues',
            'summer days': 'Reds',
            'icing days': 'GnBu',
            'tropical nights': 'Oranges',
            'R10mm': 'PuBu',
            'R20mm': 'YlGnBu',
            }
        try:
            color = data_color[name]
        except:
            color = 'jet'

        if shape:
            cs = m.contourf(xi, yi, np.squeeze(value), 110, cmap=color)
        else:
            cs = m.pcolor(xi, yi, np.squeeze(value), cmap=color)

        # ================ set colorbar =====================

        cbar_ax = self.figure.add_axes([0.05, 0.07, 0.9, 0.05])
        self.cbar = self.figure.colorbar(cs, cax=cbar_ax, orientation='horizontal')

        # ================ draw map =====================

        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()
        m.drawparallels(np.arange(_lats[len(_lats) - 1], _lats[0],
                        10.), labels=[1, 0, 0, 0], fontsize=10,
                        color='None')

        self.mapWidget = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.mapWidget, self)

        return self.mapWidget

    def getMap(self):
        return self.mapWidget

    def getToolbar(self):
        return self.toolbar

    def getGraph(self, name, year, value):

        # ================ set figure =====================

        fig = plt.figure(figsize=(1, 1))
        ax = fig.add_subplot(111)

        # ================ set title =====================

        ax.set_title(name)

        # ================ plot trend =====================

        fit1 = np.polyfit(year, value, 1)
        fit_fn1 = np.poly1d(fit1)

        # ================ plot all line =====================

        ax.plot(
            year,
            value,
            'y-o',
            year,
            fit_fn1(year),
            '-',
            )
        graph = FigureCanvas(fig)
        self.indexToolbar = NavigationToolbar(graph, self)
        return graph

    def getIndexToolbar(self):
        return self.indexToolbar

    def setUpperlat(self, upperRrightCornerlat):
        self.uplat = upperRrightCornerlat
        return self.uplat

    def setLowerlat(self, lowerleftCornerlat):
        self.lowlat = lowerleftCornerlat
        return self.lowlat

    def setUpperlon(self, upperRightCornerlon):
        self.uplon = upperRightCornerlon
        return self.uplon

    def setLowerlon(self, lowerleftCornerlon):
        self.lowlon = lowerleftCornerlon
        return self.lowlon

    def setlat(self, latitude):
        self.lat = latitude
        self.setUpperlat(latitude[0])
        self.setLowerlat(latitude[-1])
        return self.lat

    def setlon(self, longitude):
        self.lon = longitude
        self.setUpperlon(longitude[0])
        self.setLowerlon(longitude[-1])
        return self.lon

    def getUpperlat(self):
        return self.uplat

    def getLowerlat(self):
        return self.lowlat

    def getUpperlon(self):
        return self.uplon

    def getLowerlon(self):
        return self.lowlon

    def getlat(self):
        return self.lat

    def getlon(self):
        return self.lon
