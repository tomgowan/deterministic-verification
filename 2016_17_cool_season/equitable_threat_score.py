
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


region = sys.argv[1]



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
    
    
    



inhouse_data = zeros((649,186))
ncar_data = zeros((798,186))
nam4k_data = zeros((798,186))
hrrr_data = zeros((798,186))




###############################################################################
############ Read in  12Z to 12Z data   #####################
###############################################################################
             
x = 0
q = 0
v = 0
i = 0   
     
links = ["/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/snotel_precip_2015_2016_qc.csv", 
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/ncarens_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/nam4km_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/hrrrV1_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/nam12km_precip_12Zto12Z_interp.txt"]

#data = ['inhouse_data', 'ncar_data', 'nam4k_data', 'hrrr_data', 'nam12k_data']        
data = zeros((5,798,186))

         
for c in range(5):
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
nam4k_data = data[2,:,:] 
hrrr_data = data[3,:,:]
nam12k_data = data[4,:,:]



###############################################################################
##### Calculate ETS_ncar using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
w = -1
hit = zeros((end,3))
miss = zeros((end,3))
falarm = zeros((end,3))
correct_non = zeros((end,3))
#percentile = zeros((end, 800))

p_array = []

for a in range(1,end+1):
    percent = a * 5
    for x in range(len(ncar_data[:,0])):
        for y in range(len(inhouse_data[:,0])):
                if ncar_data[x,0] == inhouse_data[y,0]:
                    
                    #p_array is all precip days for one station.  Created to determine percentiles for each station
                    p_array = inhouse_data[y,3:185]
                    p_array = np.delete(p_array, np.where(p_array < 2.54))
                    p_array = np.delete(p_array, np.where(p_array > 1000))
   
                    percentile = np.percentile(p_array,percent)


                    for z in range(3,185):
                        
                        # Excludes bad data 
                        if all(data[1:,x,z] < 1000) and  inhouse_data[y,z] < 1000:
                            
                            if ncar_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                hit[a-1,0] = hit[a-1,0] + 1
                            
                            if ncar_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                miss[a-1,0] = miss[a-1,0] + 1
                            
                            if ncar_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                falarm[a-1,0] = falarm[a-1,0] + 1
                            
                            if ncar_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                correct_non[a-1,0] = correct_non[a-1,0] + 1
                                


    
        
                       

###############################################################################
##### Calculate ETS_nam4k using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
w = -1


p_array = []

for a in range(1,end+1):
    percent = a * 5
    for x in range(len(nam4k_data[:,0])):
        for y in range(len(inhouse_data[:,0])):
                if nam4k_data[x,0] == inhouse_data[y,0]:
                    
                    #p_array is all precip days for one station.  Created to determine percentiles for each station
                    p_array = inhouse_data[y,3:185]
                    p_array = np.delete(p_array, np.where(p_array < 2.54))
                    p_array = np.delete(p_array, np.where(p_array > 1000))
   
                    percentile = np.percentile(p_array,percent)


                    for z in range(3,185):
                        
                        # Excludes bad data 
                        if all(data[1:,x,z] < 1000) and  inhouse_data[y,z] < 1000:
                            
                            if nam4k_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                hit[a-1,1] = hit[a-1,1] + 1
                            
                            if nam4k_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                miss[a-1,1] = miss[a-1,1] + 1
                            
                            if nam4k_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                falarm[a-1,1] = falarm[a-1,1] + 1
                            
                            if nam4k_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                correct_non[a-1,1] = correct_non[a-1,1] + 1
                                

    
        
                       


###############################################################################
##### Calculate ETS_hrrr using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
w = -1


p_array = []

for a in range(1,end+1):
    percent = a * 5
    for x in range(len(hrrr_data[:,0])):
        for y in range(len(inhouse_data[:,0])):
                if hrrr_data[x,0] == inhouse_data[y,0]:
                    
                    #p_array is all precip days for one station.  Created to determine percentiles for each station
                    p_array = inhouse_data[y,3:185]
                    p_array = np.delete(p_array, np.where(p_array < 2.54))
                    p_array = np.delete(p_array, np.where(p_array > 1000))
   
                    percentile = np.percentile(p_array,percent)


                    for z in range(3,185):
                        
                        # Excludes bad data 
                        if all(data[1:,x,z] < 1000) and  inhouse_data[y,z] < 1000:
                            
                            if hrrr_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                hit[a-1,2] = hit[a-1,2] + 1
                            
                            if hrrr_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                miss[a-1,2] = miss[a-1,2] + 1
                            
                            if hrrr_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                falarm[a-1,2] = falarm[a-1,2] + 1
                            
                            if hrrr_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                correct_non[a-1,2] = correct_non[a-1,2] + 1
                                


# Calcualte Bias, Hit Rate, False Alarm Rate, ETS
                                
                        
ets = zeros((end,3))
hitrate = zeros((end,3))
bias = zeros((end,3))
far = zeros((end,3))
pofd = zeros((end,3))
                              
for a in range(1,end+1):
    for i in range(3):                                
        a_ref = 0
        a_ref = ((hit[a-1,i] + miss[a-1,i])*(hit[a-1,i] + falarm[a-1,i]))/(hit[a-1,i]+falarm[a-1,i]+miss[a-1,i]+correct_non[a-1,i])
    
        ets[a-1,i] = (hit[a-1,i] - a_ref)/(hit[a-1,i] - a_ref + falarm[a-1,i] + miss[a-1,i])
        hitrate[a-1,i] = (hit[a-1,i])/(hit[a-1,i] + miss[a-1,i])
        bias[a-1,i] = (hit[a-1,i] + falarm[a-1,i])/(hit[a-1,i] + miss[a-1,i])
        far[a-1,i] = (falarm[a-1,i])/(hit[a-1,i] + falarm[a-1,i])
        pofd[a-1,i] = (falarm[a-1,i])/(correct_non[a-1,i] + falarm[a-1,i])
        
  


###############################################################################
################################## PLOTS ######################################
###############################################################################

x = np.arange(5,95.0001,5)

fig1=plt.figure(num=None, figsize=(12,12), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.2, bottom = 0.1)

ax1 = fig1.add_subplot(221)
ax1.plot(x,bias[:,:])
plt.xlim([5,95.1])
plt.xticks(np.arange(5,95.1,10))
plt.grid(True)
blue_line = mlines.Line2D([], [], color='blue',
                           label='NCARens Control')
green_line = mlines.Line2D([], [], color='green',
                           label='NAM-4km')
red_line = mlines.Line2D([], [], color='red',
                           label='HRRR')
plt.legend(handles=[ blue_line, green_line, red_line], loc = "upper left")
plt.title('Bias', fontsize = 18)
plt.ylabel('Score', fontsize = 12)




ax2 = fig1.add_subplot(222, sharex = ax1)
ax2.plot(x,hitrate[:,:])
plt.grid(True)
plt.title('Hit Rate', fontsize = 18)




ax2 = fig1.add_subplot(223, sharex = ax1)
ax2.plot(x,far[:,:])
plt.grid(True)
plt.title('False Alarm Rate', fontsize = 18)
plt.xlabel('24-hour Precipitation Event (Percentiles)', fontsize = 12)
plt.ylabel('Score', fontsize = 12)




ax4 = fig1.add_subplot(224, sharex = ax1)
ax4.plot(x,pofd[:,:])
plt.grid(True)
plt.title('Probability of Fasle Detection', fontsize = 18)
plt.xlabel('24-hour Precipitation Event (Percentiles)',fontsize = 12)
plt.savefig("../plots/categorical_scores_interp.pdf")



###############################################################################
################################## ETS ########################################
###############################################################################




fig1=plt.figure(num=None, figsize=(8,8), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.2, bottom = 0.1)

ax1 = fig1.add_subplot(111)
ax1.plot(x,ets[:,:])
plt.xlim([5,95.1])
plt.xticks(np.arange(5,95.1,10))
plt.grid(True)
blue_line = mlines.Line2D([], [], color='blue',
                           label='NCARens Control')
green_line = mlines.Line2D([], [], color='green',
                           label='NAM-4km')
red_line = mlines.Line2D([], [], color='red',
                           label='HRRR')
plt.legend(handles=[ blue_line, green_line, red_line], loc = "upper right")
plt.title('Equitable Threat Score', fontsize = 18)
plt.ylabel('Score', fontsize = 12)
plt.xlabel('24-hour Precipitation Event (Percentiles)',fontsize = 12)
plt.savefig("../plots/ets_interp.pdf")











































