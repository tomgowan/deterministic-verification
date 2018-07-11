import matplotlib as mpl
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
import nclcmaps


    

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


snotel = np.copy(data[0,:,:])

######### Each portion of array is data from models as below ##################
#data[1,:,:] = ncarens
#data[2,:,:] = gfs13
#data[3,:,:] = hrrr
#data[4,:,:] = nam3km
#data[4,:,:] = sref_arw
#data[4,:,:] = sref_nmmb
###############################################################################        

#%%


###############################################################################
########################### Calculate ETS #####################################
###############################################################################
i = 0
u = 0
end = 19   
hit = zeros((end,4)) #### There arrays now go in the order col 1-4:region 1, 5-8:region2,etc...
miss = zeros((end,4))
falarm = zeros((end,4))
correct_non = zeros((end,4))


#Hold all computed statistics
data_stats = zeros((len(data[:,0,0]),len(data[0,:,0]),10))
#Choose Threshold
percent= 90

######################  Calculate simple scores ###############################
#Loop over all models
for model in range(1,len(data[:,0,0])):
    
    #Match stations in model and snotel 
    for station_mod in range(len(data[model,:,0])):
                for station_sno in range(len(snotel[:,0])):
                        if data[model,station_mod,0] == snotel[station_sno,0]:
                            data_stats[model,station_sno,0:3] = np.copy(data[model,station_mod,0:3])

                            #Calculate percentile for model and snotel
                            percentile_mod = np.nanpercentile(data[model,station_mod,3:],percent)
                            percentile_sno = np.nanpercentile(snotel[station_sno,3:],percent)

                            #Loop through days
                            for day in range(3,185):
                            
                                # Excludes bad data 
                                if any(np.isnan(data[1:,station_mod,day])) or np.isnan(snotel[station_sno,day]):
                                    pass
                                else:
                                    
                                    ##### Hits
                                    if data[model,station_mod,day] >= percentile_mod and snotel[station_sno,day] >= percentile_sno:
                                        data_stats[model,station_sno,3] += 1
                                    ##### Misses
                                    if data[model,station_mod,day] < percentile_mod and snotel[station_sno,day] >= percentile_sno:
                                        data_stats[model,station_sno,4] += 1
                                    ##### Falarm
                                    if data[model,station_mod,day] >= percentile_mod and snotel[station_sno,day] < percentile_sno:
                                        data_stats[model,station_sno,5] += 1
                                    ##### Correct nonevent
                                    if data[model,station_mod,day] < percentile_mod and snotel[station_sno,day] < percentile_sno:
                                        data_stats[model,station_sno,6] += 1
                                    

                            
################################ Calculate ETS ################################                       

#Minimum number of events                      
thres = 10
                       
for model in range(len(data[:,0,0])):
    for station in range(len(data[0,:,0])):
        
        #Make sure station has minimum number of events
        if sum(data_stats[model,station,3:5]) < thres:
            data_stats[model,station,7:9] = np.nan
            data_stats[model,station,0] = np.nan
        
        #If there are enough events compute ETS
        else:                                
            a_ref = ((data_stats[model,station,3] + data_stats[model,station,4])*(data_stats[model,station,3] + data_stats[model,station,5]))/(data_stats[model,station,3]+data_stats[model,station,5]+data_stats[model,station,4]+data_stats[model,station,6])
    
            ###ETS    
            data_stats[model,station,7] = (data_stats[model,station,3] - a_ref)/(data_stats[model,station,3] - a_ref + data_stats[model,station,5] + data_stats[model,station,4])
            ###BIAS
            data_stats[model,station,8] = (data_stats[model,station,3] + data_stats[model,station,5])/(data_stats[model,station,3] + data_stats[model,station,4])                       
                        
            
            
            
#%%             
            
            
            
###############################################################################
################################   PLOT   #####################################
###############################################################################                        
                        
                        
###### Get elevation data
        
el_file = '/uufs/chpc.utah.edu/common/home/horel-group/archive/terrain/WesternUS_terrain.nc'
fh = Dataset(el_file, mode='r')

elevation = fh.variables['elevation'][:]
lat = fh.variables['latitude'][:]
lon = fh.variables['longitude'][:]  

lat_netcdf = zeros((3600,3600))
long_netcdf = zeros((3600,3600))
for i in range(3600):
    lat_netcdf[:,i] = lat
    long_netcdf[i,:] = lon  
        
    
#Figure
fig=plt.figure(num=None, figsize=(11,20), dpi=300, facecolor='w', edgecolor='k')

#Read in colormap and put in proper format
colors1 = np.array(nclcmaps.colors['WhiteBlueGreenYellowRed'])#perc2_9lev'])
colors_int = colors1.astype(int)
colors = list(colors_int)
cmap_ets = nclcmaps.make_cmap(colors, bit=True)

#Levels
levels = np.arange(0, 0.8001, 0.05)
levels_ticks = np.arange(0, 0.8001, 0.1)
levels_el = np.arange(0,5000,100)

#Sizes
top = 22
left = 22
tick = 16
info = 16
dots = 75

cmap = cmap_ets

for model in range(1,7):
    subplot = 320 + model
    ax = plt.subplot(subplot,aspect = 'equal')
    plt.subplots_adjust(left=0.02, bottom=0.1, right=0.98, top=0.97, wspace=0.03, hspace=0.1)

    

    latlon = [-125.3, 31.0, -102.5, 49.2]
    map = Basemap(projection='merc',llcrnrlon=latlon[0],llcrnrlat=latlon[1],urcrnrlon=latlon[2],urcrnrlat=latlon[3],resolution='i')
    
    #lat lon for station and elevation
    x, y = map(data_stats[model,:,2], data_stats[model,:,1])
    x2, y2 = map(long_netcdf, lat_netcdf)
    
    #Plot elevation
    elev = map.contourf(x2,y2,elevation, levels_el, cmap = 'Greys', zorder = 0)
    #Plot scatter ETS
    ets = map.scatter(x,y, c = data_stats[model,:,7], cmap=cm.Blues, marker='o', norm=matplotlib.colors.BoundaryNorm(levels,cmap.N), s = dots, vmin = -0.1, edgecolor = 'k')
    
    #Plot characterisitcs
    map.drawcoastlines(linewidth = .5)
    map.drawstates()
    map.drawcountries()
    
    #Title
    title = ['NCAR ENS CTL', 'GFS', 'HRRR', 'NAM-3km', 'SREF ARW CTL', 'SREF NMMB CTL']
    plt.title(title[model-1], fontsize = top)
    
    #Text
    props = dict(boxstyle='square', facecolor='white', alpha=1)
    ax.text(100000, 130000, 'Mean ETS = %1.3f' % np.nanmean(data_stats[model,:,7]), fontsize = 17, bbox = props)

#Colorbar
cbaxes = fig.add_axes([0.15, 0.06, 0.7, 0.023])             
cbar = plt.colorbar(ets, cax = cbaxes, ticks = levels_ticks, orientation="horizontal")
cbar.ax.tick_params(labelsize=17)
plt.text(0.18, -1.9, 'ETS for Upper Decile Events', fontsize = 23)
    
    
    
    
    

plt.savefig("/uufs/chpc.utah.edu/common/home/u1013082/public_html/phd_plots/random/ets_by_station_upper_decile.png", dpi = 300)
plt.close()                       
                        
                        
                        
                        
                        
                        
                        
                        
                        