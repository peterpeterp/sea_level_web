import numpy as np
import dimarray as da
import itertools
import seaborn as sns
import pandas as pd

from mpl_toolkits.basemap import Basemap
from shapely.geometry import mapping, Polygon, MultiPolygon
import matplotlib.pylab as plt
from matplotlib import rcParams
import seaborn as sns


slr=da.read_nc('data/slr.nc')['slr']
# plot all
for i in slr.ID:
    plt.close()
    fig = plt.figure(figsize=(5,4))
    plt.plot([2000,2300],[0,0],'k--')
    for rcp,color in zip(['rcp85','rcp45','rcp26'],rcParams['axes.color_cycle'][0:3]):
        plt.fill_between(slr.decade,slr[i,rcp,0.167],slr[i,rcp,0.833],alpha=0.2,color=color)
        plt.plot(slr.decade,slr[i,rcp,0.5],color=color,label=rcp)
    plt.ylabel('Sea level rise [cm]')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig('../app/static/plots/'+str(i)+'.png',dpi=100)
    plt.savefig('../app/static/plots/'+str(i)+'.pdf')
#
#
# slr=ds.read_nc('slr.nc')['slr']
# # plot all
# for i in slr.ID:
#     for rcp in slr.rcp:
#         plt.close()
#         plt.plot([2000,2300],[0,0],'k--')
#         plt.fill_between(slr.decade,slr[i,rcp,0.167],slr[i,rcp,0.833],alpha=0.2)
#         plt.plot(slr.decade,slr[i,rcp,0.5])
#         plt.ylabel('Sea level rise [cm]')
#         plt.savefig('app/static/plots/'+str(i)+'_'+str(rcp)+'.png')
