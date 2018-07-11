
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


region = west



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






###############################################################################
##### Calculate ETS_ncar using percentiles with good data (<1000) for both ####
###############################################################################
i = 0
u = 0
end = 19   
hit = zeros((end,len(data[:,0,0])-1)) #### There arrays now go in the order col 1-4:region 1, 5-8:region2,etc...
miss = zeros((end,len(data[:,0,0])-1))
falarm = zeros((end,len(data[:,0,0])-1))
correct_non = zeros((end,len(data[:,0,0])-1))
#percentile = zeros((end, 800))
precip = zeros((2000,185))
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
##### Calculate gfs using percentiles with good data (<1000) for both ####
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
##### Calculate ETS_nam using percentiles with good data (<1000) for both ####
###############################################################################

end = 19
u = u + 1


p_array = []

for a in range(1,end+1):
        percent = a * 5
        s = a-1
        for x in range(len(nam_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if nam_data[x,0] == inhouse_data[y,0]:
                    
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and  inhouse_data[y,z] < 1000:
                            
                                if nam_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    hit[s,u] = hit[s,u] + 1
                            
                                if nam_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    miss[s,u] = miss[s,u] + 1
                            
                                if nam_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    falarm[s,u] = falarm[s,u] + 1
                            
                                if nam_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    correct_non[s,u] = correct_non[s,u] + 1
                                    
                                    
###############################################################################
##### Calculate sref_arw using percentiles with good data (<1000) for both ####
###############################################################################

end = 19
u = u + 1


p_array = []

for a in range(1,end+1):
        percent = a * 5
        s = a-1
        for x in range(len(sref_arw_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if sref_arw_data[x,0] == inhouse_data[y,0]:
                    
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and  inhouse_data[y,z] < 1000:
                            
                                if sref_arw_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    hit[s,u] = hit[s,u] + 1
                            
                                if sref_arw_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    miss[s,u] = miss[s,u] + 1
                            
                                if sref_arw_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    falarm[s,u] = falarm[s,u] + 1
                            
                                if sref_arw_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    correct_non[s,u] = correct_non[s,u] + 1
                                    


###############################################################################
##### Calculate sref_nmbusing percentiles with good data (<1000) for both ####
###############################################################################

end = 19
u = u + 1


p_array = []

for a in range(1,end+1):
        percent = a * 5
        s = a-1
        for x in range(len(sref_nmb_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if sref_nmb_data[x,0] == inhouse_data[y,0]:
                    
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and  inhouse_data[y,z] < 1000:
                            
                                if sref_nmb_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    hit[s,u] = hit[s,u] + 1
                            
                                if sref_nmb_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    miss[s,u] = miss[s,u] + 1
                            
                                if sref_nmb_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    falarm[s,u] = falarm[s,u] + 1
                            
                                if sref_nmb_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    correct_non[s,u] = correct_non[s,u] + 1

# Calcualte Bias, Hit Rate, False Alarm Rate, ETS
                                
                       
ets = zeros((end,len(data[:,0,0])-1))
ets_a = zeros((end,len(data[:,0,0])-1))
hitrate = zeros((end,len(data[:,0,0])-1))
bias = zeros((end,len(data[:,0,0])-1))
faratio = zeros((end,len(data[:,0,0])-1))
farate = zeros((end,len(data[:,0,0])-1))
                             
for a in range(1,end+1):
    s=a-1
    for i in range(6):                                
        a_ref = 0
        a_ref = ((hit[s,i] + miss[s,i])*(hit[s,i] + falarm[s,i]))/(hit[s,i]+falarm[s,i]+miss[s,i]+correct_non[s,i])
    
        ets[s,i] = (hit[s,i] - a_ref)/(hit[s,i] - a_ref + falarm[s,i] + miss[s,i])
        hitrate[s,i] = (hit[s,i])/(hit[s,i] + miss[s,i])
        bias[s,i] = (hit[s,i] + falarm[s,i])/(hit[s,i] + miss[s,i])
        faratio[s,i] = (falarm[s,i])/(hit[s,i] + falarm[s,i])
        farate[s,i] = (falarm[s,i])/(correct_non[s,i] + falarm[s,i])
        
        #######  Bias Adjusted ETS (Mesingger and Brill 2004)######
        O = hit[s,i] + miss[s,i]
        F = hit[s,i] + falarm[s,i]
        N = hit[s,i] + falarm[s,i] + miss[s,i] + correct_non[s,i]
        H = hit[s,i]
        H_a = O*(1-((O-H)/O)**(O/F))
        
        
        ets_a[s,i] = (H_a-F*F/N)/(F+O-H_a-F*F/N)
        
        
#%%    

###############################################################################
################################## PLOTS ######################################
###############################################################################

#x = np.arange(5.08,50.800001,2.54)
x = np.arange(5,95.1,5)
linecolor = ['blue', 'green', 'red', 'c', 'gold', 'magenta']
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
                           label='SREF NMB CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')

plt.title('Bias Score', fontsize = 22)
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
ax3.plot(x,faratio[:,:],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.title('False Alarm Ratio', fontsize = 22)
plt.xlabel('24-hour Precipitation Event (Percentiles)', fontsize = 18)
plt.ylabel('Score', fontsize = 18)
plt.xlim([5,95.1])
plt.xticks(np.arange(5,96,10))
ax3.set_xticklabels(np.arange(5,96,10), fontsize = 16)
ax3.tick_params(axis='y', labelsize=16)



ax4 = fig1.add_subplot(224, sharex = ax1)
plt.gca().set_color_cycle(linecolor)
ax4.plot(x,farate[:,:],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.title('False Alarm Rate', fontsize = 22)
plt.xlabel('Precipitation Event (Percentile)',fontsize = 18)
plt.xlim([5,95.1])
plt.xticks(np.arange(5,96,10))
ax4.set_xticklabels(np.arange(5,96,10), fontsize = 16)
ax4.tick_params(axis='y', labelsize=16)
plt.legend(handles=[ blue, green, red, cyan, gold, magenta], loc='upper center', bbox_to_anchor=(-0.10, -0.17), 
           ncol=3, fontsize = 16)
plt.savefig("../../../public_html/categorical_scores_percentilethresholds_interp_2016_17.pdf")



###############################################################################
################################## ETS ########################################
###############################################################################

linecolor = ['blue', 'green', 'red', 'c', 'gold', 'magenta']
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
                           label='SREF NMB CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')

plt.legend(handles=[ blue, green, red, cyan, gold, magenta], loc = "lower left")
plt.title('Equitable Threat Score', fontsize = 22)
plt.ylabel('Score', fontsize = 18)
plt.xlabel('Precipitation Event (Percentile)',fontsize = 18)
plt.savefig("../../../public_html/ets_percentilethresholds_interp_2016_17.pdf")
#%%

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






























