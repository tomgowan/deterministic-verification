#%%
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import pygrib, os, sys, glob
from netCDF4 import Dataset
from numpy import *
import numpy as np
from pylab import *
import time
from datetime import date, timedelta
from tempfile import TemporaryFile
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal
from matplotlib.mlab import bivariate_normal
from matplotlib import colors, ticker, cm
from datetime import date, timedelta
from tempfile import TemporaryFile
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import colors, ticker, cm
import matplotlib.lines as mlines


wmont = [-117.0, 43.0, -108.5, 49.0]
utah = [-114.7, 36.7, -108.9, 42.5]
colorado = [-110.0, 36.0, -104.0, 41.9]
wasatch = [-113.4, 39.5, -110.7, 41.9]
cascades = [-125.3, 42.0, -116.5, 49.1]
west = [-125.3, 31.0, -102.5, 49.2]


region = 'west'



if region == 'wmont':
    latlon = wmont
    
if region == 'utah':
    latlon = utah
    
if region == 'colorado':
    latlon = colorado
    
if region == 'wasatch':
    latlon = wasatch
    
if region == 'cascades':
    latlon = cascades

if region == 'west':
    latlon = west
    

###############################################################################
############ Read in  12Z to 12Z data   #######################################
###############################################################################

            
x = 0
q = 0
v = 0
i = 0   

         

links = ["/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/snotel_precip_2016_2017_qc.csv",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/ncarens_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/gfs13km_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/hrrr_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/nam3km_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/sref_arw_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/sref_nmb_precip_12Zto12Z_interp.txt"]

#data = ['inhouse_data', 'ncar_data', 'nam4k_data', 'hrrr_data', 'nam12k_data']        
data = zeros((len(links),798,185))

         
for c in range(len(links)):
    x = 0
    q = 0
    v = 0
    i = 0     
    with open(links[c], "rt") as f:
        for line in f:
            commas = line.count(',') + 1
            year = line.split(',')[0]
            month = line.split(',')[1]
            day = line.split(',')[2]
            date = year + month + day
            y = 0
      

            if i == 0:     
                for t in range(3,commas):
                    station_id = line.split(',')[t]
                    data[c,x,0] = station_id
                    x = x + 1
                    
            if i == 1:     
                for t in range(3,commas):
                    lat = line.split(',')[t]
                    data[c,q,1] = lat
                    q = q + 1
            
            if i == 2:     
                for t in range(3,commas):
                    lon = line.split(',')[t]
                    data[c,v,2] = lon
                    v = v + 1

            if i != 0 and i != 1 and i != 2:
                for t in range(3,commas):   
                    precip = line.split(',')[t]
                    precip = float(precip)
                    data[c,y,i] = precip

                    y = y + 1
            
            i = i + 1

data[np.isnan(data)] = 9999



inhouse_data = data[0,:,:]
ncar_data = data[1,:,:]
gfs_data = data[2,:,:]
hrrr_data = data[3,:,:]
nam_data = data[4,:,:]
sref_arw_data = data[5,:,:]
sref_nmb_data = data[6,:,:]




regions = np.array([[37,40, -122,-118,0,0,0,0],###Sierra Nevada
                    [40,50, -125,-120, 42.97, -121.69,0,0], ##Far NW minus bottom right(>42.97, <-121.69)
                    [35.5,44, -108.7,-104,0,0,0,0], ## CO Rockies
                    [37,44.5, -114,-109.07, 39.32, -109, 43.6, -111.38], ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                    [44,50, -117.2,-109, 45.28,-115.22,44.49, -110.84], ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                    [43,45.5, -116.5,-113.5,44.46,-114.5,0,0]]) ### SW ID minus top right (< 44.46, <-114.5)




############ Determine percentiles for entire interior and pacific
inhouse_pac = []
ncar_pac = []
gfs_pac = []
hrrr_pac = []
nam_pac = []
sref_arw_pac = []
sref_nmb_pac = []


inhouse_int = []
ncar_int = []
gfs_int = []
hrrr_int = []
nam_int = []
sref_arw_int = []
sref_nmb_int = []

for w in range(0,2):
    for x in range(len(ncar_data[:,0])):
        for y in range(len(inhouse_data[:,0])):
                                ################### PACIFIC ###################            
            if w == 0:
                    if ((regions[0,0] <= ncar_data[x,1] <= regions[0,1] and regions[0,2] <= ncar_data[x,2] <= regions[0,3]) or ###Sierra Nevada
                            
                        (regions[1,0] <= ncar_data[x,1] <= regions[1,1] and regions[1,2] <= ncar_data[x,2] <= regions[1,3]) and  ##Far NW minus bottom right(>42.97, <-121.69)
                        (ncar_data[x,1] >= regions[1,4] or ncar_data[x,2] <= regions[1,5])):
                        if ncar_data[x,0] == inhouse_data[y,0]:
                            
                            inhouse_pac = np.append(inhouse_pac, inhouse_data[y,3:185])
                            ncar_pac = np.append(ncar_pac, ncar_data[x,3:185])
                            gfs_pac = np.append(gfs_pac, gfs_data[x,3:185])
                            hrrr_pac = np.append(hrrr_pac, hrrr_data[x,3:185])
                            nam_pac = np.append(nam_pac, nam_data[x,3:185])
                            sref_arw_pac = np.append(sref_arw_pac, sref_arw_data[x,3:185])
                            sref_nmb_pac = np.append(sref_nmb_pac, sref_nmb_data[x,3:185])
                            
                            
                            
                            
                                                        ################  INTERMOUNTAIN #################                                        
            if w == 1:
                    if ((regions[2,0] <= ncar_data[x,1] <= regions[2,1] and regions[2,2] <= ncar_data[x,2] <= regions[2,3]) or ## CO Rockies
    
                        (regions[3,0] <= ncar_data[x,1] <= regions[3,1] and regions[3,2] <= ncar_data[x,2] <= regions[3,3]) and  ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                        (ncar_data[x,1] >= regions[3,4] or ncar_data[x,2] <= regions[3,5]) and 
                        (ncar_data[x,1] <= regions[3,6] or ncar_data[x,2] >= regions[3,7]) or
                        
                        (regions[4,0] <= ncar_data[x,1] <= regions[4,1] and regions[4,2] <= ncar_data[x,2] <= regions[4,3]) and  ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                        (ncar_data[x,1] >= regions[4,4] or ncar_data[x,2] >= regions[4,5]) and 
                        (ncar_data[x,1] >= regions[4,6] or ncar_data[x,2] <= regions[4,7]) or
                        
                        (regions[5,0] <= ncar_data[x,1] <= regions[5,1] and regions[5,2] <= ncar_data[x,2] <= regions[5,3]) and  ### SW ID minus top right (< 44.46, <-114.5)
                        (ncar_data[x,1] <= regions[5,4] or ncar_data[x,2] <= regions[5,5])):  
                        if ncar_data[x,0] == inhouse_data[y,0]:
                            
                            inhouse_int = np.append(inhouse_int, inhouse_data[y,3:185])
                            ncar_int = np.append(ncar_int, ncar_data[x,3:185])
                            gfs_int = np.append(gfs_int, gfs_data[x,3:185])
                            hrrr_int = np.append(hrrr_int, hrrr_data[x,3:185])
                            nam_int = np.append(nam_int, nam_data[x,3:185])
                            sref_arw_int = np.append(sref_arw_int, sref_arw_data[x,3:185])
                            sref_nmb_int = np.append(sref_nmb_int, sref_nmb_data[x,3:185])
                            
                            
#### Determine percentiles
inhouse_pac2 = inhouse_pac

inhouse_pac = np.delete(inhouse_pac, np.where(inhouse_pac > 1000))
ncar_pac = np.delete(ncar_pac, np.where(inhouse_pac2 > 1000))
gfs_pac = np.delete(gfs_pac, np.where(inhouse_pac2 > 1000))
hrrr_pac = np.delete(hrrr_pac, np.where(inhouse_pac2 > 1000))
nam_pac = np.delete(nam_pac, np.where(inhouse_pac2 > 1000))
sref_arw_pac = np.delete(sref_arw_pac, np.where(inhouse_pac2 > 1000))
sref_nmb_pac = np.delete(sref_nmb_pac, np.where(inhouse_pac2 > 1000))

## NAm-3km is only model with missing days
inhouse_pac = np.delete(inhouse_pac, np.where(nam_pac > 1000))
ncar_pac = np.delete(ncar_pac, np.where(nam_pac > 1000))
gfs_pac = np.delete(gfs_pac, np.where(nam_pac > 1000))
hrrr_pac = np.delete(hrrr_pac, np.where(nam_pac > 1000))
sref_arw_pac = np.delete(sref_arw_pac, np.where(nam_pac > 1000))
sref_nmb_pac = np.delete(sref_nmb_pac, np.where(nam_pac > 1000))
nam_pac = np.delete(nam_pac, np.where(nam_pac > 1000))


#### Determine percentiles
inhouse_int2 = inhouse_int

inhouse_int = np.delete(inhouse_int, np.where(inhouse_int > 1000))
ncar_int = np.delete(ncar_int, np.where(inhouse_int2 > 1000))
gfs_int = np.delete(gfs_int, np.where(inhouse_int2 > 1000))
hrrr_int = np.delete(hrrr_int, np.where(inhouse_int2 > 1000))
nam_int = np.delete(nam_int, np.where(inhouse_int2 > 1000))
sref_arw_int = np.delete(sref_arw_int, np.where(inhouse_int2 > 1000))
sref_nmb_int = np.delete(sref_nmb_int, np.where(inhouse_int2 > 1000))

## NAm-3km is only model with missing days
inhouse_int = np.delete(inhouse_int, np.where(nam_int > 1000))
ncar_int = np.delete(ncar_int, np.where(nam_int > 1000))
gfs_int = np.delete(gfs_int, np.where(nam_int > 1000))
hrrr_int = np.delete(hrrr_int, np.where(nam_int > 1000))
sref_arw_int = np.delete(sref_arw_int, np.where(nam_int > 1000))
sref_nmb_int = np.delete(sref_nmb_int, np.where(nam_int > 1000))
nam_int = np.delete(nam_int, np.where(nam_int > 1000))

#Calculate percentiles
percent_pac = zeros((19,7))
percent_int = zeros((19,7))
for p in range(5,96,5):
    print(p)
    i = p/5-1
    percent_pac[i,0] = np.percentile(inhouse_pac,p)
    percent_pac[i,1] = np.percentile(ncar_pac,p)
    percent_pac[i,2] = np.percentile(gfs_pac,p)
    percent_pac[i,3] = np.percentile(hrrr_pac,p)
    percent_pac[i,4] = np.percentile(nam_pac,p)
    percent_pac[i,5] = np.percentile(sref_arw_pac,p)
    percent_pac[i,6] = np.percentile(sref_nmb_pac,p)
    
    percent_int[i,0] = np.percentile(inhouse_int,p)
    percent_int[i,1] = np.percentile(ncar_int,p)
    percent_int[i,2] = np.percentile(gfs_int,p)
    percent_int[i,3] = np.percentile(hrrr_int,p)
    percent_int[i,4] = np.percentile(nam_int,p)
    percent_int[i,5] = np.percentile(sref_arw_int,p)
    percent_int[i,6] = np.percentile(sref_nmb_int,p)
    
#%%    
#Plot for Pac and Int



#x = np.arange(5.08,50.800001,2.54)
x = np.arange(50,95.1,5)
linecolor = ['k','blue', 'green', 'red', 'c', 'gold', 'magenta']
fig1=plt.figure(num=None, figsize=(14,8), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.4, bottom = 0.2)


ax1 = fig1.add_subplot(121)
plt.gca().set_color_cycle(linecolor)
ax1.plot(x,percent_pac[9:,:],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
black = mlines.Line2D([], [], color='k',
                           label='SNOTEL', linewidth = 2,marker = "o", markeredgecolor = 'none')
blue = mlines.Line2D([], [], color='blue',
                           label='NCAR ENS CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
green = mlines.Line2D([], [], color='green',
                           label='GFS', linewidth = 2,marker = "o", markeredgecolor = 'none')
red = mlines.Line2D([], [], color='red',
                           label='HRRR', linewidth = 2,marker = "o", markeredgecolor = 'none')
cyan = mlines.Line2D([], [], color='c',
                           label='NAM-3km', linewidth = 2,marker = "o", markeredgecolor = 'none')
gold = mlines.Line2D([], [], color='gold',
                           label='SREF ARW CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
magenta = mlines.Line2D([], [], color='magenta',
                           label='SREF NMMB CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.ylabel('Absolute Threshold (mm)', fontsize = 19)
plt.xlabel('Percentile Threshold', fontsize = 19)
props = dict(boxstyle='square', facecolor='white', alpha=1)
fig1.text(0.7, 0.1, '(a) Pacific Ranges', fontsize = 19, bbox = props)
plt.xlim([50,95.1])
plt.ylim([0,55])
plt.xticks(np.arange(5,96,5))
ax1.set_xticklabels(np.arange(5,96,5), fontsize = 14)
ax1.tick_params(axis='y', labelsize=12)




ax1 = fig1.add_subplot(122, sharex = ax1)
plt.gca().set_color_cycle(linecolor)
ax1.plot(x,percent_int[9:,:],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
props = dict(boxstyle='square', facecolor='white', alpha=1)
fig1.text(0.7,.8, '(b) Interior Ranges', fontsize = 19, bbox = props)
plt.xlabel('Percentile Threshold', fontsize = 19)
plt.ylim([0,25])
plt.xticks(np.arange(5,96,5))
ax1.set_xticklabels(np.arange(5,96,5), fontsize = 14)
ax1.tick_params(axis='y', labelsize=14)
plt.xlim([50,95])

plt.legend(handles=[ black, blue,  red, cyan,green, gold, magenta], loc='upper left', bbox_to_anchor=(-1.2, 0.9), 
           ncol=1, fontsize = 13)
plt.savefig("../../../public_html/SNOTEL_forecast_thresholds.pdf")
















    
