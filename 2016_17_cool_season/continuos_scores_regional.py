
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

links = ["/uufs/chpc.utah.edu/common/home/steenburgh-group5/cstar/snotel/Tom_in_house.csv", 
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/SNOTEL/ncarens_precip_12Zto12Z.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/SNOTEL/nam4k_precip_12Zto12Z.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/SNOTEL/hrrr_precip_12Zto12Z.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/SNOTEL/nam12k_precip_12Zto12Z.txt"]

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
########################### NCAR forecast vs. observed ########################
###############################################################################
i = 0
u = 0
end = 19   
precip = zeros((2000,186))

bins = np.arange(2.54,50, 2.54)
ncar_array = zeros((len(bins)-1, len(bins)-1))
ncar_array_norm = zeros((len(bins)-1, len(bins)-1))

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


for x in range(len(ncar_data[:,0])):
    for y in range(len(inhouse_data[:,0])):
        if ncar_data[x,0] == inhouse_data[y,0]:
            

### Create forecat and observed array (forecast on x axis and oberved on y axis)     
            for z in range(3,185):
                        # Excludes bad data 
                        if ncar_data[x,z] < 1000 and  inhouse_data[y,z] < 1000:
                            for i in range(len(bins)-1):
                                for j in range(len(bins)-1):
                                    if bins[i] - 1.27 <= ncar_data[x,z] < bins[i+1] -1.27 and bins[j] <= inhouse_data[y,z] < bins[j+1]:
                                        print i, j
                                        print('yo') 
                                        ncar_array[j,i] = ncar_array[j,i] + 1



### To nomalize the data
for i in range(len(bins)-1):
    for j in range(len(bins)-1):
        ncar_array_norm[j,i] = ncar_array[j,i]/((max(ncar_array[j,:])+max(ncar_array[:,i]))/2)











          





    
   
                       

###############################################################################
################### NAM4k forecast vs. observed ########################
###############################################################################

end = 19   
u = u + 1
nam4k_array = zeros((len(bins)-1, len(bins)-1))
nam4k_array_norm = zeros((len(bins)-1, len(bins)-1))
precip = zeros((2000,186))


for x in range(len(nam4k_data[:,0])):
    for y in range(len(inhouse_data[:,0])):
        if nam4k_data[x,0] == inhouse_data[y,0]:
            
            for z in range(3,185):
                # Excludes bad data 
                if nam4k_data[x,z] < 1000 and  inhouse_data[y,z] < 1000:
                    for i in range(len(bins)-1):
                        for j in range(len(bins)-1):
                            if bins[i]-1.27 <= nam4k_data[x,z] < bins[i+1]-1.27 and bins[j] <= inhouse_data[y,z] < bins[j+1]:
                                nam4k_array[j,i] = nam4k_array[j,i] + 1



### To nomalize the data
for i in range(len(bins)-1):
    for j in range(len(bins)-1):
        nam4k_array_norm[j,i] = nam4k_array[j,i]/((max(nam4k_array[j,:])+max(nam4k_array[:,i]))/2)


    
        
                       


###############################################################################
##################### HRRR forecast vs. observed ########################
###############################################################################

end = 19   
u = u + 1
hrrr_array = zeros((len(bins)-1, len(bins)-1))
hrrr_array_norm = zeros((len(bins)-1, len(bins)-1))
p_array = []
precip = zeros((2000,186))



for x in range(len(hrrr_data[:,0])):
    for y in range(len(inhouse_data[:,0])):
        if hrrr_data[x,0] == inhouse_data[y,0]:
            
            for z in range(3,185):
                
                # Excludes bad data 
                if hrrr_data[x,z] < 1000 and  inhouse_data[y,z] < 1000:
                    for i in range(len(bins)-1):
                        for j in range(len(bins)-1):
                            if bins[i]-1.27 <= hrrr_data[x,z] < bins[i+1]-1.27 and bins[j] <= inhouse_data[y,z] < bins[j+1]:
                                print('hi')
                                hrrr_array[j,i] = hrrr_array[j,i] + 1



### To nomalize the data
for i in range(len(bins)-1):
    for j in range(len(bins)-1):
        hrrr_array_norm[j,i] = hrrr_array[j,i]/((max(hrrr_array[j,:])+max(hrrr_array[:,i]))/2)









###############################################################################
#################### NAM12k forecast vs. observed ########################
###############################################################################
precip = zeros((2000,186))
end = 19
u = u + 1
nam12k_array = zeros((len(bins)-1, len(bins)-1))
nam12k_array_norm = zeros((len(bins)-1, len(bins)-1))


for x in range(len(nam12k_data[:,0])):
    for y in range(len(inhouse_data[:,0])):
        if nam12k_data[x,0] == inhouse_data[y,0]:
            for z in range(3,185):
                
                # Excludes bad data 
                if nam12k_data[x,z] < 1000 and  inhouse_data[y,z] < 1000:
                    for i in range(len(bins)-1):
                        for j in range(len(bins)-1):
                            if bins[i]-1.27 <= nam12k_data[x,z] < bins[i+1]-1.27 and bins[j] <= inhouse_data[y,z] < bins[j+1]:
                                nam12k_array[j,i] = nam12k_array[j,i] + 1
                                            


### To nomalize the data
for i in range(len(bins)-1):
    for j in range(len(bins)-1):
        nam12k_array_norm[j,i] = nam12k_array[j,i]/((max(nam12k_array[j,:])+max(nam12k_array[:,i]))/2)

'''
'''
###### Change to frequencies
array = zeros((4,18,18))
array[0,:,:] = ncar_array
array[1,:,:] = hrrr_array
array[2,:,:] = nam4k_array
array[3,:,:] = nam12k_array

for i in range(4):
    tot = np.sum(array[i])
    array[i] = array[i]/tot
  
#####  Determine most likely forecasted amounts for each snotel value
#array_32 = zeros((4,18,18))
array2 = array
array3 = array


for i in range(4):
    for j in range(18):
        #m = np.percentile(array2[i,:,j],95)
        m = max(array2[i,:,j])
        for t in range(18):
            if m == array2[i,t,j]:
                pass
            else:
                array2[i,t,j] = 0

array3 = zeros((4,18,18))
array3[0,:,:] = ncar_array
array3[1,:,:] = hrrr_array
array3[2,:,:] = nam4k_array
array3[3,:,:] = nam12k_array

for i in range(4):
    for j in range(18):
        #m = np.percentile(array2[i,:,j],95)
        m = max(array3[i,j,:])
        for t in range(18):
            if m == array3[i,j,t]:
                pass
            else:
                array3[i,j,t] = 0 
                
array2 = array2+array3
                
'''
###### Change to frequencies
array = zeros((4,18,18))
array[0,:,:] = ncar_array
array[1,:,:] = hrrr_array
array[2,:,:] = nam4k_array
array[3,:,:] = nam12k_array

for i in range(4):
    tot = np.sum(array[i])
    array[i] = array[i]/tot


        

###############################################################################
#########################  PLots   ############################################
###############################################################################


###############################################################################
#####  Code found online to discritize any color map ##########################
###############################################################################

def discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap from the specified input map"""

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)




model = ['NCAR Ensemble Control', 'HRRR', 'NAM-4km','NAM-12km'] 
labels = np.arange(2.54,60,2.54)
x = np.arange(0,20,2)
y = np.arange(0,20,2)
fig1=plt.figure(num=None, figsize=(12,12), dpi=500, facecolor='w', edgecolor='k')
ax2 = fig1.add_axes([0.025,0.12,1.08,0.78])
ax2.axis('off')
plot = 220
#array = [ncar_array, nam4k_array, hrrr_array, nam12k_array]

for i in range(4):
    g = array[i]
    #ax1.yaxis.set_major_formatter(FormatStrFormatter('%1.1f'))
    #ax1.xaxis.set_major_formatter(FormatStrFormatter('%1.1f'))
    print i
    plot = 221 + i
    ax1 = fig1.add_subplot(plot)
    plt.title(model[i], fontsize = 22)
    #ax1.tick_params(axis='x', which='both', bottom='on', labelbottom='on') 
    plt.grid(True)  
    ##plt.tick_params(axis='y', which='both', bottom='on')
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    if i == 2 or i == 3:

        ax1.set_xlabel('Forecasted 24-hour Events (mm)', fontsize  = 18, labelpad = 12)
    if i == 0 or i == 2:

        ax1.set_ylabel('Observed 24-hour Events (mm)', fontsize  = 18, labelpad = 12)
    if i == 2 or i == 3:
        ax1.set_xticklabels([(i*2.54)+1.27 for i in x], fontsize  = 16, rotation = 60)
    else:
        ax1.set_xticklabels([])
    if i == 2 or i == 0:
        ax1.set_yticklabels([(i*2.54)+1.27 for i in y], fontsize = 16)
    else:
        ax1.set_yticklabels([])

    if plot == 223: 
        ax1.set_yticklabels([(i*2.54)+1.27 for i in y], fontsize = 16)
 


   
    heatmap = ax1.pcolor(g, vmin=0.00005, vmax=.1, cmap=discrete_cmap(12, 'jet'), norm=matplotlib.colors.LogNorm())

    lims = [
        np.min([ax1.get_xlim(), ax1.get_ylim()]),  # min of both axes
        np.max([ax1.get_xlim(), ax1.get_ylim()]),  # max of both axes
        ]

    # now plot both limits against eachother
    ax1.plot(lims, lims, 'k', alpha=1, zorder=1)
    ax1.set_aspect('equal')
    ax1.set_xlim(lims)
    ax1.set_ylim(lims)
formatter = LogFormatter(10)#, labelOnlyBase=False) 
#cbar = plt.colorbar(heatmap, ax = ax2, ticks=[1,1.77,3.16,10**.75, 10, 10**1.25, 10**1.5, 10**1.75, 10**2, 10**2.25, 10**2.5, 10**2.75, 10**3],format = formatter)
ticks = np.logspace(1, 0.232503, num = 13, base = 0.00005)
cbar = plt.colorbar(heatmap, ax = ax2,ticks = ticks,format = formatter)
cbar.ax.set_yticklabels(['0.00005', '0.00009', '0.0002', '0.0003','0.0006','0.001','0.002','0.004','0.008','0.015','0.03','0.05','0.1'], fontsize = 16)
cbar.ax.set_xlabel('\nFrequency', fontsize  = 16)
#plt.tight_layout()
plt.savefig("../public_html/heatmaps.pdf", bbox_inches='tight')
plt.show()








###############################################################################
#########################  PLots   ############################################
###############################################################################


###############################################################################
#####  Code found online to discritize any color map ##########################
###############################################################################

def discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap from the specified input map"""

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)




model = ['NCARens Control', 'HRRR', 'NAM-4km','NAM-12km'] 
labels = np.arange(2.54,60,2.54)
x = np.arange(0,20,1)
y = np.arange(0,20,1)
fig1=plt.figure(num=None, figsize=(12,12), dpi=500, facecolor='w', edgecolor='k')
ax2 = fig1.add_axes([0.025,0.12,1.08,0.78])
plt.axis('off')
plot = 220
#array = [ncar_array, nam4k_array, hrrr_array, nam12k_array]

for i in range(4):
    g = array2[i]

    print i
    plot = 221 + i
    ax1.set_xticks(x)
    ax1.set_yticks(y)
    ax1.set_yticklabels([])
    ax1 = fig1.add_subplot(plot)
    plt.title(model[i], fontsize = 22)
    if i == 2 or i == 3:
        ax1.set_xlabel('Forecasted 24-hour Event Size (mm)', fontsize  = 18, labelpad = 12)
    if i == 0 or i == 2:
        ax1.set_ylabel('Observed 24-hour Event Size (mm)', fontsize  = 18, labelpad = 12)


    if i == 0 or i == 2:
        ax1.set_yticklabels([(i*5.08)+1.27 for i in y], fontsize = 17)
    else:
        ax1.set_yticklabels([])
    if i == 2 or i == 3:
        ax1.set_xticklabels([(i*5.08)+1.27 for i in x], fontsize  = 17, rotation = 45)
    else:
        ax1.set_xticklabels([])

    
   
    heatmap = ax1.pcolor(g, vmin=0.00005, vmax=.1, cmap=discrete_cmap(12, 'jet'), norm=matplotlib.colors.LogNorm())

    lims = [
        np.min([ax1.get_xlim(), ax1.get_ylim()]),  # min of both axes
        np.max([ax1.get_xlim(), ax1.get_ylim()]),  # max of both axes
        ]

    # now plot both limits against eachother
    ax1.plot(lims, lims, 'k', alpha=1, zorder=1)
    ax1.set_aspect('equal')
    ax1.set_xlim(lims)
    ax1.set_ylim(lims)
formatter = LogFormatter(10)#, labelOnlyBase=False) 
#cbar = plt.colorbar(heatmap, ax = ax2, ticks=[1,1.77,3.16,10**.75, 10, 10**1.25, 10**1.5, 10**1.75, 10**2, 10**2.25, 10**2.5, 10**2.75, 10**3],format = formatter)
ticks = np.logspace(1, 0.232503, num = 13, base = 0.00005)
cbar = plt.colorbar(heatmap, ax = ax2,ticks = ticks,format = formatter)
cbar.ax.set_yticklabels(['0.00005', '0.00009', '0.0002', '0.0003','0.0006','0.001','0.002','0.004','0.008','0.015','0.03','0.05','0.1'], fontsize = 16)

cbar.ax.set_xlabel('\nFreq', fontsize  = 16)
plt.savefig("./plots/heatmaps_greatesst.pdf", bbox_inches='tight')
plt.show()







####   Ideal example plots

ideal = zeros((18,18))
for i in range(18):
    ideal[i,i] = 9-.5*i
    if i > 0:
        ideal[i,i-1] = 9-.5*i
        ideal[i-1,i] = 9-.5*i
        
notideal = zeros((18,18))
for i in range(18):
        notideal[17-i,:] = 19-np.arange(1,162,9) +10*i



x = np.arange(0,20,1)
y = np.arange(0,20,1)
fig1=plt.figure(num=None, figsize=(12,12), dpi=500, facecolor='w', edgecolor='k')
ax2 = fig1.add_axes([.11,0.335,.97,0.355])
plt.axis('off')
plot = 220
#array = [ncar_array, nam4k_array, hrrr_array, nam12k_array]
model = ['High Accuracy', 'Low Accuracy'] 

for i in range(2):


    print i
    plot = 121 + i
    ax1 = fig1.add_subplot(plot)
    plt.title(model[i], fontsize = 23)

    if i == 1 or i ==0:
        ax1.set_xlabel('Forecasted Event Size', fontsize  = 20, labelpad = 15)


    if i == 0:
        ax1.set_ylabel('Observed Event Size', fontsize  = 20, labelpad = 15)

    #ax1.set_xticks(x)
    #ax1.set_yticks(y)
    #ax1.set_xticklabels([(i*2.54)+1.27 for i in x], fontsize  = 10, rotation = 45)
    #ax1.set_yticklabels([(i*2.54)+1.27 for i in y], fontsize = 10)

    
    if i == 0:
        heatmap = ax1.pcolor(ideal, vmin=1, vmax=9, cmap=discrete_cmap(12, 'jet'), norm=matplotlib.colors.LogNorm())
    if i == 1:
        heatmap = ax1.pcolor(notideal, vmin = 20, vmax=170, cmap=discrete_cmap(12, 'jet'))#, norm=matplotlib.colors.LogNorm())
    ax1.set_yticklabels([])
    ax1.set_xticklabels([])


    lims = [
        np.min([ax1.get_xlim(), ax1.get_ylim()]),  # min of both axes
        np.max([ax1.get_xlim(), ax1.get_ylim()]),  # max of both axes
        ]
    # now plot both limits against eachother
    ax1.plot(lims, lims, 'k', alpha=1, zorder=1)
    ax1.set_aspect('equal')
    ax1.set_xlim(lims)
    ax1.set_ylim(lims)

formatter = LogFormatter(10)#, labelOnlyBase=False) 
#cbar = plt.colorbar(heatmap, ax = ax2, ticks=[1,1.77,3.16,10**.75, 10, 10**1.25, 10**1.5, 10**1.75, 10**2, 10**2.25, 10**2.5, 10**2.75, 10**3],format = formatter)
ticks = np.logspace(1, 0.232503, num = 13, base = 0.00005)
cbar = plt.colorbar(heatmap, ax = ax2,ticks = ticks,format = formatter)
#cbar.ax.set_yticklabels(['0.00005', '0.00009', '0.0002', '0.0003','0.0006','0.001','0.002','0.004','0.008','0.015','0.03','0.05','0.1'], fontsize = 12)

cbar.ax.set_xlabel('\nFrequency', fontsize  = 19)
plt.savefig("../public_html/heatmaps_examples.pdf", bbox_inches='tight')
plt.show()



