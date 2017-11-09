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
from netCDF4 import Dataset,netcdftime,num2date
import pandas as pd
import pycountry
import dimarray as da

stations=da.read_nc('data/stations.nc')['stations']

station_names=list(stations.name)
station_lons,station_lats,station_colors,station_icons=[],[],[],[]
for name in stations.name:
        station_lons.append(float(stations[name,'lon']))
        station_lats.append(float(stations[name,'lat']))
        if stations[name,'tide']:
            station_colors.append('red')
            station_icons.append('http://dev.openlayers.org/img/marker-gold.png')
        if stations[name,'tide']==False:
            station_colors.append('green')
            station_icons.append('http://dev.openlayers.org/img/marker-green.png')
