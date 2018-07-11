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
hit = zeros((end,4)) #### There arrays now go in the order col 1-4:region 1, 5-8:region2,etc...
miss = zeros((end,4))
falarm = zeros((end,4))
correct_non = zeros((end,4))
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


t = 0
percent= 75  ### for n2,h2,n42....75 for n,h,n4
ncar_stats = zeros((800,10))
for x in range(len(ncar_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if ncar_data[x,0] == inhouse_data[y,0]:
                        ncar_stats[t,0:2] = ncar_data[x,1:3]
                        
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)
                        #percentile = 90

                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and inhouse_data[y,z] < 1000:
                                ##### Hits
                                if ncar_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    ncar_stats[t,2] = ncar_stats[t,2] + 1
                                ##### Misses
                                if ncar_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    ncar_stats[t,3] = ncar_stats[t,3] + 1
                                ##### Falarm
                                if ncar_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    ncar_stats[t,4] = ncar_stats[t,4] + 1
                                ##### Correct_non
                                if ncar_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    ncar_stats[t,5] = ncar_stats[t,5] + 1
                                
                        t = t + 1

    
        
                       

###############################################################################
##### Calculate ETS_nam4k using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
u = u + 1

p_array = []
t = 0

nam4k_stats = zeros((800,10))
for x in range(len(nam4k_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if nam4k_data[x,0] == inhouse_data[y,0]:
                        nam4k_stats[t,0:2] = nam4k_data[x,1:3]
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and inhouse_data[y,z] < 1000:
                            
                                if nam4k_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    nam4k_stats[t,2] = nam4k_stats[t,2] + 1
                            
                                if nam4k_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    nam4k_stats[t,3] = nam4k_stats[t,3] + 1
                            
                                if nam4k_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    nam4k_stats[t,4] = nam4k_stats[t,4] + 1
                            
                                if nam4k_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    nam4k_stats[t,5] = nam4k_stats[t,5] + 1
                        t = t + 1        

    
        
                       


###############################################################################
##### Calculate ETS_hrrr using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
u = u + 1

p_array = []
t = 0

hrrr_stats = zeros((800,10))
for x in range(len(hrrr_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if hrrr_data[x,0] == inhouse_data[y,0]:
                        hrrr_stats[t,0:2] = hrrr_data[x,1:3]
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and inhouse_data[y,z] < 1000:
                            
                                if hrrr_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                   hrrr_stats[t,2] = hrrr_stats[t,2] + 1
                            
                                if hrrr_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    hrrr_stats[t,3] = hrrr_stats[t,3] + 1
                            
                                if hrrr_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    hrrr_stats[t,4] = hrrr_stats[t,4] + 1
                            
                                if hrrr_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    hrrr_stats[t,5] = hrrr_stats[t,5] + 1
                                
                        t = t + 1


###############################################################################
##### Calculate ETS_nam12k using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
u = u + 1

p_array = []
t = 0

nam12k_stats = zeros((800,10))
for x in range(len(nam12k_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if nam12k_data[x,0] == inhouse_data[y,0]:
                        nam12k_stats[t,0:2] = nam12k_data[x,1:3]
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and inhouse_data[y,z] < 1000:
                            
                                if nam12k_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    nam12k_stats[t,2] = nam12k_stats[t,2] + 1
                            
                                if nam12k_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    nam12k_stats[t,3] = nam12k_stats[t,3] + 1
                            
                                if nam12k_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    nam12k_stats[t,4] = nam12k_stats[t,4] + 1
                            
                                if nam12k_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    nam12k_stats[t,5] = nam12k_stats[t,5] + 1
                        t = t + 1        

    
        
                       

###############################################################################
##### Calculate gfs using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
u = u + 1

p_array = []
t = 0

gfs_stats = zeros((800,10))
for x in range(len(gfs_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if gfs_data[x,0] == inhouse_data[y,0]:
                        gfs_stats[t,0:2] = gfs_data[x,1:3]
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and inhouse_data[y,z] < 1000:
                            
                                if gfs_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    gfs_stats[t,2] = gfs_stats[t,2] + 1
                            
                                if gfs_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    gfs_stats[t,3] = gfs_stats[t,3] + 1
                            
                                if gfs_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    gfs_stats[t,4] = gfs_stats[t,4] + 1
                            
                                if gfs_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    gfs_stats[t,5] = gfs_stats[t,5] + 1
                        t = t + 1        

    
        
                       



############    SKILL score calcs    #########################################
                                
                       
ets = zeros((end,5))
ets_a = zeros((end,5))
hitrate = zeros((end,5))
bias = zeros((end,5))
far = zeros((end,5))
pofd = zeros((end,5))

mod = ['ncar_stats', 'nam4k_stats', 'hrrr_stats', 'nam12k_stats', 'gfs_stats']
    
### hits(2), miss(3). falarm(4), corredctnon(5), ets(6)
    
### make simpler names
n = ncar_stats
n4 = nam4k_stats
h = hrrr_stats
n12 = nam12k_stats
g = gfs_stats


thres = 10
####  NCAR                         
for a in range(3):
    for i in range(800):
        if sum(n[i,2:4]) < thres:
            n[i,6:8] = -9999
            n[i,0] = 0
        else:                                
            a_ref = 0
            a_ref = ((n[i,2] + n[i,3])*(n[i,2] + n[i,4]))/(n[i,2]+n[i,4]+n[i,3]+n[i,5])
    
            ### ets    
            n[i,6] = (n[i,2] - a_ref)/(n[i,2] - a_ref + n[i,4] + n[i,3])
            n[i,7] = (n[i,2] + n[i,4])/(n[i,2] + n[i,3])  ## BIAS
        
        
 #####  hrrr       
for a in range(3):
    for i in range(800):
        if sum(h[i,2:4]) < thres:
            h[i,6:8] = -9999
            h[i,0] = 0
        else:                                
            a_ref = 0
            a_ref = ((h[i,2] + h[i,3])*(h[i,2] + h[i,4]))/(h[i,2]+h[i,4]+h[i,3]+h[i,5])
    
            ### ets    
            h[i,6] = (h[i,2] - a_ref)/(h[i,2] - a_ref + h[i,4] + h[i,3])
            h[i,7] = (h[i,2] + h[i,4])/(h[i,2] + h[i,3])  ## BIAS
        
        
### nam4k        
for a in range(3):
    for i in range(800):
        if sum(n4[i,2:4]) < thres:
            n4[i,6:8] = -9999
            n4[i,0] = 0
        else:                                
            a_ref = 0
            a_ref = ((n4[i,2] + n4[i,3])*(n4[i,2] + n4[i,4]))/(n4[i,2]+n4[i,4]+n4[i,3]+n4[i,5])
    
            ### ets    
            n4[i,6] = (n4[i,2] - a_ref)/(n4[i,2] - a_ref + n4[i,4] + n4[i,3])
            n4[i,7] = (n4[i,2] + n4[i,4])/(n4[i,2] + n4[i,3])  ## BIAS
            
            
### nam12k        
for a in range(3):
    for i in range(800):
        if sum(n12[i,2:4]) < thres:
            n12[i,6:8] = -9999
            n12[i,0] = 0
        else:                                
            a_ref = 0
            a_ref = ((n12[i,2] + n12[i,3])*(n12[i,2] + n12[i,4]))/(n12[i,2]+n12[i,4]+n12[i,3]+n12[i,5])
    
            ### ets    
            n12[i,6] = (n12[i,2] - a_ref)/(n12[i,2] - a_ref + n12[i,4] + n12[i,3])
            n12[i,7] = (n12[i,2] + n12[i,4])/(n12[i,2] + n12[i,3])  ## BIAS



            
### gfs        
for a in range(3):
    for i in range(800):
        if sum(g[i,2:4]) < thres:
            g[i,6:8] = -9999
            g[i,0] = 0
        else:                                
            a_ref = 0
            a_ref = ((g[i,2] + g[i,3])*(g[i,2] + g[i,4]))/(g[i,2]+g[i,4]+g[i,3]+g[i,5])
    
            ### ets    
            g[i,6] = (g[i,2] - a_ref)/(g[i,2] - a_ref + g[i,4] + g[i,3])
            g[i,7] = (g[i,2] + g[i,4])/(g[i,2] + g[i,3])  ## BIAS













###############################################################################
###############################################################################
###############################################################################
###############################################################################
############################ Upper decile #####################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################












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


t = 0
percent= 90  ### for n2,h2,n42....75 for n,h,n4
ncar_stats = zeros((800,10))
for x in range(len(ncar_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if ncar_data[x,0] == inhouse_data[y,0]:
                        ncar_stats[t,0:2] = ncar_data[x,1:3]
                        
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)
                        #percentile = 90

                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and inhouse_data[y,z] < 1000:
                                ##### Hits
                                if ncar_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    ncar_stats[t,2] = ncar_stats[t,2] + 1
                                ##### Misses
                                if ncar_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    ncar_stats[t,3] = ncar_stats[t,3] + 1
                                ##### Falarm
                                if ncar_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    ncar_stats[t,4] = ncar_stats[t,4] + 1
                                ##### Correct_non
                                if ncar_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    ncar_stats[t,5] = ncar_stats[t,5] + 1
                                
                        t = t + 1

    
        
                       

###############################################################################
##### Calculate ETS_nam4k using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
u = u + 1

p_array = []
t = 0

nam4k_stats = zeros((800,10))
for x in range(len(nam4k_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if nam4k_data[x,0] == inhouse_data[y,0]:
                        nam4k_stats[t,0:2] = nam4k_data[x,1:3]
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and inhouse_data[y,z] < 1000:
                            
                                if nam4k_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    nam4k_stats[t,2] = nam4k_stats[t,2] + 1
                            
                                if nam4k_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    nam4k_stats[t,3] = nam4k_stats[t,3] + 1
                            
                                if nam4k_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    nam4k_stats[t,4] = nam4k_stats[t,4] + 1
                            
                                if nam4k_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    nam4k_stats[t,5] = nam4k_stats[t,5] + 1
                        t = t + 1        

    
        
                       


###############################################################################
##### Calculate ETS_hrrr using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
u = u + 1

p_array = []
t = 0

hrrr_stats = zeros((800,10))
for x in range(len(hrrr_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if hrrr_data[x,0] == inhouse_data[y,0]:
                        hrrr_stats[t,0:2] = hrrr_data[x,1:3]
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and inhouse_data[y,z] < 1000:
                            
                                if hrrr_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                   hrrr_stats[t,2] = hrrr_stats[t,2] + 1
                            
                                if hrrr_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    hrrr_stats[t,3] = hrrr_stats[t,3] + 1
                            
                                if hrrr_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    hrrr_stats[t,4] = hrrr_stats[t,4] + 1
                            
                                if hrrr_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    hrrr_stats[t,5] = hrrr_stats[t,5] + 1
                                
                        t = t + 1



###############################################################################
##### Calculate ETS_nam12k using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
u = u + 1

p_array = []
t = 0

nam12k_stats = zeros((800,10))
for x in range(len(nam12k_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if nam12k_data[x,0] == inhouse_data[y,0]:
                        nam12k_stats[t,0:2] = nam12k_data[x,1:3]
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and inhouse_data[y,z] < 1000:
                            
                                if nam12k_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    nam12k_stats[t,2] = nam12k_stats[t,2] + 1
                            
                                if nam12k_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    nam12k_stats[t,3] = nam12k_stats[t,3] + 1
                            
                                if nam12k_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    nam12k_stats[t,4] = nam12k_stats[t,4] + 1
                            
                                if nam12k_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    nam12k_stats[t,5] = nam12k_stats[t,5] + 1
                        t = t + 1        

    



###############################################################################
##### Calculate ETS_nam12k using percentiles with good data (<1000) for both ####
###############################################################################

end = 19   
u = u + 1

p_array = []
t = 0

gfs_stats = zeros((800,10))
for x in range(len(gfs_data[:,0])):
            for y in range(len(inhouse_data[:,0])):
                    if gfs_data[x,0] == inhouse_data[y,0]:
                        gfs_stats[t,0:2] = gfs_data[x,1:3]
                        #p_array is all precip days for one station.  Created to determine percentiles for each station
                        p_array = inhouse_data[y,3:185]
                        p_array = np.delete(p_array, np.where(p_array < 2.54))
                        p_array = np.delete(p_array, np.where(p_array > 1000))
   
                        percentile = np.percentile(p_array,percent)


                        for z in range(3,185):
                        
                            # Excludes bad data 
                            if all(data[1:,x,z] < 1000) and inhouse_data[y,z] < 1000:
                            
                                if gfs_data[x,z] >= percentile and inhouse_data[y,z] >= percentile:
                                    gfs_stats[t,2] = gfs_stats[t,2] + 1
                            
                                if gfs_data[x,z] < percentile and inhouse_data[y,z] >= percentile:
                                    gfs_stats[t,3] = gfs_stats[t,3] + 1
                            
                                if gfs_data[x,z] >= percentile and inhouse_data[y,z] < percentile:
                                    gfs_stats[t,4] = gfs_stats[t,4] + 1
                            
                                if gfs_data[x,z] < percentile and inhouse_data[y,z] < percentile:
                                    gfs_stats[t,5] = gfs_stats[t,5] + 1
                        t = t + 1        









        


############    SKILL score calcs    #########################################
                                
                       
ets = zeros((end,5))
ets_a = zeros((end,5))
hitrate = zeros((end,5))
bias = zeros((end,5))
far = zeros((end,5))
pofd = zeros((end,5))

mod = ['ncar_stats', 'nam4k_stats', 'hrrr_stats', 'gfs_stats']
    
### hits(2), miss(3). falarm(4), corredctnon(5), ets(6)
    
### make simpler names
n2 = ncar_stats
n42 = nam4k_stats
h2 = hrrr_stats
n122 = nam12k_stats
g2 = gfs_stats


thres = 10
####  NCAR                         
for a in range(3):
    for i in range(800):
        if sum(n2[i,2:4]) < thres:
            n2[i,6:8] = -9999
            n2[i,0] = 0
        else:                                
            a_ref = 0
            a_ref = ((n2[i,2] + n2[i,3])*(n2[i,2] + n2[i,4]))/(n2[i,2]+n2[i,4]+n2[i,3]+n2[i,5])
    
            ### ets    
            n2[i,6] = (n2[i,2] - a_ref)/(n2[i,2] - a_ref + n2[i,4] + n2[i,3])
            n2[i,7] = (n2[i,2] + n2[i,4])/(n2[i,2] + n2[i,3])  ## BIAS
        
        
 #####  hrrr       
for a in range(3):
    for i in range(800):
        if sum(h2[i,2:4]) < thres:
            h2[i,6:8] = -9999
            h2[i,0] = 0
        else:                                
            a_ref = 0
            a_ref = ((h2[i,2] + h2[i,3])*(h2[i,2] + h2[i,4]))/(h2[i,2]+h2[i,4]+h2[i,3]+h2[i,5])
    
            ### ets    
            h2[i,6] = (h2[i,2] - a_ref)/(h2[i,2] - a_ref + h2[i,4] + h2[i,3]) ## ETS
            h2[i,7] = (h2[i,2] + h2[i,4])/(h2[i,2] + h2[i,3])  ## BIAS
        
### nam4k        
for a in range(3):
    for i in range(800):
        if sum(n42[i,2:4]) < thres:
            n42[i,6:8] = -9999
            n42[i,0] = 0
        else:                                
            a_ref = 0
            a_ref = ((n42[i,2] + n42[i,3])*(n42[i,2] + n42[i,4]))/(n42[i,2]+n42[i,4]+n42[i,3]+n42[i,5])
    
            ### ets    
            n42[i,6] = (n42[i,2] - a_ref)/(n42[i,2] - a_ref + n42[i,4] + n42[i,3]) ## ETS
        #hitrate[s,i] = (hit[s,i])/(hit[s,i] + miss[s,i])
            n42[i,7] = (n42[i,2] + n42[i,4])/(n42[i,2] + n42[i,3])  ## BIAS
            
            
### nam12k        
for a in range(3):
    for i in range(800):
        if sum(n122[i,2:4]) < thres:
            n122[i,6:8] = -9999
            n122[i,0] = 0
        else:                                
            a_ref = 0
            a_ref = ((n122[i,2] + n122[i,3])*(n122[i,2] + n122[i,4]))/(n122[i,2]+n122[i,4]+n122[i,3]+n122[i,5])
    
            ### ets    
            n122[i,6] = (n122[i,2] - a_ref)/(n122[i,2] - a_ref + n122[i,4] + n122[i,3]) ## ETS
            n122[i,7] = (n122[i,2] + n122[i,4])/(n122[i,2] + n122[i,3])  ## BIAS



### gfs        
for a in range(3):
    for i in range(800):
        if sum(g2[i,2:4]) < thres:
            g2[i,6:8] = -9999
            g2[i,0] = 0
        else:                                
            a_ref = 0
            a_ref = ((g2[i,2] + g2[i,3])*(g2[i,2] + g2[i,4]))/(g2[i,2]+g2[i,4]+g2[i,3]+g2[i,5])
    
            ### ets    
            g2[i,6] = (g2[i,2] - a_ref)/(g2[i,2] - a_ref + g2[i,4] + g2[i,3]) ## ETS
            g2[i,7] = (g2[i,2] + g2[i,4])/(g2[i,2] + g2[i,3])  ## BIAS
            
            
            
  
            
            
            
            
        
###### Get elevation data
        
NCARens_file = '/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/random/wrfinput_d02'
fh = Dataset(NCARens_file, mode='r')

elevation = fh.variables['HGT'][:]
lat_netcdf = fh.variables['XLAT'][:]
long_netcdf = fh.variables['XLONG'][:]      
        
    

###############################################################################
################################## PLOTS ######################################
###############################################################################

cmap = matplotlib.cm.get_cmap('YlOrRd')
fig = plt.figure(figsize=(30,13.5))



#levels = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 6.5, 7, 7.5, 8 ,8.5, 9,9.5, 10,11, 12, 13, 14, 15, 16, 18, 20, 22,26,30,34,38,42]
levels = np.arange(0.000001, .80001, 0.05)
levels_el = np.arange(0,5000,100)
#######################   PRISM and SNOTEL event frequency  #############################################
top = 22
left = 22
tick = 16
info = 16
dots = 75

ax = fig.add_subplot(251)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(n[:,1], n[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = n[:,6], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = np.arange(0.000001, .80001, 0.10))
cbar.ax.tick_params(labelsize=12)
plt.title('NCAR Ensemble Control', fontsize = top)
cbar.ax.set_xticklabels(np.arange(0,0.80001,0.10), fontsize = tick)
plt.annotate('24-hr Upper Quartile Events', xy=(-0.06, .8),
             xycoords='axes fraction', fontsize = left, rotation = 90)
plt.annotate('Mean ETS = %1.3f' % np.average(n[:,6], weights=(n[:,6] >-5)), xy=(0.016, .024),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')
#cbar.ax.set_xlabel('Equitable Threat Score', fontsize = 12)

ax = fig.add_subplot(252)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(h[:,1], h[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = h[:,6], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = np.arange(0.000001, .80001, 0.1))
cbar.ax.tick_params(labelsize=tick)
plt.title('HRRR', fontsize = top)
cbar.ax.set_xticklabels(np.arange(0,0.80001,0.1), fontsize = tick)
plt.annotate('Mean ETS = %1.3f' % np.average(h[:,6], weights=(h[:,6] >-5)), xy=(0.016, .024),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')
#cbar.ax.set_xlabel('Equitable Threat Score', fontsize = 12)


ax = fig.add_subplot(253)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(n4[:,1], n4[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = n4[:,6], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = np.arange(0.000001, .80001, 0.1))
cbar.ax.tick_params(labelsize=tick)
plt.title('NAM-4km', fontsize = top)
cbar.ax.set_xticklabels(np.arange(0,0.80001,0.1), fontsize = tick)
plt.annotate('Mean ETS = %1.3f' % np.average(n4[:,6], weights=(n4[:,6] >-5)), xy=(0.016, .024),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')
#cbar.ax.set_xlabel('Equitable Threat Score', fontsize = 12)
             
             

ax = fig.add_subplot(254)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(n12[:,1], n12[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = n12[:,6], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = np.arange(0.000001, .80001, 0.1))
cbar.ax.tick_params(labelsize=tick)
plt.title('NAM-12km', fontsize = top)
cbar.ax.set_xticklabels(np.arange(0,0.80001,0.1), fontsize = tick)
plt.annotate('Mean ETS = %1.3f' % np.average(n12[:,6], weights=(n12[:,6] >-5)), xy=(0.016, .024),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')
#cbar.ax.set_xlabel('Equitable Threat Score', fontsize = 12)




ax = fig.add_subplot(255)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(g[:,1], g[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = g[:,6], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = np.arange(0.000001, .80001, 0.1))
cbar.ax.tick_params(labelsize=tick)
plt.title('GFS', fontsize = top)
cbar.ax.set_xticklabels(np.arange(0,0.80001,0.1), fontsize = tick)
plt.annotate('Mean ETS = %1.3f' % np.average(g[:,6], weights=(g[:,6] >-5)), xy=(0.016, .024),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')
#cbar.ax.set_xlabel('Equitable Threat Score', fontsize = 12)
             
             
             


ax = fig.add_subplot(256)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(n2[:,1], n2[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = n2[:,6], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = np.arange(0.000001, .80001, 0.1))
cbar.ax.tick_params(labelsize=12)
#plt.title('NCAR Ensemble Control (Upper Decile 24-hr Precip Events)', fontsize = 14)
cbar.ax.set_xticklabels(np.arange(0,0.80001,0.1), fontsize = tick)
cbar.ax.set_xlabel('Equitable Threat Score', fontsize = left)
plt.annotate('24-hr Upper Decile Events', xy=(-0.06, .8),
             xycoords='axes fraction', fontsize = top, rotation = 90)
plt.annotate('Mean ETS = %1.3f' % np.average(n2[:,6], weights=(n2[:,6] >-5)), xy=(0.016, .024),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')


ax = fig.add_subplot(257)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(h2[:,1], h2[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = h2[:,6], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = np.arange(0.000001, .80001, 0.1))
cbar.ax.tick_params(labelsize=tick)
#plt.title('HRRR (Upper Decile 24-hr Precip Events)', fontsize = 14)
cbar.ax.set_xticklabels(np.arange(0,0.80001,0.1), fontsize = tick)
cbar.ax.set_xlabel('Equitable Threat Score', fontsize = top)
plt.annotate('Mean ETS = %1.3f' % np.average(h2[:,6], weights=(h2[:,6] >-5)), xy=(0.016, .024),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')


ax = fig.add_subplot(258)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(n42[:,1], n42[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = n42[:,6], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = np.arange(0.000001, .80001, 0.1))
cbar.ax.tick_params(labelsize=tick)
#plt.title('NAM-4km (Upper Decile 24-hr Precip Events)', fontsize = 14)
cbar.ax.set_xticklabels(np.arange(0,0.80001,0.1), fontsize = tick)
cbar.ax.set_xlabel('Equitable Threat Score', fontsize = top)
plt.annotate('Mean ETS = %1.3f' % np.average(n42[:,6], weights=(n42[:,6] >-5)), xy=(0.016, .024),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')



ax = fig.add_subplot(259)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(n122[:,1], n122[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = n122[:,6], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = np.arange(0.000001, .80001, 0.1))
cbar.ax.tick_params(labelsize=12)
#plt.title('NAM-4km (Upper Decile 24-hr Precip Events)', fontsize = 14)
cbar.ax.set_xticklabels(np.arange(0,0.80001,0.1), fontsize = tick)
cbar.ax.set_xlabel('Equitable Threat Score', fontsize = top)
plt.annotate('Mean ETS = %1.3f' % np.average(n122[:,6], weights=(n122[:,6] >-5)), xy=(0.016, .024),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')
  

           
ax = fig.add_subplot(2,5,10)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(g2[:,1], g2[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = g2[:,6], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = np.arange(0.000001, .80001, 0.1))
cbar.ax.tick_params(labelsize=12)
#plt.title('NAM-4km (Upper Decile 24-hr Precip Events)', fontsize = 14)
cbar.ax.set_xticklabels(np.arange(0,0.80001,0.1), fontsize = tick)
cbar.ax.set_xlabel('Equitable Threat Score', fontsize = top)
plt.annotate('Mean ETS = %1.3f' % np.average(g2[:,6], weights=(g2[:,6] >-5)), xy=(0.016, .024),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')             
             
             
             
             
plt.tight_layout()
plt.savefig("../plots/ets_scatter_map_interp.png")
plt.show()



'''


###############################################################################
################################## PLOTS ######################################
###############################################################################

cmap = matplotlib.cm.get_cmap('BrBG')
fig = plt.figure(figsize=(24,13.5))




#######################   PRISM and SNOTEL event frequency  #############################################
top = 22
left = 22
tick = 16
info = 16
dots = 75


#levels = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 6.5, 7, 7.5, 8 ,8.5, 9,9.5, 10,11, 12, 13, 14, 15, 16, 18, 20, 22,26,30,34,38,42]
levels = np.arange(0.500001, 2.0001, 0.05)
levels = [0.1, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.2, 1.4, 1.6, 1.8,2, 5]
levels_el = np.arange(0,5000,100)

myticks= [0.1, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.2, 1.4, 1.6, 1.8,2,5]
      
label = ['<0.5','0.5','0.6', '0.7', '0.8', '0.9', '1', '1.2', '1.4', '1.6', '1.8','2','>2']
#######################   PRISM and SNOTEL event frequency  #############################################


ax = fig.add_subplot(241)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(n[:,1], n[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = n[:,7], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = myticks)
cbar.ax.tick_params(labelsize=12)
plt.title('NCAR Ensemble Control', fontsize = top)
cbar.ax.set_xticklabels(label, fontsize = tick)
plt.annotate('24-hr Upper Quartile Events', xy=(-0.06, .73),
             xycoords='axes fraction', fontsize = top, rotation = 90)
plt.annotate('Mean Bias Score = %1.3f' % np.average(n[:,7], weights=(n[:,7] >-5)), xy=(0.015, .02),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')
#cbar.ax.set_xlabel('Equitable Threat Score', fontsize = 12)

ax = fig.add_subplot(242)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(h[:,1], h[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = h[:,7], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = myticks)
cbar.ax.tick_params(labelsize=12)
plt.title('HRRR', fontsize = top)
cbar.ax.set_xticklabels(label, fontsize = tick)
plt.annotate('Mean Bias Score = %1.3f' % np.average(h[:,7], weights=(h[:,7] >-5)), xy=(0.015, .02),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')
#cbar.ax.set_xlabel('Equitable Threat Score', fontsize = 12)


ax = fig.add_subplot(243)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(n4[:,1], n4[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = n4[:,7], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = myticks)
cbar.ax.tick_params(labelsize=12)
plt.title('NAM-4km', fontsize = top)
cbar.ax.set_xticklabels(label, fontsize = tick)
plt.annotate('Mean Bias Score = %1.3f' % np.average(n4[:,7], weights=(n4[:,7] >-5)), xy=(0.015, .02),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')
#cbar.ax.set_xlabel('Equitable Threat Score', fontsize = 12)


ax = fig.add_subplot(244)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(n12[:,1], n12[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = n12[:,7], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = myticks)
cbar.ax.tick_params(labelsize=tick)
plt.title('NAM-12km', fontsize = top)
cbar.ax.set_xticklabels(label, fontsize = 10)
plt.annotate('Mean Bias Score = %1.3f' % np.average(n12[:,7], weights=(n12[:,7] >-5)), xy=(0.015, .02),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')
#cbar.ax.set_xlabel('Equitable Threat Score', fontsize = 12)


ax = fig.add_subplot(245)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(n2[:,1], n2[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = n2[:,7], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = myticks)
cbar.ax.tick_params(labelsize=12)
#plt.title('NCAR Ensemble Control (Upper Decile 24-hr Precip Events)', fontsize = 14)
cbar.ax.set_xticklabels(label, fontsize = tick)
cbar.ax.set_xlabel('Bias Score', fontsize = top)
plt.annotate('24-hr Upper Decile Events', xy=(-0.06, .73),
             xycoords='axes fraction', fontsize = top, rotation = 90)
plt.annotate('Mean Bias Score = %1.3f' % np.average(n2[:,7], weights=(n2[:,7] >-5)), xy=(0.015, .02),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')


ax = fig.add_subplot(246)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(h2[:,1], h2[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = h2[:,7], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = myticks)
cbar.ax.tick_params(labelsize=12)
#plt.title('HRRR (Upper Decile 24-hr Precip Events)', fontsize = 14)
cbar.ax.set_xticklabels(label, fontsize = tick)
cbar.ax.set_xlabel('Bias Score', fontsize = top)
plt.annotate('Mean Bias Score = %1.3f' % np.average(h2[:,7], weights=(h2[:,7] >-5)), xy=(0.015, .02),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')


ax = fig.add_subplot(247)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(n42[:,1], n42[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = n42[:,7], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = myticks)
cbar.ax.tick_params(labelsize=12)
#plt.title('NAM-4km (Upper Decile 24-hr Precip Events)', fontsize = 14)
cbar.ax.set_xticklabels(label, fontsize = tick)
cbar.ax.set_xlabel('Bias Score', fontsize = top)
plt.annotate('Mean Bias Score = %1.3f' % np.average(n42[:,7], weights=(n42[:,7] >-5)), xy=(0.015, .02),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')
             
             
ax = fig.add_subplot(248)
map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
x, y = map(n122[:,1], n122[:,0])
x2, y2 = map(long_netcdf[0,:,:], lat_netcdf[0,:,:])
csAVG2 = map.contourf(x2,y2,elevation[0,:,:], levels_el, cmap = 'Greys', zorder = 0)
csAVG = map.scatter(x,y, c = n122[:,7], cmap=cmap, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots)#,norm=matplotlib.colors.LogNorm() )  
map.drawcoastlines(linewidth = .5)
map.drawstates()
map.drawcountries()
cbar = map.colorbar(csAVG, location='bottom', pad="5%", ticks = myticks)
cbar.ax.tick_params(labelsize=12)
#plt.title('NAM-4km (Upper Decile 24-hr Precip Events)', fontsize = 14)
cbar.ax.set_xticklabels(label, fontsize = tick)
cbar.ax.set_xlabel('Bias Score', fontsize = top)
plt.annotate('Mean Bias Score = %1.3f' % np.average(n122[:,7], weights=(n122[:,7] >-5)), xy=(0.015, .02),
             xycoords='axes fraction', fontsize = info, backgroundcolor = 'w')
             
             
plt.tight_layout()
plt.savefig("../plots/bias_scatter_map_interp.png")
plt.show()
'''















