#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from _ncToDict import ncToDict
from _mapToPyQt import mapToPyQt
from _Controller import Controller
from netCDF4 import Dataset
import numpy as np
import json


class TestClimate(unittest.TestCase):

    def setUp(self):
        np.set_printoptions(threshold=np.nan)
        self.read = ncToDict('ncFile/_grib2netcdfChRz9Z.nc')
        self.nc = Dataset('ncFile/_grib2netcdfChRz9Z.nc', 'r')
        self.temp = self.read.timeVar
        with open('jsonFile/ForUnittest/3dArray.json') as data_file:
            data = json.load(data_file)
            self.data = data
        path = 'jsonFile/ForUnittest/average3dArray.json'
        with open(path) as data_file:
            data = json.load(data_file)
            self.data2 = data

        with open('jsonFile/_grib2netcdfChRz9Z_.json') as data_file:
            data = json.load(data_file)
            self.valuePlot = data
        self.c = Controller()

    def test_add_method_returns_correct_ncToDict(self):
        self.assertEqual(self.valuePlot['lat'], self.read.getLatitude())
        self.assertEqual(self.valuePlot['lon'],
                         self.read.getLongitude())

        _list = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]], [[None, 2, 3], [1,
                 2, 3], [1, 2, 3]]]
        _complete = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
        index = self.read.getIndexError(_list)[0]
        self.assertEqual(1, index)
        self.assertEqual(_complete, self.read.removeErrorValue(_list,
                         [index]))

        self.assertEqual(_list, self.read.setLatitude(_list))
        self.assertEqual(_list, self.read.setLongitude(_list))

        self.assertEqual(self.data2,
                         self.read.setMesurement(self.data2))
        self.assertEqual(_list, self.read.setTime(_list))

        time = self.nc.variables['time']
        self.assertEqual('1957-09-01', self.read.ncToTime(time, 0))

    def test_add_method_returns_correct_Controller(self):
        self.assertEqual('Mean sea level pressure',
                         self.c.setKey('Mean sea level pressure'))
        self.assertEqual('_grib2netcdfChRz9Z',
                         self.c.getFileName('_grib2netcdfChRz9Z.nc'))
        self.assertEqual('.nc',
                         self.c.getExtension('_grib2netcdfChRz9Z.nc'))

        self.assertEqual([1, 2, 3], self.c.setKey([1, 2, 3]))
        self.assertEqual('2 metre', self.c.setPoint('2 metre'))
        self.assertEqual(0, self.c.setFirstIndex(0))
        self.assertEqual(0, self.c.setLastIndex(0))
        self.assertEqual('i', self.c.setResolution('high'))

        data = Dataset('ncFile/_grib2netcdfChRz9Z.nc', 'r')
        time = data.variables['time']
        self.assertEqual('1957-09-01', self.c.ncToTime(time, 0))
        self.assertEqual(3, self.c.averageValue([1, 2, 3, 4, 5]))
        temp = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]], [[4, 5, 6], [7, 8,
                9], [7, 7, 7]]]

        self.assertEqual(temp[0], self.c.getMinValue(temp))
        self.assertEqual(temp[1], self.c.getMaxValue(temp))

        self.assertEqual(True, self.c.setShape('curve'))
        self.assertEqual('ICE', self.c.setIndexName('ICE'))


if __name__ == '__main__':
    unittest.main()
