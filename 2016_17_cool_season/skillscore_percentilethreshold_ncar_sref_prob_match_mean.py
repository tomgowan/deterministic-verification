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
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/ncarens_mean_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/ncarens_prob_match_mean_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/sref_arw_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/sref_arw_mean_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/sref_arw_prob_match_mean_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/sref_nmb_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/sref_nmmb_mean_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/sref_nmmb_prob_match_mean_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/2016_17_cool_season/nam3km_precip_12Zto12Z_interp.txt"] #Nam-3km included so bad days can be eliminated

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
ncar_mean_data = data[7,:,:]
ncar_prob_match_mean_data = data[8,:,:]


# Inspect percentile thresholds
#percentile = zeros((20))
#percentile_f = zeros((20))
#
#model = 'sref_nmb_data'
#
#for x in range(len(data[1,:,0])):
#    for y in range(len(data[0,:,0])):
#        if data[1,x,0] == data[0,y,0] == 651:
#            for percent in range(0,100,5):
#                print percent
#                p_array = data[0,y,3:185]
#                p_array_f = data[1,x,3:185]
#                 
#                p_array_f = np.delete(p_array_f, np.where(p_array_f > 1000))          
#                p_array = np.delete(p_array, np.where(p_array > 1000))
#
#                                
#                percentile[percent/5] = np.percentile(p_array,percent)
#                percentile_f[percent/5] = np.percentile(p_array_f,percent)
#

#fig1=plt.figure(num=None, figsize=(5,5))
#ax1 = fig1.add_subplot(111)
#x = np.arange(0,100,5)
#ax1.plot(x,percentile,linewidth = 2, color = 'red')
#ax1.plot(x,percentile_f,linewidth = 2, color = 'blue')
#plt.title('Utah', fontsize = 14)
#plt.ylabel('Abolute Threshold', fontsize = 14)
#plt.xlabel('Percentile', fontsize = 14)
#plt.savefig("../../../public_html/stations_percentiles.pdf")


###############################################################################
##### Dvide into regionms#####################################################
###############################################################################



regions = np.array([[37,40, -122,-118,0,0,0,0],###Sierra Nevada
                    [40,50, -125,-120, 42.97, -121.69,0,0], ##Far NW minus bottom right(>42.97, <-121.69)
                    [35.5,44, -108.7,-104,0,0,0,0], ## CO Rockies
                    [37,44.5, -114,-109.07, 39.32, -109, 43.6, -111.38], ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                    [44,50, -117.2,-109, 45.28,-115.22,44.49, -110.84], ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                    [43,45.5, -116.5,-113.5,44.46,-114.5,0,0]]) ### SW ID minus top right (< 44.46, <-114.5)


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
precip = zeros((2000,185))
p_array = []


for x in range(len(data[1,:,0])):
        for y in range(len(data[0,:,0])):
                if data[1,x,0] == data[0,y,0]:
                    print data[1,x,0]
                    print data[0,y,0]
                    
                    ### Just to investigate data
                    precip[i,:] = data[1,x,:]
                    precip[i+1,:] = data[0,y,:]
                    i = i +2

############ Determine percentiles for entire interior and pacific
inhouse_pac = []
ncar_pac = []
ncar_em_pac = []
ncar_pmm_pac = []
arw_pac = []
arw_em_pac = []
arw_pmm_pac = []
nmmb_pac = []
nmmb_em_pac = []
nmmb_pmm_pac = []

nam_pac = [] #Incuded so bad days can be eliminated

inhouse_int = []
ncar_int = []
ncar_em_int = []
ncar_pmm_int = []
arw_int = []
arw_em_int = []
arw_pmm_int = []
nmmb_int = []
nmmb_em_int = []
nmmb_pmm_int = []

nam_int = [] #Incuded so bad days can be eliminated


for w in range(0,2):
    for x in range(len(data[1,:,0])):
        for y in range(len(data[0,:,0])):
                                ################### PACIFIC ###################            
            if w == 0:
                    if ((regions[0,0] <= data[1,x,1] <= regions[0,1] and regions[0,2] <= data[1,x,2] <= regions[0,3]) or ###Sierra Nevada
                            
                        (regions[1,0] <= data[1,x,1] <= regions[1,1] and regions[1,2] <= data[1,x,2] <= regions[1,3]) and  ##Far NW minus bottom right(>42.97, <-121.69)
                        (data[1,x,1] >= regions[1,4] or data[1,x,2] <= regions[1,5])):
                        if data[1,x,0] == data[0,y,0]:
                            
                            inhouse_pac = np.append(inhouse_pac, data[0,y,3:185])
                            ncar_pac = np.append(ncar_pac, data[1,x,3:185])
                            ncar_em_pac = np.append(ncar_em_pac, data[2,x,3:185])
                            ncar_pmm_pac = np.append(ncar_pmm_pac, data[3,x,3:185])
                            arw_pac = np.append(arw_pac, data[4,x,3:185])
                            arw_em_pac = np.append(arw_em_pac, data[5,x,3:185])
                            arw_pmm_pac = np.append(arw_pmm_pac, data[6,x,3:185])
                            nmmb_pac = np.append(nmmb_pac, data[7,x,3:185])
                            nmmb_em_pac = np.append(nmmb_em_pac, data[8,x,3:185])
                            nmmb_pmm_pac = np.append(nmmb_pmm_pac, data[9,x,3:185])
                            
                            nam_pac = np.append(nam_pac, data[10,x,3:185])
                            
                            
                            
                            
                                                        ################  INTERMOUNTAIN #################                                        
            if w == 1:
                    if ((regions[2,0] <= data[1,x,1] <= regions[2,1] and regions[2,2] <= data[1,x,2] <= regions[2,3]) or ## CO Rockies
    
                        (regions[3,0] <= data[1,x,1] <= regions[3,1] and regions[3,2] <= data[1,x,2] <= regions[3,3]) and  ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                        (data[1,x,1] >= regions[3,4] or data[1,x,2] <= regions[3,5]) and 
                        (data[1,x,1] <= regions[3,6] or data[1,x,2] >= regions[3,7]) or
                        
                        (regions[4,0] <= data[1,x,1] <= regions[4,1] and regions[4,2] <= data[1,x,2] <= regions[4,3]) and  ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                        (data[1,x,1] >= regions[4,4] or data[1,x,2] >= regions[4,5]) and 
                        (data[1,x,1] >= regions[4,6] or data[1,x,2] <= regions[4,7]) or
                        
                        (regions[5,0] <= data[1,x,1] <= regions[5,1] and regions[5,2] <= data[1,x,2] <= regions[5,3]) and  ### SW ID minus top right (< 44.46, <-114.5)
                        (data[1,x,1] <= regions[5,4] or data[1,x,2] <= regions[5,5])):  
                        if data[1,x,0] == data[0,y,0]:
                            
                            inhouse_int = np.append(inhouse_int, data[0,y,3:185])
                            ncar_int = np.append(ncar_int, data[1,x,3:185])
                            ncar_em_int = np.append(ncar_em_int, data[2,x,3:185])
                            ncar_pmm_int = np.append(ncar_pmm_int, data[3,x,3:185])
                            arw_int = np.append(arw_int, data[4,x,3:185])
                            arw_em_int = np.append(arw_em_int, data[5,x,3:185])
                            arw_pmm_int = np.append(arw_pmm_int, data[6,x,3:185])
                            nmmb_int = np.append(nmmb_int, data[7,x,3:185])
                            nmmb_em_int = np.append(nmmb_em_int, data[8,x,3:185])
                            nmmb_pmm_int = np.append(nmmb_pmm_int, data[9,x,3:185])
                            
                            nam_int = np.append(nam_int, data[10,x,3:185])
                            
                            
#### Determine percentiles

abs_thres = np.arange(2.54,80,2.54)

p_array = np.delete(p_array, np.where(p_array > 1000))
    

    

for w in range(0,2):
    print w
    
    
    u = w*10  ##### This is important to change when adding more models ####### 
    for a in range(1,end+1):
        percent= a * 5
        s = a-1
        for x in range(len(data[1,:,0])):
            for y in range(len(data[0,:,0])):
                                ################### PACIFIC ###################            
                if w == 0:
                    if ((regions[0,0] <= data[1,x,1] <= regions[0,1] and regions[0,2] <= data[1,x,2] <= regions[0,3]) or ###Sierra Nevada
                            
                        (regions[1,0] <= data[1,x,1] <= regions[1,1] and regions[1,2] <= data[1,x,2] <= regions[1,3]) and  ##Far NW minus bottom right(>42.97, <-121.69)
                        (data[1,x,1] >= regions[1,4] or data[1,x,2] <= regions[1,5])):
                        if data[1,x,0] == data[0,y,0]:
                
              
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_pac
                            p_array_f = ncar_pac
                            
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_pac > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_pac > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                                                    
                          
                            
                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)


                            
                                                     

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[1,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[1,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[1,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[1,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1
                                        
                                        
                                        
                                    ################  INTERMOUNTAIN #################                                        
                if w == 1:
                    if ((regions[2,0] <= data[1,x,1] <= regions[2,1] and regions[2,2] <= data[1,x,2] <= regions[2,3]) or ## CO Rockies
    
                        (regions[3,0] <= data[1,x,1] <= regions[3,1] and regions[3,2] <= data[1,x,2] <= regions[3,3]) and  ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                        (data[1,x,1] >= regions[3,4] or data[1,x,2] <= regions[3,5]) and 
                        (data[1,x,1] <= regions[3,6] or data[1,x,2] >= regions[3,7]) or
                        
                        (regions[4,0] <= data[1,x,1] <= regions[4,1] and regions[4,2] <= data[1,x,2] <= regions[4,3]) and  ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                        (data[1,x,1] >= regions[4,4] or data[1,x,2] >= regions[4,5]) and 
                        (data[1,x,1] >= regions[4,6] or data[1,x,2] <= regions[4,7]) or
                        
                        (regions[5,0] <= data[1,x,1] <= regions[5,1] and regions[5,2] <= data[1,x,2] <= regions[5,3]) and  ### SW ID minus top right (< 44.46, <-114.5)
                        (data[1,x,1] <= regions[5,4] or data[1,x,2] <= regions[5,5])):  
                        if data[1,x,0] == data[0,y,0]:
                            
                            
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_int
                            p_array_f = ncar_int
                                                  
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_int > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_int > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                           
                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)
                            

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[1,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[1,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[1,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[1,x,z] < percentile_f and data[0,y,z] < percentile:
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
        for x in range(len(data[2,:,0])):
            for y in range(len(data[0,:,0])):
                                                ################### PACIFIC ###################            
                if w == 0:
                    if ((regions[0,0] <= data[2,x,1] <= regions[0,1] and regions[0,2] <= data[2,x,2] <= regions[0,3]) or ###Sierra Nevada
                            
                        (regions[1,0] <= data[2,x,1] <= regions[1,1] and regions[1,2] <= data[2,x,2] <= regions[1,3]) and  ##Far NW minus bottom right(>42.97, <-121.69)
                        (data[2,x,1] >= regions[1,4] or data[2,x,2] <= regions[1,5])):
                        if data[1,x,0] == data[0,y,0]:
                
              
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_pac
                            p_array_f = ncar_em_pac
                                                    

                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_pac > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_pac > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                            
                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)
                            

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[2,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[2,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[2,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[2,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1
                                        
                                        
                                        
                                    ################  INTERMOUNTAIN #################                                        
                if w == 1:
                    if ((regions[2,0] <= data[2,x,1] <= regions[2,1] and regions[2,2] <= data[2,x,2] <= regions[2,3]) or ## CO Rockies
    
                        (regions[3,0] <= data[2,x,1] <= regions[3,1] and regions[3,2] <= data[2,x,2] <= regions[3,3]) and  ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                        (data[2,x,1] >= regions[3,4] or data[2,x,2] <= regions[3,5]) and 
                        (data[2,x,1] <= regions[3,6] or data[2,x,2] >= regions[3,7]) or
                        
                        (regions[4,0] <= data[2,x,1] <= regions[4,1] and regions[4,2] <= data[2,x,2] <= regions[4,3]) and  ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                        (data[2,x,1] >= regions[4,4] or data[2,x,2] >= regions[4,5]) and 
                        (data[2,x,1] >= regions[4,6] or data[2,x,2] <= regions[4,7]) or
                        
                        (regions[5,0] <= data[2,x,1] <= regions[5,1] and regions[5,2] <= data[2,x,2] <= regions[5,3]) and  ### SW ID minus top right (< 44.46, <-114.5)
                        (data[2,x,1] <= regions[5,4] or data[2,x,2] <= regions[5,5])):  
                        if data[2,x,0] == data[0,y,0]:
                            
                            
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_int
                            p_array_f = ncar_em_int
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_int > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_int > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                            
                                                    

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[2,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[2,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[2,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[2,x,z] < percentile_f and data[0,y,z] < percentile:
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
        for x in range(len(data[3,:,0])):
            for y in range(len(data[0,:,0])):
                                                ################### PACIFIC ###################            
                if w == 0:
                    if ((regions[0,0] <= data[3,x,1] <= regions[0,1] and regions[0,2] <= data[3,x,2] <= regions[0,3]) or ###Sierra Nevada
                            
                        (regions[1,0] <= data[3,x,1] <= regions[1,1] and regions[1,2] <= data[3,x,2] <= regions[1,3]) and  ##Far NW minus bottom right(>42.97, <-121.69)
                        (data[3,x,1] >= regions[1,4] or data[3,x,2] <= regions[1,5])):
                        if data[3,x,0] == data[0,y,0]:
                
              
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_pac
                            p_array_f = ncar_pmm_pac
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_pac > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_pac > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                                                    

                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)                         

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[3,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[3,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[3,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[3,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1
                                        
                                        
                                        
                                    ################  INTERMOUNTAIN #################                                        
                if w == 1:
                    if ((regions[2,0] <= data[3,x,1] <= regions[2,1] and regions[2,2] <= data[3,x,2] <= regions[2,3]) or ## CO Rockies
    
                        (regions[3,0] <= data[3,x,1] <= regions[3,1] and regions[3,2] <= data[3,x,2] <= regions[3,3]) and  ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                        (data[3,x,1] >= regions[3,4] or data[3,x,2] <= regions[3,5]) and 
                        (data[3,x,1] <= regions[3,6] or data[3,x,2] >= regions[3,7]) or
                        
                        (regions[4,0] <= data[3,x,1] <= regions[4,1] and regions[4,2] <= data[3,x,2] <= regions[4,3]) and  ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                        (data[3,x,1] >= regions[4,4] or data[3,x,2] >= regions[4,5]) and 
                        (data[3,x,1] >= regions[4,6] or data[3,x,2] <= regions[4,7]) or
                        
                        (regions[5,0] <= data[3,x,1] <= regions[5,1] and regions[5,2] <= data[3,x,2] <= regions[5,3]) and  ### SW ID minus top right (< 44.46, <-114.5)
                        (data[3,x,1] <= regions[5,4] or data[3,x,2] <= regions[5,5])):  
                        if data[3,x,0] == data[0,y,0]:
                            
                            
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_int
                            p_array_f = ncar_pmm_int
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_int > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_int > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                                                    

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)                           

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[3,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[3,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[3,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[3,x,z] < percentile_f and data[0,y,z] < percentile:
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
        for x in range(len(data[4,:,0])):
            for y in range(len(data[0,:,0])):
                                                ################### PACIFIC ###################            
                if w == 0:
                    if ((regions[0,0] <= data[4,x,1] <= regions[0,1] and regions[0,2] <= data[4,x,2] <= regions[0,3]) or ###Sierra Nevada
                            
                        (regions[1,0] <= data[4,x,1] <= regions[1,1] and regions[1,2] <= data[4,x,2] <= regions[1,3]) and  ##Far NW minus bottom right(>42.97, <-121.69)
                        (data[4,x,1] >= regions[1,4] or data[4,x,2] <= regions[1,5])):
                        if data[4,x,0] == data[0,y,0]:
                
              
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_pac
                            p_array_f = arw_pac
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_pac > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_pac > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                                                    
                           

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)
                            

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[4,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[4,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[4,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[4,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1
                                        
                                        
                                        
                                    ################  INTERMOUNTAIN #################                                        
                if w == 1:
                    if ((regions[2,0] <= data[4,x,1] <= regions[2,1] and regions[2,2] <= data[4,x,2] <= regions[2,3]) or ## CO Rockies
    
                        (regions[3,0] <= data[4,x,1] <= regions[3,1] and regions[3,2] <= data[4,x,2] <= regions[3,3]) and  ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                        (data[4,x,1] >= regions[3,4] or data[4,x,2] <= regions[3,5]) and 
                        (data[4,x,1] <= regions[3,6] or data[4,x,2] >= regions[3,7]) or
                        
                        (regions[4,0] <= data[4,x,1] <= regions[4,1] and regions[4,2] <= data[4,x,2] <= regions[4,3]) and  ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                        (data[4,x,1] >= regions[4,4] or data[4,x,2] >= regions[4,5]) and 
                        (data[4,x,1] >= regions[4,6] or data[4,x,2] <= regions[4,7]) or
                        
                        (regions[5,0] <= data[4,x,1] <= regions[5,1] and regions[5,2] <= data[4,x,2] <= regions[5,3]) and  ### SW ID minus top right (< 44.46, <-114.5)
                        (data[4,x,1] <= regions[5,4] or data[4,x,2] <= regions[5,5])):  
                        if data[4,x,0] == data[0,y,0]:
                            
                            
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_int
                            p_array_f = arw_int
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_int > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_int > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                                                    
                           

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)
                            

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[4,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[4,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[4,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[4,x,z] < percentile_f and data[0,y,z] < percentile:
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
        for x in range(len(data[5,:,0])):
            for y in range(len(data[0,:,0])):
                                ################### PACIFIC ###################            
                if w == 0:
                    if ((regions[0,0] <= data[5,x,1] <= regions[0,1] and regions[0,2] <= data[5,x,2] <= regions[0,3]) or ###Sierra Nevada
                            
                        (regions[1,0] <= data[5,x,1] <= regions[1,1] and regions[1,2] <= data[5,x,2] <= regions[1,3]) and  ##Far NW minus bottom right(>42.97, <-121.69)
                        (data[5,x,1] >= regions[1,4] or data[5,x,2] <= regions[1,5])):
                        if data[5,x,0] == data[0,y,0]:
                
                            
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_pac
                            p_array_f = arw_em_pac
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_pac > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_pac > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                                                    

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)                            

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[5,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[5,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[5,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[5,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1
                                        
                                        
                                        
                                    ################  INTERMOUNTAIN #################                                        
                if w == 1:
                    if ((regions[2,0] <= data[5,x,1] <= regions[2,1] and regions[2,2] <= data[5,x,2] <= regions[2,3]) or ## CO Rockies
    
                        (regions[3,0] <= data[5,x,1] <= regions[3,1] and regions[3,2] <= data[5,x,2] <= regions[3,3]) and  ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                        (data[5,x,1] >= regions[3,4] or data[5,x,2] <= regions[3,5]) and 
                        (data[5,x,1] <= regions[3,6] or data[5,x,2] >= regions[3,7]) or
                        
                        (regions[4,0] <= data[5,x,1] <= regions[4,1] and regions[4,2] <= data[5,x,2] <= regions[4,3]) and  ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                        (data[5,x,1] >= regions[4,4] or data[5,x,2] >= regions[4,5]) and 
                        (data[5,x,1] >= regions[4,6] or data[5,x,2] <= regions[4,7]) or
                        
                        (regions[5,0] <= data[5,x,1] <= regions[5,1] and regions[5,2] <= data[5,x,2] <= regions[5,3]) and  ### SW ID minus top right (< 44.46, <-114.5)
                        (data[5,x,1] <= regions[5,4] or data[5,x,2] <= regions[5,5])):  
                        if data[5,x,0] == data[0,y,0]:
                            
                            
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_int
                            p_array_f = arw_em_int
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_int > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_int > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                            
                                                    

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)                           

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[5,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[5,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[5,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[5,x,z] < percentile_f and data[0,y,z] < percentile:
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
        for x in range(len(data[6,:,0])):
            for y in range(len(data[0,:,0])):
                                                ################### PACIFIC ###################            
                if w == 0:
                    if ((regions[0,0] <= data[6,x,1] <= regions[0,1] and regions[0,2] <= data[6,x,2] <= regions[0,3]) or ###Sierra Nevada
                            
                        (regions[1,0] <= data[6,x,1] <= regions[1,1] and regions[1,2] <= data[6,x,2] <= regions[1,3]) and  ##Far NW minus bottom right(>42.97, <-121.69)
                        (data[6,x,1] >= regions[1,4] or data[6,x,2] <= regions[1,5])):
                        if data[6,x,0] == data[0,y,0]:
                
              
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_pac
                            p_array_f = arw_pmm_pac
                            
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_pac > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_pac > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                                                    

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)                          
                            
                            
                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[6,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[6,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[6,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[6,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1
                                        
                                        
                                        
                                    ################  INTERMOUNTAIN #################                                        
                if w == 1:
                    if ((regions[2,0] <= data[6,x,1] <= regions[2,1] and regions[2,2] <= data[6,x,2] <= regions[2,3]) or ## CO Rockies
    
                        (regions[3,0] <= data[6,x,1] <= regions[3,1] and regions[3,2] <= data[6,x,2] <= regions[3,3]) and  ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                        (data[6,x,1] >= regions[3,4] or data[6,x,2] <= regions[3,5]) and 
                        (data[6,x,1] <= regions[3,6] or data[6,x,2] >= regions[3,7]) or
                        
                        (regions[4,0] <= data[6,x,1] <= regions[4,1] and regions[4,2] <= data[6,x,2] <= regions[4,3]) and  ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                        (data[6,x,1] >= regions[4,4] or data[6,x,2] >= regions[4,5]) and 
                        (data[6,x,1] >= regions[4,6] or data[6,x,2] <= regions[4,7]) or
                        
                        (regions[5,0] <= data[6,x,1] <= regions[5,1] and regions[5,2] <= data[6,x,2] <= regions[5,3]) and  ### SW ID minus top right (< 44.46, <-114.5)
                        (data[6,x,1] <= regions[5,4] or data[6,x,2] <= regions[5,5])):  
                        if data[6,x,0] == data[0,y,0]:

                            
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_int
                            p_array_f = arw_pmm_int
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_int > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_int > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                                                    

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[6,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[6,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[6,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[6,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1
                                







###############################################################################
##### Calculate ncar_mean percentiles with good data (<1000) for both ####
###############################################################################

    end = 19
    u = u + 1


    p_array = []

    for a in range(1,end+1):
        percent = a * 5
        s = a-1
        for x in range(len(data[7,:,0])):
            for y in range(len(data[0,:,0])):
                                                ################### PACIFIC ###################            
                if w == 0:
                    if ((regions[0,0] <= data[7,x,1] <= regions[0,1] and regions[0,2] <= data[7,x,2] <= regions[0,3]) or ###Sierra Nevada
                            
                        (regions[1,0] <= data[7,x,1] <= regions[1,1] and regions[1,2] <= data[7,x,2] <= regions[1,3]) and  ##Far NW minus bottom right(>42.97, <-121.69)
                        (data[7,x,1] >= regions[1,4] or data[7,x,2] <= regions[1,5])):
                        if data[7,x,0] == data[0,y,0]:
                
              
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_pac
                            p_array_f = nmmb_pac
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_pac > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_pac > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                            

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)                         
                            
                            
                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[7,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[7,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[7,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[7,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1
                                        
                                        
                                        
                                    ################  INTERMOUNTAIN #################                                        
                if w == 1:
                    if ((regions[2,0] <= data[7,x,1] <= regions[2,1] and regions[2,2] <= data[7,x,2] <= regions[2,3]) or ## CO Rockies
    
                        (regions[3,0] <= data[7,x,1] <= regions[3,1] and regions[3,2] <= data[7,x,2] <= regions[3,3]) and  ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                        (data[7,x,1] >= regions[3,4] or data[7,x,2] <= regions[3,5]) and 
                        (data[7,x,1] <= regions[3,6] or data[7,x,2] >= regions[3,7]) or
                        
                        (regions[4,0] <= data[7,x,1] <= regions[4,1] and regions[4,2] <= data[7,x,2] <= regions[4,3]) and  ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                        (data[7,x,1] >= regions[4,4] or data[7,x,2] >= regions[4,5]) and 
                        (data[7,x,1] >= regions[4,6] or data[7,x,2] <= regions[4,7]) or
                        
                        (regions[5,0] <= data[7,x,1] <= regions[5,1] and regions[5,2] <= data[7,x,2] <= regions[5,3]) and  ### SW ID minus top right (< 44.46, <-114.5)
                        (data[7,x,1] <= regions[5,4] or data[7,x,2] <= regions[5,5])):  
                        if data[7,x,0] == data[0,y,0]:

                            
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_int
                            p_array_f = nmmb_int
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_int > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_int > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                            
                                                    
                           
                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[7,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[7,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[7,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[7,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1









###############################################################################
##### Calculate ncar_prob_match_mean percentiles with good data (<1000) for both ####
###############################################################################

    end = 19
    u = u + 1


    p_array = []

    for a in range(1,end+1):
        percent = a * 5
        s = a-1
        for x in range(len(data[8,:,0])):
            for y in range(len(data[0,:,0])):
                                                ################### PACIFIC ###################            
                if w == 0:
                    if ((regions[0,0] <= data[8,x,1] <= regions[0,1] and regions[0,2] <= data[8,x,2] <= regions[0,3]) or ###Sierra Nevada
                            
                        (regions[1,0] <= data[8,x,1] <= regions[1,1] and regions[1,2] <= data[8,x,2] <= regions[1,3]) and  ##Far NW minus bottom right(>42.97, <-121.69)
                        (data[8,x,1] >= regions[1,4] or data[8,x,2] <= regions[1,5])):
                        if data[8,x,0] == data[0,y,0]:
                
              
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_pac
                            p_array_f = nmmb_em_pac
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_pac > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_pac > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                            
                            
                                                    

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)                           
                            
                            
                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[8,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[8,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[8,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[8,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1
                                        
                                        
                                        
                                    ################  INTERMOUNTAIN #################                                        
                if w == 1:
                    if ((regions[2,0] <= data[8,x,1] <= regions[2,1] and regions[2,2] <= data[8,x,2] <= regions[2,3]) or ## CO Rockies
    
                        (regions[3,0] <= data[8,x,1] <= regions[3,1] and regions[3,2] <= data[8,x,2] <= regions[3,3]) and  ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                        (data[8,x,1] >= regions[3,4] or data[8,x,2] <= regions[3,5]) and 
                        (data[8,x,1] <= regions[3,6] or data[8,x,2] >= regions[3,7]) or
                        
                        (regions[4,0] <= data[8,x,1] <= regions[4,1] and regions[4,2] <= data[8,x,2] <= regions[4,3]) and  ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                        (data[8,x,1] >= regions[4,4] or data[8,x,2] >= regions[4,5]) and 
                        (data[8,x,1] >= regions[4,6] or data[8,x,2] <= regions[4,7]) or
                        
                        (regions[5,0] <= data[8,x,1] <= regions[5,1] and regions[5,2] <= data[8,x,2] <= regions[5,3]) and  ### SW ID minus top right (< 44.46, <-114.5)
                        (data[8,x,1] <= regions[5,4] or data[8,x,2] <= regions[5,5])):  
                        if data[8,x,0] == data[0,y,0]:
                            
                            
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_int
                            p_array_f = nmmb_em_int
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_int > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_int > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                                                    
                           

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)                            

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[8,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[8,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[8,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[8,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1











###############################################################################
##### Calculate ncar_prob_match_mean percentiles with good data (<1000) for both ####
###############################################################################

    end = 19
    u = u + 1


    p_array = []

    for a in range(1,end+1):
        percent = a * 5
        s = a-1
        for x in range(len(data[9,:,0])):
            for y in range(len(data[0,:,0])):
                                                ################### PACIFIC ###################            
                if w == 0:
                    if ((regions[0,0] <= data[9,x,1] <= regions[0,1] and regions[0,2] <= data[9,x,2] <= regions[0,3]) or ###Sierra Nevada
                            
                        (regions[1,0] <= data[9,x,1] <= regions[1,1] and regions[1,2] <= data[9,x,2] <= regions[1,3]) and  ##Far NW minus bottom right(>42.97, <-121.69)
                        (data[9,x,1] >= regions[1,4] or data[9,x,2] <= regions[1,5])):
                        if data[9,x,0] == data[0,y,0]:
                
              
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_pac
                            p_array_f = nmmb_pmm_pac
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_pac > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_pac > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                                                    

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)                          
                            
                            
                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[9,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[9,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[9,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[9,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1
                                        
                                        
                                        
                                    ################  INTERMOUNTAIN #################                                        
                if w == 1:
                    if ((regions[2,0] <= data[9,x,1] <= regions[2,1] and regions[2,2] <= data[9,x,2] <= regions[2,3]) or ## CO Rockies
    
                        (regions[3,0] <= data[9,x,1] <= regions[3,1] and regions[3,2] <= data[9,x,2] <= regions[3,3]) and  ### Intermounaint mimus bottom right and top left (> 39.32, < -109.54, <43.6, > -111.38)
                        (data[9,x,1] >= regions[3,4] or data[9,x,2] <= regions[3,5]) and 
                        (data[9,x,1] <= regions[3,6] or data[9,x,2] >= regions[3,7]) or
                        
                        (regions[4,0] <= data[9,x,1] <= regions[4,1] and regions[4,2] <= data[9,x,2] <= regions[4,3]) and  ### Intermountain NW minus bottom left and bottom right ( > 45.28, > -115.22, > 44.49, < -110.84)
                        (data[9,x,1] >= regions[4,4] or data[9,x,2] >= regions[4,5]) and 
                        (data[9,x,1] >= regions[4,6] or data[9,x,2] <= regions[4,7]) or
                        
                        (regions[5,0] <= data[9,x,1] <= regions[5,1] and regions[5,2] <= data[9,x,2] <= regions[5,3]) and  ### SW ID minus top right (< 44.46, <-114.5)
                        (data[9,x,1] <= regions[5,4] or data[9,x,2] <= regions[5,5])):  
                        if data[9,x,0] == data[0,y,0]:
                            
                            
                            #p_array is all precip days for one station.  Created to determine percentiles for each station
                            p_array = inhouse_int
                            p_array_f = nmmb_pmm_int
                            
                            
                            ## NAM is only mondel with bad data
                            p_array = np.delete(p_array, np.where(nam_int > 1000))
                            p_array_f = np.delete(p_array_f, np.where(nam_int > 1000))
                  
                            p_array_f = np.delete(p_array_f, np.where(p_array> 1000))
                            p_array = np.delete(p_array, np.where(p_array > 1000))
                                                    
                           

                            
                            percentile = np.percentile(p_array,percent)
                            percentile_f = np.percentile(p_array_f,percent)                        

                            for z in range(3,185):
                        
                                # Excludes bad data 
                                if all(data[1:,x,z] < 1000) and  data[0,y,z] < 1000:
                                    
                                    if data[9,x,z] >= percentile_f and data[0,y,z] >= percentile:
                                        hit[s,u] = hit[s,u] + 1
                                        
                                    if data[9,x,z] < percentile_f and data[0,y,z] >= percentile:
                                        miss[s,u] = miss[s,u] + 1
                                            
                                    if data[9,x,z] >= percentile_f and data[0,y,z] < percentile:
                                        falarm[s,u] = falarm[s,u] + 1
                                                
                                    if data[9,x,z] < percentile_f and data[0,y,z] < percentile:
                                        correct_non[s,u] = correct_non[s,u] + 1
    
#%%
# Calcualte Bias, Hit Rate, False Alarm Rate, ETS
                       
ets = zeros((end,40))
hitrate = zeros((end,40))
bias = zeros((end,40))
faratio = zeros((end,40))
farate = zeros((end,40))
ets_a = zeros((end,40))
                             
for a in range(1,end+1):
    s=a-1
    for i in range(40):                                
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

################################################################################
################################### PLOTS ######################################
################################################################################
#
#
#
#
################################################################################
################################### ETS by Regional(model) #####################
################################################################################
#
#
#
#linecolor = ['blue', 'green', 'red', 'c', 'gold','magenta']
#t = 0
#
#
#plt.gca().set_color_cycle(linecolor)
#
#props = dict(boxstyle='square', facecolor='white', alpha=1)
#
#region = ['Pacific', 'Interior']                
#
#x = np.arange(5,95.0001,5)
#
#fig1=plt.figure(num=None, figsize=(11,12), dpi=500, facecolor='w', edgecolor='k')
#fig1.subplots_adjust(hspace=.2, bottom = 0.17)
#
#for i in range(0,2):
#    plot = 211+i
#    ax1 = fig1.add_subplot(plot)
#    if i == 1:
#        ax1.text(7, .075, 'Interior', fontsize = 25, bbox = props)
#        plt.xlabel('Precipitation Event (Percentile)',fontsize = 18)
#
#        
#    if i == 0:
#        plt.title('Equitable Threat Score', fontsize = 22)
#        ax1.text(7, .075, 'Pacific', fontsize = 25, bbox = props)
#        
#    t = 6*i+6 
#    plt.gca().set_color_cycle(linecolor)
#    ax1.plot(x,ets[:,6*i:t], linewidth = 2, marker = "o", markeredgecolor = 'none')
#
#    plt.xlim([6,95.1])
#    plt.xticks(np.arange(5,96,10))
#    ax1.set_xticklabels(np.arange(5,96,10), fontsize = 16)
#    ax1.tick_params(axis='y', labelsize=16)
#
#    plt.grid(True)
#    
#    blue = mlines.Line2D([], [], color='blue',
#                           label='NCAR ENS CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
#    green = mlines.Line2D([], [], color='green',
#                           label='GFS', linewidth = 2,marker = "o", markeredgecolor = 'none')
#    red = mlines.Line2D([], [], color='red',
#                           label='HRRR', linewidth = 2,marker = "o", markeredgecolor = 'none')
#    cyan = mlines.Line2D([], [], color='c',
#                           label='NAM-3km', linewidth = 2,marker = "o", markeredgecolor = 'none')
#    gold = mlines.Line2D([], [], color='gold',
#                           label='SREF ARW CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
#    magenta = mlines.Line2D([], [], color='magenta',
#                           label='SREF NMB CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
#    
#
#    
#    plt.ylabel('Score', fontsize = 18)
#    
#    
#
#plt.legend(handles=[ blue, green, red, cyan, gold, magenta], loc='upper center', bbox_to_anchor=(0.50, -0.17), 
#           ncol=3, fontsize = 16)
##plt.tight_layout()
#plt.savefig('../../../public_html/ets_regionalgrouping_biascorrected_interp_2016_17.pdf')
#plt.show()
#




#%%





#x = np.arange(5.08,50.800001,2.54)
x = np.arange(5,95.1,5)

linecolor = ['lightblue', 'blue', 'darkblue', 'lightgreen', 'mediumseagreen', 'darkgreen',  'lightcoral','red', 'darkred']
fig1=plt.figure(num=None, figsize=(14,15), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.2, bottom = 0.2)


props = dict(boxstyle='square', facecolor='white', alpha=1)

ax2 = fig1.add_subplot(321)
plt.gca().set_color_cycle(linecolor)
ax2.plot(x,hitrate[:,0:9],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)

lightblue = mlines.Line2D([], [], color='lightblue',
                           label='NCAR ENS CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
blue = mlines.Line2D([], [], color='blue',
                           label='NCAR ENS EM', linewidth = 2,marker = "o", markeredgecolor = 'none')
darkblue = mlines.Line2D([], [], color='darkblue',
                           label='NCAR ENS PMM', linewidth = 2,marker = "o", markeredgecolor = 'none')
lightgreen = mlines.Line2D([], [], color='lightgreen',
                           label='SREF ARW CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
mediumseagreen = mlines.Line2D([], [], color='mediumseagreen',
                           label='SREF ARW EM', linewidth = 2,marker = "o", markeredgecolor = 'none')
darkgreen = mlines.Line2D([], [], color='darkgreen',
                           label='SREF ARW PMM', linewidth = 2,marker = "o", markeredgecolor = 'none')
lightcoral = mlines.Line2D([], [], color='lightcoral',
                           label='SREF NMMB CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
red = mlines.Line2D([], [], color='red',
                           label='SREF NMMB EM', linewidth = 2,marker = "o", markeredgecolor = 'none')
darkred = mlines.Line2D([], [], color='darkred',
                           label='SREF NMMB PMM', linewidth = 2,marker = "o", markeredgecolor = 'none')
props = dict(boxstyle='square', facecolor='white', alpha=1)
plt.ylabel('Hit Rate', fontsize = 20)
plt.title('Pacific Ranges', fontsize = 20)
plt.xlim([75,95.1])
plt.ylim([0.19,0.7])
plt.xticks(np.arange(75,96,5))
plt.yticks(np.arange(0.2,0.8,0.1))
ax2.set_xticklabels(np.arange(75,96,5), fontsize = 14)
ax2.tick_params(axis='y', labelsize=14)
locx = 30
locy = 30
font = 25
fig1.text(0.129, 0.693, '(a)', fontsize = font)




ax2 = fig1.add_subplot(322)
plt.gca().set_color_cycle(linecolor)
ax2.plot(x,hitrate[:,10:19],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.title('Interior Ranges', fontsize = 20)
plt.xlim([75,95.1])
plt.ylim([0.19,0.7])
plt.xticks(np.arange(5,96,5))
plt.yticks(np.arange(0.2,0.8,0.1))
ax2.set_xticklabels(np.arange(5,96,5), fontsize = 14)
ax2.tick_params(axis='y', labelsize=14)
fig1.text(0.552, 0.693, '(b)', fontsize = font)





ax3 = fig1.add_subplot(323, sharex = ax2)
plt.gca().set_color_cycle(linecolor)
ax3.plot(x,faratio[:,0:9],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.ylabel('False Alarm Ratio', fontsize = 20)
plt.xlim([75,95.1])
plt.ylim([0.09,0.8])
plt.xticks(np.arange(5,96,5))
plt.yticks(np.arange(0.1,0.9,0.1))
ax3.set_xticklabels(np.arange(5,96,5), fontsize = 14)
ax3.tick_params(axis='y', labelsize=14)
fig1.text(0.129, 0.449, '(c)', fontsize = font)



ax3 = fig1.add_subplot(324, sharex = ax2)
plt.gca().set_color_cycle(linecolor)
ax3.plot(x,faratio[:,10:19],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.xlim([75,95.1])
plt.ylim([0.09,0.8])
plt.xticks(np.arange(5,96,5))
plt.yticks(np.arange(0.1,0.9,0.1))
ax3.set_xticklabels(np.arange(5,96,5), fontsize = 14)
ax3.tick_params(axis='y', labelsize=14)
fig1.text(0.552, 0.449, '(d)', fontsize = font)


ax4 = fig1.add_subplot(325, sharex = ax2)
plt.gca().set_color_cycle(linecolor)
ax4.plot(x,ets[:,0:9],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.ylabel('ETS', fontsize = 20)
plt.xlabel('Event Threshold (Percentile)', fontsize = 20)
plt.xlim([75,95.1])
plt.ylim([0.09,0.45])
plt.xticks(np.arange(5,96,5))
plt.yticks(np.arange(0.1,0.5,0.05))
ax4.set_xticklabels(np.arange(5,96,5), fontsize = 14)
ax4.tick_params(axis='y', labelsize=14)
fig1.text(0.129, 0.213, '(e)', fontsize = font)



ax4 = fig1.add_subplot(326, sharex = ax2)
plt.gca().set_color_cycle(linecolor)
ax4.plot(x,ets[:,10:19],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.xlabel('Event Threshold (Percentile)', fontsize = 20)
plt.xlim([75,95.1])
plt.ylim([0.09,0.45])
plt.xticks(np.arange(5,96,5))
plt.xlim([75,95.1])
ax4.set_xticklabels(np.arange(5,96,5), fontsize = 14)
plt.yticks(np.arange(0.1,0.5,0.05))
ax4.tick_params(axis='y', labelsize=14)
fig1.text(0.552, 0.213, '(f)', fontsize = font)




plt.legend(handles=[lightblue, blue, darkblue, lightgreen, mediumseagreen, darkgreen, lightcoral, red,  darkred], loc='upper center', bbox_to_anchor=(-0.10, -0.21), 
           ncol=3, fontsize = 18)
plt.savefig("../../../public_html/ms_thesis_plots/categorical_scores_percentile_2016_17_ncar_sref_PM.pdf")
plt.close(fig1)



##%%
################################################################################
############### ETS and Bias Score for ICAM  Regional(model) #####################
################################################################################
#
#
#
#linecolor = ['blue', 'green', 'red', 'c', 'gold','magenta']
#t = 0
#
#
#plt.gca().set_color_cycle(linecolor)
#
#props = dict(boxstyle='square', facecolor='white', alpha=1)
#
#region = ['Pacific', 'Interior']                
#
#x = np.arange(5,95.0001,5)
#
#fig1=plt.figure(num=None, figsize=(22,12), dpi=500, facecolor='w', edgecolor='k')
#fig1.subplots_adjust(hspace=.2, bottom = 0.17)
#
#for i in range(4):
#    plot = 221+i
#    ax1 = fig1.add_subplot(plot)
#
#    
#    if i == 0: 
#        plt.title('Equitable Threat Score', fontsize = 22)
#        ax1.text(7, .075, 'Pacific', fontsize = 25, bbox = props)
#        t = 6*i+6 
#        plt.gca().set_color_cycle(linecolor)
#        ax1.plot(x,ets[:,6*i:t], linewidth = 2, marker = "o", markeredgecolor = 'none')
#        
#    if i == 1:
#        plt.title('Bias Score', fontsize = 22)
#        ax1.text(7, .075, 'Pacific', fontsize = 25, bbox = props)
#        ax1.plot(x,bias[:,0:6],linewidth = 2,marker = "o", markeredgecolor = 'none')
#        
#    if i == 2:
#        ax1.text(7, .075, 'Interior', fontsize = 25, bbox = props)
#        i = i - 1
#        t = 6*i+6 
#        plt.gca().set_color_cycle(linecolor)
#        ax1.plot(x,ets[:,6*i:t], linewidth = 2, marker = "o", markeredgecolor = 'none')
#        
#    if i == 3:
#        ax1.text(7, .075, 'Interior', fontsize = 25, bbox = props)
#        ax1.plot(x,bias[:,6:12],linewidth = 2,marker = "o", markeredgecolor = 'none')
#
#
#    plt.xlim([6,95.1])
#    plt.xticks(np.arange(5,96,10))
#    ax1.set_xticklabels(np.arange(5,96,10), fontsize = 16)
#    ax1.tick_params(axis='y', labelsize=16)
#
#    plt.grid(True)
#    
#    blue = mlines.Line2D([], [], color='blue',
#                           label='NCAR ENS CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
#    green = mlines.Line2D([], [], color='green',
#                           label='GFS', linewidth = 2,marker = "o", markeredgecolor = 'none')
#    red = mlines.Line2D([], [], color='red',
#                           label='HRRR', linewidth = 2,marker = "o", markeredgecolor = 'none')
#    cyan = mlines.Line2D([], [], color='c',
#                           label='NAM-3km', linewidth = 2,marker = "o", markeredgecolor = 'none')
#    gold = mlines.Line2D([], [], color='gold',
#                           label='SREF ARW CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
#    magenta = mlines.Line2D([], [], color='magenta',
#                           label='SREF NMB CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
#    
#
#    if i == 0 or 2:
#        plt.ylabel('Score', fontsize = 18)
#    
#    
#
#plt.legend(handles=[ blue, green, red, cyan, gold, magenta], loc='upper center', bbox_to_anchor=(0.50, -0.17), 
#           ncol=3, fontsize = 16)
##plt.tight_layout()
#plt.savefig('../../../public_html/ets_bias_score_regional_interp_2016_17.pdf')
#plt.show()
#




