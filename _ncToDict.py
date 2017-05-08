#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from netCDF4 import Dataset, num2date

class ncToDict:
    latitudeVar = []
    longitudeVar = []
    timeVar = []
    otherDimeVar = {}
    mes = {}

    def __init__(self, path):
        self.path = path
        self.readNCFile(path)

    def readNCFile(self, path):
        nc = Dataset(path, 'r')

        # ----- Dimensions -------------

        dime = nc.dimensions.keys()
        for x in xrange(len(dime)):
            if (dime[x])[:3] == 'lat':
                self.setLatitude((nc.variables[dime[x]])[:].tolist())
            elif (dime[x])[:3] == 'lon':
                self.setLongitude((nc.variables[dime[x]])[:].tolist())
            elif (dime[x])[:4] == 'time':
                tempTime = nc.variables[dime[x]]
                for y in xrange(len(nc.variables[dime[x]])):
                    #tempTime2 = str(num2date(tempTime[x],
                    #                tempTime.units, calendar='365_day'))
                    #tempTime3 = tempTime2.split(' ')
                    temp = [self.ncToTime(tempTime,y),tempTime[y].tolist()]
                    self.addTime(temp)
            else:
                try:
                    tempValue = (nc.variables[dime[x]])[:].tolist()
                    self.addOtherDime({dime[x]: tempValue})
                except:
                    pass

        # http://icclim.readthedocs.io/en/latest/intro.html
        # ------------- Variables ------------ import matplotlib.dates as dt

        Keys = nc.variables.keys()

        for x in xrange(len(dime)):
            try:
                Keys.remove(dime[x])
            except:
                pass

        for x in xrange(len(Keys)):
            long_name = nc.variables[Keys[x]].getncattr('long_name')
            listValue = (nc.variables[Keys[x]])[:].tolist()
            indexError_temp = self.getIndexError(listValue)
            if len(indexError_temp) > 0 :
                indexError = indexError_temp
                listValue = self.removeErrorValue(listValue,indexError)
            try:
                self.addMesurement({long_name: np.around(listValue,
                        decimals=4).tolist()})
            except :
                self.addMesurement({long_name: listValue})
        try:
            self.setTime(self.removeErrorValue(self.getTime(),indexError))
        except :
            pass
        
        temp = np.array(self.getTime())
        self.setTime(np.swapaxes(temp, 0, 1).tolist())

        #print self.getTime()


    def ncToTime(self, time, i):
        temp = str(num2date(time[i],time.units, calendar='standard'))
        temp = temp.split(' ')
        return temp[0]

    def getIndexError(self,_list):
        i = 0
        indexError = []
        while (len(_list) > i):
            if _list[i][0][0] is None :
                del _list[i]
                indexError.append(i)
                i -= 1
            i += 1
        try:
            indexError.remove(0)
        except :
            pass
        return indexError

    def removeErrorValue(self,_list,indexError):
        for x in xrange(len(indexError)):
            try :
                del _list[indexError[x]]
            except :
                pass
        return _list
            
    def average(self, pointVar):
        _sum = 0
        count = 0
        totalAvg = {}

        for x in xrange(len(pointVar.keys())):
            t1 = np.array(pointVar[pointVar.keys()[x]])
            t1 = np.swapaxes(t1, 0, 1)
            t2 = np.swapaxes(t1, 1, 2)
            for i in xrange(len(t2)):
                for j in xrange(len(t2[i])):
                    for k in xrange(len(t2[i][j])):
                        try:
                            _sum += t2[i][j][k]
                            count += 1
                        except TypeError:
                            pass
                    try:
                        t2[i][j][0] = _sum / count
                    except:
                        t2[i][j][0] = 'Error'
                    _sum = 0
                    count = 0

            t2 = np.delete(t2, [1, 2, 3, 4], 2)
            t2 = np.swapaxes(t2, 1, 2)
            t2 = np.swapaxes(t2, 0, 1)
            t3 = {pointVar.keys()[x]: t2.tolist()}
            totalAvg.update(t3)
        return totalAvg

    def average2(self, pointVar):
        totalAvg = {}
        for x in xrange(len(pointVar.keys())):
            t1 = np.array(pointVar[pointVar.keys()[x]])
            t1 = np.mean(t1, axis=0)
            tempDict = {pointVar.keys()[x]: t1.tolist()}
            totalAvg.update(tempDict)
        return totalAvg

    def setLatitude(self, lat):
        self.latitudeVar = lat
        return lat

    def setLongitude(self, lon):
        self.longitudeVar = lon
        return lon


    def setTime(self, time):
        self.timeVar = time
        return self.timeVar

    def setMesurement(self, measurement):
        self.mes = measurement
        return self.mes

    def addTime(self, time):
        self.timeVar.append(time)
        return self.timeVar

    def addMesurement(self, measurement):
        self.mes.update(measurement)
        return self.mes

    def addOtherDime(self, dimension):
        self.otherDimeVar.update(dimension)
        return self.otherDimeVar

    def getLatitude(self):
        return self.latitudeVar

    def getLongitude(self):
        return self.longitudeVar

    def getTime(self):
        return self.timeVar

    def getMesurement(self):  # measurement
        return self.mes

    def getOtherDime(self):  # Dimension
        return self.otherDimeVar

    def getUnits(self):
        return self.units



#if __name__ == '__main__':
#    read = ncToDict('ncFile/_grib2netcdfChRz9Z.nc')
 #   print '--------------------------------------'
 #   print read.getTime()