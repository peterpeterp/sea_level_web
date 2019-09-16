# -*- coding: utf-8 -*-

# Copyright (C) 2014 Matthias Mengel and Carl-Friedrich Schleussner
#
# This file is part of wacalc.
#
# wacalc is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# wacalc is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with wacalc; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA




""" database setting file. """


import sys,glob,os,pickle,string
import numpy as np
from netCDF4 import Dataset,num2date
import pandas as pd
import pycountry
import dimarray as da


# basepath is the directory where the app is located
basepath='/Users/peterpfleiderer/Box Sync/Website - Online tools/'
try:
  os.chdir(basepath)
except:
  basepath='/home/tooli/'

basepath+='localSLR/'
os.chdir(basepath)

inland_grids=['grid_14.0_16.0','grid_12.0_16.0','grid_14.0_14.0','grid_12.0_14.0','grid_0.0_32.0','grid_-2.0_32.0','grid_-0.0_34.0','grid_-2.0_34.0','grid_-4.0_30.0','grid_-6.0_30.0','grid_-8.0_30.0','grid_-8.0_32.0','grid_-10.0_34.0','grid_-12.0_34.0','grid_-14.0_34.0','grid_-12.0_36.0','grid_-14.0_36.0','grid_46.0_58.0','grid_46.0_60.0','grid_46.0_62.0','grid_44.0_58.0','grid_44.0_60.0','grid_44.0_62.0','grid_56.0_110.0','grid_54.0_110.0','grid_54.0_108.0','grid_52.0_108.0','grid_52.0_106.0','grid_52.0_106.0','grid_52.0_104.0','grid_62.0_242.0','grid_62.0_244.0','grid_62.0_246.0','grid_62.0_248.0','grid_62.0_250.0','grid_62.0_252.0','grid_60.0_244.0','grid_60.0_246.0','grid_60.0_250.0','grid_60.0_252.0','grid_64.0_238.0','grid_58.0_248.0','grid_58.0_250.0','grid_56.0_256.0','grid_56.0_258.0','grid_58.0_258.0','grid_54.0_260.0','grid_54.0_262.0','grid_52.0_262.0','grid_50.0_262.0','grid_52.0_264.0','grid_50.0_264.0','grid_48.0_268.0','grid_48.0_270.0','grid_48.0_272.0','grid_48.0_274.0','grid_48.0_276.0','grid_50.0_272.0','grid_46.0_268.0','grid_46.0_270.0','grid_46.0_272.0','grid_46.0_274.0','grid_46.0_276.0','grid_46.0_278.0','grid_46.0_280.0','grid_44.0_272.0','grid_44.0_274.0','grid_44.0_276.0','grid_44.0_278.0','grid_44.0_280.0','grid_44.0_282.0','grid_44.0_284.0','grid_42.0_272.0','grid_42.0_274.0','grid_42.0_276.0','grid_42.0_278.0','grid_42.0_280.0','grid_42.0_282.0']

slr=da.read_nc('data/slr.nc')['slr']
slr_copied=da.read_nc('data/slr_copied.nc')['slr']
slr=da.concatenate((slr, slr_copied), axis='ID')


stations=da.read_nc('data/stations.nc')['stations']
stations_copied=da.read_nc('data/stations_copied.nc')['stations']
stations=da.concatenate((stations, stations_copied), axis='name')

station_lons,station_lats,station_names=[],[],[]
grid_xmin,grid_xmax,grid_ymin,grid_ymax,grid_names=[],[],[],[],[]
for name in list(set(stations.name)):
    if stations[name,'tide']:
        station_names.append(name)
        station_lons.append(float(stations[name,'lon']))
        station_lats.append(float(stations[name,'lat']))

    if stations[name,'tide']==False:
        if name not in inland_grids:
            grid_names.append(name)
            grid_xmin.append(float(stations[name,'lon']-1))
            grid_xmax.append(float(stations[name,'lon']+1))
            grid_ymin.append(float(stations[name,'lat']-1))
            grid_ymax.append(float(stations[name,'lat']+1))
