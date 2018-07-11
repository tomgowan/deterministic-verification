
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
    
    
   
'''


inhouse_data = zeros((798,186))
ncar_data = zeros((798,186))
nam4k_data = zeros((798,186))
nam12k_data = zeros((798,186))
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
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/nam12km_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/gfs_precip_12Zto12Z_interp.txt"]

#data = ['inhouse_data', 'ncar_data', 'nam4k_data', 'hrrr_data', 'nam12k_data']        
data = zeros((len(links),798,186))

         
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
nam4k_data = data[2,:,:] 
hrrr_data = data[3,:,:]
nam12k_data = data[4,:,:]
gfs_data = data[5,:,:]



###############################################################################
##### Dvide into regionms#####################################################
###############################################################################

regions = np.array([[41.5,49.2, -123.0,-120.5],
                    [37.0,41.0, -121.0,-118.0], 
                    [43.7,46.2, -120.0,-116.8], 
                    [43.0,49.3, -116.8,-112.2], 
                    [41.8,47.0, -112.5,-105.5],
                    [37.2,41.8, -113.9,-109.2],
                    [35.6,41.5, -108.7,-104.5],
                    [32.5,35.5, -113.0,-107.0]])





###############################################################################
##### Calculate ETS_ncar using percentiles with good data (<1000) for both ####
###############################################################################
i = 0
u = 0
end = 19   
hit = zeros((end,5)) #### There arrays now go in the order col 1-4:region 1, 5-8:region2,etc...
miss = zeros((end,5))
falarm = zeros((end,5))
correct_non = zeros((end,5))
#percentile = zeros((end, 800))
precip = zeros((2000,186))
p_array = []


for x in range(len(ncar_data[:,0])):
        for y in range(len(inhouse_data[:,0])):
                if ncar_data[x,0] == inhouse_data[y,0]:
                    print ncar_data[x,0]
                    print inhouse_data[y,0]
                    
                    ### Just to investigate data
                    precip[i,:] = ncar_data[x,:]
                    precip[i+1,:] = inhouse_data[y,:]
                    i = i +2


u = 0               
for a in range(1,end+1):
        percent= a * 5
        s = a-1
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
                                    hit[s,u] = hit[s,u] + 1
                            
                                if ncar_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    miss[s,u] = miss[s,u] + 1
                            
                                if ncar_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    falarm[s,u] = falarm[s,u] + 1
                            
                                if ncar_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    correct_non[s,u] = correct_non[s,u] + 1
                                


    
        
                       

###############################################################################
##### Calculate ETS_nam4k using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
u = u + 1

p_array = []

for a in range(1,end+1):
        percent = a * 5
        s = a-1
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
                                    hit[s,u] = hit[s,u] + 1
                            
                                if nam4k_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    miss[s,u] = miss[s,u] + 1
                            
                                if nam4k_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    falarm[s,u] = falarm[s,u] + 1
                            
                                if nam4k_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    correct_non[s,u] = correct_non[s,u] + 1
                                

    
        
                       


###############################################################################
##### Calculate ETS_hrrr using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
u = u + 1

p_array = []

for a in range(1,end+1):
        percent = a * 5
        s = a-1
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
                                    hit[s,u] = hit[s,u] + 1
                            
                                if hrrr_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    miss[s,u] = miss[s,u] + 1
                            
                                if hrrr_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    falarm[s,u] = falarm[s,u] + 1
                            
                                if hrrr_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    correct_non[s,u] = correct_non[s,u] + 1
                                







###############################################################################
##### Calculate ETS_nam12k using percentiles with good data (<1000) for both ####
###############################################################################

end = 19
u = u + 1


p_array = []

for a in range(1,end+1):
        percent = a * 5
        s = a-1
        for x in range(len(nam12k_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if nam12k_data[x,0] == inhouse_data[y,0]:
                    
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and  inhouse_data[y,z] < 1000:
                            
                                if nam12k_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    hit[s,u] = hit[s,u] + 1
                            
                                if nam12k_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    miss[s,u] = miss[s,u] + 1
                            
                                if nam12k_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    falarm[s,u] = falarm[s,u] + 1
                            
                                if nam12k_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    correct_non[s,u] = correct_non[s,u] + 1
                                    
                                    
###############################################################################
##### Calculate ETS_gfs using percentiles with good data (<1000) for both ####
###############################################################################

end = 19
u = u + 1


p_array = []

for a in range(1,end+1):
        percent = a * 5
        s = a-1
        for x in range(len(gfs_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if gfs_data[x,0] == inhouse_data[y,0]:
                    
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and  inhouse_data[y,z] < 1000:
                            
                                if gfs_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    hit[s,u] = hit[s,u] + 1
                            
                                if gfs_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    miss[s,u] = miss[s,u] + 1
                            
                                if gfs_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    falarm[s,u] = falarm[s,u] + 1
                            
                                if gfs_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    correct_non[s,u] = correct_non[s,u] + 1

# Calcualte Bias, Hit Rate, False Alarm Rate, ETS
                                
                       
ets = zeros((end,5))
ets_a = zeros((end,5))
hitrate = zeros((end,5))
bias = zeros((end,5))
far = zeros((end,5))
pofd = zeros((end,5))
                             
for a in range(1,end+1):
    s=a-1
    for i in range(5):                                
        a_ref = 0
        a_ref = ((hit[s,i] + miss[s,i])*(hit[s,i] + falarm[s,i]))/(hit[s,i]+falarm[s,i]+miss[s,i]+correct_non[s,i])
    
        ets[s,i] = (hit[s,i] - a_ref)/(hit[s,i] - a_ref + falarm[s,i] + miss[s,i])
        hitrate[s,i] = (hit[s,i])/(hit[s,i] + miss[s,i])
        bias[s,i] = (hit[s,i] + falarm[s,i])/(hit[s,i] + miss[s,i])
        far[s,i] = (falarm[s,i])/(hit[s,i] + falarm[s,i])
        pofd[s,i] = (falarm[s,i])/(correct_non[s,i] + falarm[s,i])
        
        #######  Bias Adjusted ETS (Mesingger and Brill 2004)######
        O = hit[s,i] + miss[s,i]
        F = hit[s,i] + falarm[s,i]
        N = hit[s,i] + falarm[s,i] + miss[s,i] + correct_non[s,i]
        H = hit[s,i]
        H_a = O*(1-((O-H)/O)**(O/F))
        
        
        ets_a[s,i] = (H_a-F*F/N)/(F+O-H_a-F*F/N)
        
        
    
'''
###############################################################################
################################## PLOTS ######################################
###############################################################################

#x = np.arange(5.08,50.800001,2.54)
x = np.arange(5,95.1,5)
linecolor = ['blue', 'green', 'red', 'c', 'gold']
fig1=plt.figure(num=None, figsize=(14,12), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.2, bottom = 0.2)


ax1 = fig1.add_subplot(221)

plt.gca().set_color_cycle(linecolor)

ax1.plot(x,bias[:,:],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.xlim([5,95.1])
plt.xticks(np.arange(5,96,10))
ax1.set_xticklabels(np.arange(5,96,10), fontsize = 16)

ax1.tick_params(axis='y', labelsize=16)

plt.grid(True)
blue_line = mlines.Line2D([],[] , color='blue',
                           label='NCAR Ens Control', markeredgecolor = 'none', linewidth = 2,marker = "o")
green_line = mlines.Line2D([], [], color='green',
                           label='NAM-4km', markeredgecolor = 'none', linewidth = 2,marker = "o")
red_line = mlines.Line2D([], [], color='red',
                           label='HRRR', markeredgecolor = 'none', linewidth = 2,marker = "o")
cyan_line = mlines.Line2D([], [], color='c',
                           label='NAM-12km', markeredgecolor = 'none', linewidth = 2,marker = "o")
gold_line = mlines.Line2D([], [], color='gold',
                           label='GFS', markeredgecolor = 'none', linewidth = 2,marker = "o")

plt.title('Bias', fontsize = 22)
plt.ylabel('Score', fontsize = 18)




ax2 = fig1.add_subplot(222, sharex = ax1)
plt.gca().set_color_cycle(linecolor)
ax2.plot(x,hitrate[:,:],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.title('Hit Rate', fontsize = 22)
plt.xlim([5,95.1])
plt.xticks(np.arange(5,96,10))
ax2.set_xticklabels(np.arange(5,96,10), fontsize = 16)
ax2.tick_params(axis='y', labelsize=16)



ax3 = fig1.add_subplot(223, sharex = ax1)
plt.gca().set_color_cycle(linecolor)
ax3.plot(x,far[:,:],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.title('False Alarm Rate', fontsize = 22)
plt.xlabel('24-hour Precipitation Event (Percentiles)', fontsize = 18)
plt.ylabel('Score', fontsize = 18)
plt.xlim([5,95.1])
plt.xticks(np.arange(5,96,10))
ax3.set_xticklabels(np.arange(5,96,10), fontsize = 16)
ax3.tick_params(axis='y', labelsize=16)



ax4 = fig1.add_subplot(224, sharex = ax1)
plt.gca().set_color_cycle(linecolor)
ax4.plot(x,pofd[:,:],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.title('Probability of False Detection', fontsize = 22)
plt.xlabel('24-hour Precipitation Event (Percentile)',fontsize = 18)
plt.xlim([5,95.1])
plt.xticks(np.arange(5,96,10))
ax4.set_xticklabels(np.arange(5,96,10), fontsize = 16)
ax4.tick_params(axis='y', labelsize=16)
plt.legend(handles=[ blue_line, green_line, red_line, cyan_line, gold_line], loc='upper center', bbox_to_anchor=(-0.10, -0.17), 
           fancybox=True, shadow=True, ncol=5, fontsize = 16)
plt.savefig("../plots/categorical_scores_percentilethresholds_interp.pdf")



###############################################################################
################################## ETS ########################################
###############################################################################

linecolor = ['blue', 'green', 'red', 'c', 'gold']
t = 0

fig1=plt.figure(num=None, figsize=(8,8), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.2, bottom = 0.1)

ax1 = fig1.add_subplot(111)

plt.gca().set_color_cycle(linecolor)
ax1.plot(x,ets[:,:], linewidth = 2, marker = "o", markeredgecolor = 'none')

plt.xlim([5,95.1])
plt.xticks(np.arange(5,96,10))
ax1.set_xticklabels(np.arange(5,96,10), fontsize = 16)
ax1.tick_params(axis='y', labelsize=16)

plt.grid(True)

blue_line = mlines.Line2D([],[] , color='blue',
                           label='NCAR Ens Control',  linewidth = 2,marker = "o", markeredgecolor = 'none')
green_line = mlines.Line2D([], [], color='green',
                           label='NAM-4km',  linewidth = 2,marker = "o", markeredgecolor = 'none')
red_line = mlines.Line2D([], [], color='red',
                           label='HRRR',  linewidth = 2,marker = "o", markeredgecolor = 'none')
cyan_line = mlines.Line2D([], [], color='c',
                           label='NAM-12km', linewidth = 2,marker = "o", markeredgecolor = 'none')
gold_line = mlines.Line2D([], [], color='gold',
                           label='GFS', markeredgecolor = 'none', linewidth = 2,marker = "o")
plt.legend(handles=[ blue_line, green_line, red_line, cyan_line, gold_line], loc = "lower left")
plt.title('Equitable Threat Score', fontsize = 22)
plt.ylabel('Score', fontsize = 18)
plt.xlabel('24-hour Precipitation Event (Percentile)',fontsize = 18)
plt.savefig("../plots/ets_percentilethresholds_interp.pdf")


'''

###############################################################################
################################## ETS_adjusted################################
###############################################################################

linecolor = ['blue', 'green', 'red', 'c']
t = 0

fig1=plt.figure(num=None, figsize=(8,8), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.2, bottom = 0.1)

ax1 = fig1.add_subplot(111)

plt.gca().set_color_cycle(linecolor)
ax1.plot(x,ets_a[:,:], linewidth = 2, marker = "o", markeredgecolor = 'none')


plt.xlim([5,95.1])
plt.ylim([0,.5])
plt.xticks(np.arange(5,95.1,5))
plt.yticks(np.arange(0,.750001,.05))
plt.grid(True)

blue_line = mlines.Line2D([],[] , color='blue',
                           label='NCAR Ens Control',  linewidth = 2,marker = "o", markeredgecolor = 'none')
green_line = mlines.Line2D([], [], color='green',
                           label='NAM-4km',  linewidth = 2,marker = "o", markeredgecolor = 'none')
red_line = mlines.Line2D([], [], color='red',
                           label='HRRR',  linewidth = 2,marker = "o", markeredgecolor = 'none')
cyan_line = mlines.Line2D([], [], color='c',
                           label='NAM-12km', linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.legend(handles=[ blue_line, green_line, red_line, cyan_line], loc = "upper right")
plt.title('Equitable Threat Score (Bias Adjusted)', fontsize = 18)
plt.ylabel('Score', fontsize = 14)
plt.xlabel('24-hour Precipitation Event (Percentile)',fontsize = 14)
plt.savefig("../plots/ets_adjusted_percentilethresholds_interp.pdf")
'''






























