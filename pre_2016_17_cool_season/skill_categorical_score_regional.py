
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


inhouse_data = zeros((649,186))
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
hit = zeros((end,40)) #### There arrays now go in the order col 1-4:region 1, 5-8:region2,etc...
miss = zeros((end,40))
falarm = zeros((end,40))
correct_non = zeros((end,40))
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

for w in range(0,8):
    print w
    
    
    u = w*5               
    for a in range(1,end+1):
        percent= a * 5
        s = a-1
        for x in range(len(ncar_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                if regions[w,0] <= inhouse_data[y,1] <= regions[w,1] and regions[w,2] <= inhouse_data[y,2] <= regions[w,3]:
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
                if regions[w,0] <= inhouse_data[y,1] <= regions[w,1] and regions[w,2] <= inhouse_data[y,2] <= regions[w,3]:
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
                if regions[w,0] <= inhouse_data[y,1] <= regions[w,1] and regions[w,2] <= inhouse_data[y,2] <= regions[w,3]:
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
                if regions[w,0] <= inhouse_data[y,1] <= regions[w,1] and regions[w,2] <= inhouse_data[y,2] <= regions[w,3]:
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
                if regions[w,0] <= inhouse_data[y,1] <= regions[w,1] and regions[w,2] <= inhouse_data[y,2] <= regions[w,3]:
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
                       
ets = zeros((end,40))
hitrate = zeros((end,40))
bias = zeros((end,40))
far = zeros((end,40))
pofd = zeros((end,40))
ets_a = zeros((end,40))
                             
for a in range(1,end+1):
    s=a-1
    for i in range(40):                                
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




###############################################################################
################################## ETS by Regional(model) #####################
###############################################################################


linecolor = ['blue', 'green', 'red', 'c','gold']
t = 0


plt.gca().set_color_cycle(linecolor)









region = ['Pacific Northwest', 'Sierra Nevada','Blue Mountains, OR','Idaho/Western MT','NW Wyoming','Utah','CO' ,'AZ/NM']                
x = np.arange(5,95.1,5)

fig1=plt.figure(num=None, figsize=(12,16), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.25, bottom = 0.1)

for i in range(1,9):
    plot = 420+i
    w = 5*i
    t = w - 5
    ax1 = fig1.add_subplot(plot)
    plt.xlim([5,95.1])
    plt.ylim([.1,0.6])
    plt.yticks(np.arange(.1,0.60001, 0.1))
    ax1.set_yticklabels(np.arange(.1,0.60001, .1), fontsize = 15)
    plt.gca().set_color_cycle(linecolor)
    ax1.plot(x,ets[:,t:w],linewidth = 2, marker = "o", markeredgecolor = 'none')
    plt.xlim([5,95.1])
    plt.xticks(np.arange(5,95.1,10))
    ax1.set_xticklabels(np.arange(5,96,10), fontsize = 15)
    plt.grid(True)
    blue_line = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='blue',
                           label='NCARens Control')
    green_line = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='green',
                           label='NAM-4km')
    red_line = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='red',
                           label='HRRR')
    cyan_line = mlines.Line2D([], [], linewidth = 2, marker = "o", markeredgecolor = 'none',color='c',
                           label='NAM-12km')
    gold_line = mlines.Line2D([], [], linewidth = 2, marker = "o", markeredgecolor = 'none',color='gold',
                           label='GFS')
    
    plt.title(region[i-1], fontsize = 22)
            
    
    if i == 1 or i == 3 or i == 5 or i == 7:
        plt.ylabel('Equitable Threat Score', fontsize = 18, labelpad = 13)

    if i == 8 or  i == 7:
        plt.xlabel('24-hour Precip. Event (Percentile)', fontsize = 18, labelpad = 13)

plt.legend(handles=[ blue_line, green_line, red_line, cyan_line, gold_line], loc='upper center', bbox_to_anchor=(-0.16, -0.24), 
           fancybox=True, shadow=True, ncol=5,fontsize = 18)
plt.savefig('../plots/ets_regionalgrouping_interp.pdf')









###############################################################################
################################## ETS by Model (regions)    ###############################
###############################################################################
linecolor = ['blue', 'green', 'red', 'c', 'y', 'darkred', 'purple', 'salmon']
model = ['NCARens Control', 'NAM-4km','HRRR', 'NAM-12km']                
reg = np.arange(0,31,4)
fig1=plt.figure(num=None, figsize=(12,12), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.23, bottom = 0.25)

for i in range(1,5):
    plot = 220+i
    
    ax1 = fig1.add_subplot(plot)
    plt.xlim([5,95.1])
    plt.xticks(np.arange(5,95.1,10))
    ax1.set_xticklabels(np.arange(5,96,10), fontsize = 15)
    plt.ylim([.2,0.6])
    plt.yticks(np.arange(.2,0.60001,0.1))
    ax1.set_yticklabels(np.arange(.2,0.60001, .1), fontsize = 15)
    
    for p in range(8):
        plt.gca().set_color_cycle(linecolor[p])

        ax1.plot(x,ets[:,reg[p]],linewidth = 2, marker = "o", markeredgecolor = 'none')

    reg = reg + 1
    

    plt.grid(True)
    
    blue = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='blue',
                           label=region[0])
    green = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='green',
                           label=region[1])
    red = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='red',
                           label=region[2])
    cyan = mlines.Line2D([], [], linewidth = 2, marker = "o", markeredgecolor = 'none',color='c',
                           label=region[3])
    yellow = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='y',
                           label=region[4])
    black = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='darkred',
                           label=region[5])
    purple = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='purple',
                           label=region[6])
    salmon = mlines.Line2D([], [], linewidth = 2, marker = "o", markeredgecolor = 'none',color='salmon',
                           label=region[7])
    
    plt.title(model[i-1], fontsize = 22)
            
    
    if i == 1 or i == 3:
        plt.ylabel('Equitable Threat Score', fontsize = 18, labelpad = 10)

    if i == 3 or  i == 4:
        plt.xlabel('24-hour Precip. Event (Percentile)', fontsize = 18, labelpad = 10)

plt.legend(handles=[ blue, green, red, cyan, yellow, black, purple, salmon], loc='upper center', bbox_to_anchor=(-0.15, -0.2), 
           fancybox=True, shadow=True, ncol=4, fontsize = 16)
plt.savefig('../plots/ets_regional_modelgrouping_interp.pdf')



###############################################################################
########### Same plots with bias corrected ETS   ##############################
###############################################################################


###############################################################################
################################## ETS by Regional(model) #####################
###############################################################################


linecolor = ['blue', 'green', 'red', 'c']
t = 0


plt.gca().set_color_cycle(linecolor)









region = ['Pacific Northwest', 'Sierra Nevada','Blue Mountains, OR','Idaho/Western MT','NW Wyoming','Utah','Colorado' ,'Arizona/New Mexico']                
x = np.arange(5,95.1,5)

fig1=plt.figure(num=None, figsize=(12,16), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.25, bottom = 0.1)

for i in range(1,9):
    plot = 420+i
    w = 4*i
    t = w - 4
    ax1 = fig1.add_subplot(plot)
    plt.xlim([5,95.1])
    plt.xticks(np.arange(5,95.1,5))
    plt.ylim([0,0.5])
    plt.yticks(np.arange(0,0.910001,0.1))
    plt.gca().set_color_cycle(linecolor)
    ax1.plot(x,ets_a[:,t:w],linewidth = 2, marker = "o", markeredgecolor = 'none')
    plt.xlim([5,95.1])
    plt.xticks(np.arange(5,95.1,5))
    plt.grid(True)
    blue_line = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='blue',
                           label='NCAR Ens Control')
    green_line = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='green',
                           label='NAM-4km')
    red_line = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='red',
                           label='HRRR')
    cyan_line = mlines.Line2D([], [], linewidth = 2, marker = "o", markeredgecolor = 'none',color='c',
                           label='NAM-12km')
    
    plt.title(region[i-1], fontsize = 18)
            
    
    if i == 1 or i == 3 or i == 5 or i == 7:
        plt.ylabel('Equitable Threat Score\n(Bias Corrected)', fontsize = 14)

    if i == 8 or  i == 7:
        plt.xlabel('24-hour Precipitation Event (Percentile)', fontsize = 12)

plt.legend(handles=[ blue_line, green_line, red_line, cyan_line], loc='upper center', bbox_to_anchor=(-0.16, -0.18), 
           fancybox=True, shadow=True, ncol=4)
plt.savefig('../plots/ets_regionalgrouping_biascorrected_interp.pdf')









###############################################################################
################################## ETS by Model (regions)    ###############################
###############################################################################
linecolor = ['blue', 'green', 'red', 'c', 'y', 'darkred', 'purple', 'salmon']
model = ['NCAR Ens Control', 'NAM-4km','HRRR', 'NAM-12km']                
reg = np.arange(0,31,4)
fig1=plt.figure(num=None, figsize=(12,12), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.15, bottom = 0.2)

for i in range(1,5):
    plot = 220+i
    
    ax1 = fig1.add_subplot(plot)
    plt.xlim([5,95.1])
    plt.xticks(np.arange(5,95.1,5))
    plt.ylim([0,0.5])
    plt.yticks(np.arange(0,0.91001,0.1))
    for p in range(8):
        plt.gca().set_color_cycle(linecolor[p])

        ax1.plot(x,ets_a[:,reg[p]],linewidth = 2, marker = "o", markeredgecolor = 'none')

    reg = reg + 1
    plt.xlim([5,95.1])
    plt.xticks(np.arange(5,95.1,5))
    plt.grid(True)
    
    blue = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='blue',
                           label=region[0])
    green = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='green',
                           label=region[1])
    red = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='red',
                           label=region[2])
    cyan = mlines.Line2D([], [], linewidth = 2, marker = "o", markeredgecolor = 'none',color='c',
                           label=region[3])
    yellow = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='y',
                           label=region[4])
    black = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='darkred',
                           label=region[5])
    purple = mlines.Line2D([], [],linewidth = 2, marker = "o", markeredgecolor = 'none', color='purple',
                           label=region[6])
    salmon = mlines.Line2D([], [], linewidth = 2, marker = "o", markeredgecolor = 'none',color='salmon',
                           label=region[7])
    
    plt.title(model[i-1], fontsize = 18)
            
    
    if i == 1 or i == 3:
        plt.ylabel('Equitable Threat Score (Bias Corrected)', fontsize = 14)

    if i == 3 or  i == 4:
        plt.xlabel('24-hour Precipitation Event (Percentile)', fontsize = 12)

plt.legend(handles=[ blue, green, red, cyan, yellow, black, purple, salmon], loc='upper center', bbox_to_anchor=(-0.10, -0.12), 
           fancybox=True, shadow=True, ncol=4)
plt.savefig('../plots/ets_regional_modelgrouping_biascorrected_interp.pdf')

















