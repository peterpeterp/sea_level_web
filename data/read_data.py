import os,sys,glob
import pandas as pd
import dimarray as da

# read original
dat=pd.read_table('data/LSLproj_griddedRCPs.tsv')

# transform to dimarray
stations=sorted(set(dat['STATION']))
IDs=sorted(set(dat['ID']))
rcps=sorted(set(dat['RCP']))
decades=sorted(set(dat['DECADE']))
quantiles=[0.005,0.01,0.05,0.167,0.5,0.833,0.95,0.99,0.995,0.999]
slr=da.DimArray(axes=[IDs,rcps,quantiles,decades],dims=['ID','rcp','quantile','decade'])
for i in slr.ID:
    for rcp in slr.rcp:
        for qu in slr.quantile:
            tmp=dat[(dat['ID']==i) & (dat['RCP']==rcp)]
            slr[i,rcp,qu,tmp['DECADE']]=tmp[str(qu)]

ds=da.Dataset({'slr':slr})
ds.write_nc('data/slr.nc', mode='w')

# stations
stat=pd.read_table('data/Station_LatLon.txt')
stations=da.DimArray(axes=[list(stat['name'][:]),['ID','lon','lat','tide']],dims=['name','info'])
for i in range(len(stat['ID'])):
    stations[stat['name'][i]]=[stat['ID'][i],stat['lon'][i],stat['lat'][i],'grid' not in stat['name'][i].split('_')]

ds=da.Dataset({'stations':stations})
ds.write_nc('data/stations.nc', mode='w')
