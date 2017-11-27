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

import os,glob,sys
from app import app
from flask import redirect, render_template, url_for, request, flash, get_flashed_messages, g, session, jsonify, Flask, send_from_directory
from collections import OrderedDict
from werkzeug.routing import BuildError
import settings
import forms
import json

import numpy as np
from mpl_toolkits.basemap import Basemap
from shapely.geometry import mapping, Polygon, MultiPolygon
import matplotlib.pylab as plt
import seaborn as sns

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field: %s" % (
                getattr(form, field).label.text,
                error
            ))

station_names=settings.station_names
station_lons=settings.station_lons
station_lats=settings.station_lats

grid_names=settings.grid_names
grid_xmin=settings.grid_xmin
grid_xmax=settings.grid_xmax
grid_ymin=settings.grid_ymin
grid_ymax=settings.grid_ymax

stations=settings.stations
slr=settings.slr
languages={'en':'English','fr':'Français'}

@app.route('/')
def index():
  session['language']='en'
  session['location']='index'
  session['name']='MAGUEYES ISLAND'
  #return render_template('feature.html')
  return location(session['name'])

@app.route('/location/<name>')
def location(name):
    s=session
    ID=stations[name,'ID']

    table={}
    for rcp in ['rcp26','rcp45','rcp85']:
        table[rcp]={}
        for year in [2030,2050,2100,2150,2200]:
            table[rcp][year]={'year':year,
                            '50':slr[ID,rcp,0.5,year],
                            '17-83':str(slr[ID,rcp,0.167,year])+'-'+str(slr[ID,rcp,0.833,year]),
                            '5-95':str(slr[ID,rcp,0.05,year])+'-'+str(slr[ID,rcp,0.95,year]),
                            '99.9':slr[ID,rcp,0.999,year]}

    context = {
      'station_names':json.dumps(station_names),
      'station_lons':json.dumps(station_lons),
      'station_lats':json.dumps(station_lats),
      'grid_names':json.dumps(grid_names),
      'grid_xmin':json.dumps(grid_xmin),
      'grid_xmax':json.dumps(grid_xmax),
      'grid_ymin':json.dumps(grid_ymin),
      'grid_ymax':json.dumps(grid_ymax),
      'plot_file':'/static/plots/'+str(int(stations[name,'ID']))+'.png',
      'center_lon':stations[name,'lon'],
      'center_lat':stations[name,'lat'],
      'nstations':len(station_names),
      'ngrid':len(grid_ymax),
      'zoom':5,
      'name':name,
      'table':table,
      'color_dict':{'rcp26':'blue','rcp45':'green','rcp85':'red'}
    }
    s['name']=name
    s['location']='main'
    return render_template('main_en.html',**context)

###############################
# Navigation
###############################
def get_language_tag():
  if session['language']=='fr':
    return(languages['en'])
  if session['language']=='en':
    return(languages['fr'])

@app.route('/language_choice',  methods=('POST', ))
def language_choice():
  if session['language']=='en': lang=0
  if session['language']=='fr': lang=1
  lang*=-1
  session['language']=['en','fr'][lang+1]
  return redirect(url_for(session['location']))

@app.route('/home',  methods=('GET', ))
def render_home():
  return redirect(url_for('index'))

@app.route('/back',  methods=('GET', ))
def back():
  return location(session['name'])

@app.route('/about',  methods=('GET', ))
def render_about():
  return render_template('about.html')

@app.route('/contact',  methods=('GET', ))
def render_contact():
  return render_template('contact.html')

@app.route('/documentation')
def documentation():
  session['location']='documentation'
  return render_template('documentation_'+session['language']+'.html',language=get_language_tag())
