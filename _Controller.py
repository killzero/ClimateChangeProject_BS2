#!/usr/bin/python
# -*- coding: utf-8 -*-
from _mapToPyQt import mapToPyQt
from netCDF4 import Dataset, num2date
from PyQt4 import QtGui, QtCore
import numpy as np
import sys
import os
import json


class Controller:  # QtGui.QDialog

    path = 'jsonFile/_grib2netcdf-Lh8VbrAverage4.json'
    time = []
    resolution = 'c'
    shape = True

    def default(self):

        # ================ default plot jsonfile =====================

        self._map = mapToPyQt()
        with open(self.path) as data_file:
            data = json.load(data_file)
            self.rawlat = data['lat']
            self.lat = self.rawlat
            self.lon = data['lon']
            self.plotingValue = data['Average']['2 metre temperature']
            self.plotingValue = np.array(self.plotingValue) - 273
            data_file.close()
        self.setlat(self.lat)
        self.setlon(self.lon)

        self._map.buildMap(
            '2 metre temperature',
            self.plotingValue,
            self.lat,
            self.lon,
            1,
            'c',
            )
        self.openIndexFile()  # read index .json

    def setPath(self, path):
        self.path = path
        self.readNCFile(path)
        return path

    def getFileName(self, path):
        fileName = os.path.basename(path)
        fileName = os.path.splitext(fileName)[0]
        return fileName

    def getExtension(self, path):
        fileName = os.path.basename(path)
        extension = os.path.splitext(fileName)[1]
        return extension

    def readNCFile(self, path):
        dime = Dataset(path, 'r').dimensions.keys()
        self.data = Dataset(path, 'r')

        # ================ set dimensions (lat lon time) =====================

        for x in xrange(len(dime)):
            if (dime[x])[:3] == 'lat':
                self.rawlat = self.data.variables[dime[x]]
            elif (dime[x])[:3] == 'lon':
                self.lon = self.data.variables[dime[x]]
            elif (dime[x])[:4] == 'time':
                tempTime = self.data.variables[dime[x]]
                for y in xrange(len(self.data.variables[dime[x]])):
                    temp = [self.ncToTime(tempTime, y), tempTime[y]]
                    self.time.append(temp)

        self.setKeys(Dataset(path, 'r'))

        # ================ some time latitude was invert =====================

        if self.rawlat[0] > self.rawlat[-1]:
            self.lat = self.rawlat[::-1]  # invert latitude to correct point

        self.setlat(self.lat)
        self.setlon(self.lon)
        return True

    def ncToTime(self, time, i):

        # ================ return string of date =====================

        temp = str(num2date(time[i], time.units, calendar='standard'))
        temp = temp.split(' ')
        return temp[0]

    def setPlotMapValue(self,  _type,  _method, name):

        # ================ general type is nc =====================

        if _type == 'nc':
            try:
                # get value from GUI
                value = (self.data[self.long_name[self.key]])\
                    [self.first_index:self.last_index + 1]
            except:

                # when file has not been opened ----- so get default value

                value = self.plotingValue
                self._map.buildMap(
                    name,
                    value,
                    self.rawlat,
                    self.getlon(),
                    self.getShape(),
                    self.resolution,
                    )
                return self._map.getMap()

            if name == '2 metre temperature':
                value = value - 273  # kelvin -> celsius

            # select method to get value from GUI

            if _method == 'min':
                value = self.getMinValue(value)
                self._map.buildMap(
                    name,
                    value,
                    self.rawlat,
                    self.getlon(),
                    self.getShape(),
                    self.resolution,
                    )
            elif _method == 'avg':
                value = self.averageValue(value)
                self._map.buildMap(
                    name,
                    value,
                    self.rawlat,
                    self.getlon(),
                    self.getShape(),
                    self.resolution,
                    )
            elif _method == 'max':
                value = self.getMaxValue(value)
                self._map.buildMap(
                    name,
                    value,
                    self.rawlat,
                    self.getlon(),
                    self.getShape(),
                    self.resolution,
                    )
            return self._map.getMap()
        elif _type == 'json':

            # ================ type .json is indices =====================

            value = self.jsonData['map'][name]
            return self._map.buildMap(
                name,
                value,
                self.rawlat,
                self.getlon(),
                self.getShape(),
                self.resolution,
                )

    def averageValue(self, value):

        # use numpy array to average from 3D -> 2D array

        self.plotingValue = np.mean(value, axis=0)
        return self.plotingValue

    def getMinValue(self, value):

        # use numpy array to get index to get min value

        _temp = np.mean(value, axis=1)
        _temp = np.mean(_temp, axis=1)
        _minIndex = np.argmin(_temp, axis=0)

        self.plotingValue = value[_minIndex]
        return self.plotingValue

    def getMaxValue(self, value):

        # use numpy array to get index to get max value

        _temp = np.mean(value, axis=1)
        _temp = np.mean(_temp, axis=1)
        _maxIndex = np.argmax(_temp, axis=0)

        self.plotingValue = value[_maxIndex]
        return self.plotingValue

    def setKey(self, name):
        self.key = name
        return self.key

    def setPoint(self, point):
        self.point = point
        return self.point

    def setKeys(self, data):

        # ===== create dictionary of long_name from short_name =============
        # ============= for easy to get short_name =========================
        # ===== Example { 2 metre temperature' : 't2m' } ===================

        self.long_name = {}
        keys = data.variables.keys()
        for x in xrange(len(keys)):
            name = data.variables[keys[x]].getncattr('long_name')
            temp = {name: keys[x]}
            self.long_name.update(temp)
        dime = data.dimensions.keys()
        for x in xrange(len(dime)):
            name = data.variables[dime[x]].getncattr('long_name')
            del self.long_name[name]
        return self.long_name

    def getKeys(self):
        try:
            return self.long_name
        except:
            return {}

    def getMap(self):
        return self._map.getMap()

    def getToolbar(self):
        return self._map.getToolbar()

    def setResolution(self, value):

        # ==== set resolution for basemap =======

        if value == 'high':
            self.resolution = 'i'
        elif value == 'medium':
            self.resolution = 'l'
        else:
            self.resolution = 'c'
        return self.resolution

    def setShape(self, value):

        # ==== set shape for basemap =======

        if value == 'curve':
            self.shape = True
        else:
            self.shape = False
        return self.shape

    def getShape(self):
        return self.shape

    def getTime(self):
        return self.time

    def getlat(self):
        return self.lat

    def getlon(self):
        return self.lon

    def setFirstIndex(self, index):
        self.first_index = index
        return self.first_index

    def setLastIndex(self, index):
        self.last_index = index
        return self.last_index

    def setUpperlat(self, upperRrightCornerlat):
        self.uplat = upperRrightCornerlat
        self._map.setUpperlat(self.uplat)
        return self.uplat

    def setLowerlat(self, lowerleftCornerlat):
        self.lowlat = lowerleftCornerlat
        self._map.setLowerlat(self.lowlat)
        return self.lowlat

    def setUpperlon(self, upperRightCornerlon):
        self.uplon = upperRightCornerlon
        self._map.setUpperlon(self.uplon)
        return self.uplon

    def setLowerlon(self, lowerleftCornerlon):
        self.lowlon = lowerleftCornerlon
        self._map.setLowerlon(self.lowlon)
        return self.lowlon

    def setlat(self, latitude):
        self.lat = latitude
        self.setUpperlat(latitude[0])
        self.setLowerlat(latitude[-1])
        return self.lat

    def setlon(self, longitude):
        self.lon = longitude
        self.setUpperlon(longitude[-1])
        self.setLowerlon(longitude[0])
        return self.lon

    def getUpperlat(self):
        return self.uplat

    def getLowerlat(self):
        return self.lowlat

    def getUpperlon(self):
        return self.uplon

    def getLowerlon(self):
        return self.lowlon

    def setIndexName(self, name):
        self.index_name = name
        return self.index_name

    def getIndexName(self):
        try:
            return self.index_name
        except:
            return ''

    def openIndexFile(self):
    	path = 'jsonFile/_grib2netcdf-Lh8Vbr_indices4.json'
        with open(path) as data_file:
            self.jsonData = json.load(data_file)

            self.year = self.jsonData['graph']['year']
            self.frost_days = self.jsonData['graph']['frost days']
            self.summer_days = self.jsonData['graph']['summer days']
            self.icing_days = self.jsonData['graph']['icing days']
            self.tropical_nights = self.jsonData['graph'
                    ]['tropical nights']
            self.r10mm = self.jsonData['graph']['R10mm']
            self.r20mm = self.jsonData['graph']['R20mm']

    def getGraph(self, name):
        if name == 'frost days':
            value = self.frost_days
        elif name == 'summer days':
            value = self.summer_days
        elif name == 'icing days':
            value = self.icing_days
        elif name == 'tropical nights':
            value = self.tropical_nights
        elif name == 'R10mm':
            value = self.r10mm
        elif name == 'R20mm':
            value = self.r20mm

        return self._map.getGraph(name, self.year, value)

    def getIndexToolbar(self):
        return self._map.getIndexToolbar()
