
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
import matplotlib.lines as mlines




nearestNCAR = zeros((785,650))
totalprecip = zeros((125000))
totalprecip_hrrr = zeros((125000))
totalprecip_nam4k = zeros((125000))
Date = zeros((152))
frequency = zeros((100,10))
bias = zeros((100,10))
frequency_snotel = zeros((40,3))
daily_snotel_precip = zeros((125000))
snotel_rowloc = zeros((798))
snotel_colloc = zeros((798))



###############################################################################
############ Read in  12Z to 12Z data   #####################
###############################################################################




inhouse_data = zeros((649,186))
ncar_data = zeros((798,186))
nam4k_data = zeros((798,186))
nam12k_data = zeros((798,186))
hrrr_data = zeros((798,186))
hrrrv2_data = zeros((798,186))
            
x = 0
q = 0
v = 0
i = 0  # hrrr_precip_12Zto12Z_TEST_hr3_15.txt

# Raw model data at snotel sites
links = ["/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/snotel_precip_2015_2016_qc.csv", 
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/ncarens_precip_12Zto12Z.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/nam4k_precip_12Zto12Z.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/hrrr_precip_12Zto12Z_TEST_hr3_15.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/nam12k_precip_12Zto12Z.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/hrrrV2_precip_12Zto12Z.txt"]
'''
 # Bilinearly interpolated model data at snotel sites        
links = ["/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/snotel_precip_2015_2016_qc.csv", 
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/ncarens_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/nam4km_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/hrrrV1_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/nam12km_precip_12Zto12Z_interp.txt",
         "/uufs/chpc.utah.edu/common/home/steenburgh-group5/tom/snotel_data/hrrrV2_precip_12Zto12Z_interp.txt"]
'''
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
hrrrv2_data = data[5,:,:]

'''
for x in range(len(data[1,:,0])):
                    num = 0
                    for r in range(3,186):
                        if all(data[:,x,r] < 1000):  # Make sure all models have data for that day
                            pass
                                
                        else: 
                            num = num + 1
                    print num
'''

bins = 30
j = 0

print c
# print ranges in array
for x in range(1,bins):
        x = x*2.54
        y = x-2.54
        frequency[j,c+1] = x-1.27
        bias[j,c+1] = x-1.27
        j = j + 1


## Frequency of event for each model
num = 0

for c in range(1,6): # loop over snotel, ncar, nam4k, hrrr, nam12k, hrrrv2
    print c
    j = 0
    for x in range(1,bins):
        print x
        x = x*2.54
        y = x-2.54
        for z in range(len(data[c,:,0])):
            for f in range(len(data[0,:,0])):
                    if data[c,z,0] == data[0,f,0]:

                        for r in range(3,185):
                            if all(data[1:,z,r] < 1000) and data[0,f,r] < 1000:

                                if data[c,z,r] > y and data[c,z,r] <= x:
                                    frequency[j,c] = frequency[j,c] + 1

        j = j + 1


j = 0
## Frequency of event for snotel data
for x in range(1,bins):
        x = x*2.54
        y = x-2.54
        for f in range(len(data[0,:,0])):
            for z in range(len(data[1,:,0])):
                if data[1,z,0] == data[0,f,0]:
                    for r in range(3,186):
                        if all(data[1:,z,r] < 1000) and data[0,f,r] < 1000:  # Make sure all models have data for that day
                            if data[0,z,r] > y and data[0,z,r] <= x:
                                frequency[j,0] = frequency[j,0] + 1
        j = j + 1  

    





sum_inhouse = sum(frequency[:,0])
sum_ncar = sum(frequency[:,1])
sum_nam4k = sum(frequency[:,2])
sum_hrrr = sum(frequency[:,3])
sum_nam12k = sum(frequency[:,4])
sum_hrrrv2 = sum(frequency[:,5])

#### Calculate Frequencues



for i in range(0,bins):
 

   frequency[i,0]= frequency[i,0]/sum_inhouse*100 
   frequency[i,1]= frequency[i,1]/sum_ncar*100 
   frequency[i,2]= frequency[i,2]/sum_nam4k*100 
   frequency[i,3]= frequency[i,3]/sum_hrrr*100 
   frequency[i,4]= frequency[i,4]/sum_nam12k*100
   frequency[i,5]= frequency[i,5]/sum_hrrrv2*100 

for i in range(0,bins):
   
   bias[i,0] = frequency[i,1]/frequency[i,0] #NCARens
   bias[i,1] = frequency[i,2]/frequency[i,0] #nam4k
   bias[i,2] = frequency[i,3]/frequency[i,0] #HRRRR
   bias[i,3] = frequency[i,4]/frequency[i,0] #nam12k
   bias[i,4] = frequency[i,5]/frequency[i,0] #hrrrv2


    






#fig1 = plt.figure()

fig1=plt.figure(num=None, figsize=(11, 11), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.4, bottom = 0.1)
ax1 = fig1.add_subplot(211)
plt.xlim([0,60])
plt.xticks(np.arange(0,61,6))
ax1.set_xticks(np.arange(0,61,6))
ax1.set_xticklabels(np.arange(0,61,6), fontsize = 16)
plt.ylim([0.1,60])
#ax1.set_yscale('log')
linecolor = ['gold','blue', 'green', 'red', 'c','darkred']

plt.gca().set_color_cycle(linecolor)
plt.grid(True)
ax1.plot(frequency[:,6],frequency[:,0:6],linewidth = 2, marker = "o", markeredgecolor = 'none')
#,['50','30','20','10','5','1','0.75','0.5','0.2','0.1'])

ax1.set_yscale('log')
ax1.set_yticks([60,35,20,10,5,2,1,0.5,0.2,0.1,0.05])
ax1.set_yticklabels(['60','35','20','10','5','2','1','0.5','0.2','0.1','0.05'], fontsize = 14)
ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%1.2f'))
black = mlines.Line2D([], [], color='gold',
                           label='SNOTEL', linewidth = 2,marker = "o", markeredgecolor = 'none')
blue = mlines.Line2D([], [], color='blue',
                           label='NCAR Ens Control', linewidth = 2,marker = "o", markeredgecolor = 'none')
green = mlines.Line2D([], [], color='green',
                           label='NAM-4km', linewidth = 2,marker = "o", markeredgecolor = 'none')
red = mlines.Line2D([], [], color='red',
                           label='HRRRV1 (hrs 2-14)', linewidth = 2,marker = "o", markeredgecolor = 'none')
cyan = mlines.Line2D([], [], color='c',
                           label='NAM-12km', linewidth = 2,marker = "o", markeredgecolor = 'none')
darkred = mlines.Line2D([], [], color='darkred',
                           label='HRRRV2 (hrs 3-15)', linewidth = 2,marker = "o", markeredgecolor = 'none')


plt.legend(handles=[black, blue, green, red, cyan, darkred], fontsize = 15)
plt.title('Event Size Frequency', fontsize = 22)
plt.xlabel('24-hour Precipitation (mm)', fontsize = 17, labelpad = 10)
plt.ylabel('Frequency (%)', fontsize = 17, labelpad = 10)





##############  Bias Plots






ax2 = fig1.add_subplot(212)
plt.xlim([0,60])
plt.xticks(np.arange(0,61,6))



plt.grid(True)
line1 = ax2.plot(bias[:,6],bias[:,0])
line2 = ax2.plot(bias[:,6],bias[:,1])
line3 = ax2.plot(bias[:,6],bias[:,2])
line4 = ax2.plot(bias[:,6],bias[:,3])
line5 = ax2.plot(bias[:,6],bias[:,4])

x = np.linspace(0, 200, 200)
y = np.linspace(1,1,200)
line6 = ax2.plot(x,y)

plt.yticks(np.arange(0.4,2.5001,0.2))
ax2.set_yticklabels(np.arange(0.4,2.5001,0.2), fontsize = 16)
plt.ylim([.4, 2])
ax2.set_xticklabels(np.arange(0, 61,6), fontsize = 16)
#ax1.set_yticks([50,20,10,5,2,1,0.5,0.2,0.1,0.05])
#ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
#ax1.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%1.2f'))

plt.setp(line1, color='blue', linewidth=2.0,marker = "o", markeredgecolor = 'none')
plt.setp(line2, color='green', linewidth=2.0,marker = "o", markeredgecolor = 'none')
plt.setp(line3, color='red', linewidth=2.0,marker = "o", markeredgecolor = 'none')
plt.setp(line4, color='c', linewidth=2.0,marker = "o", markeredgecolor = 'none')
plt.setp(line5, color='darkred', linewidth=2.0,marker = "o", markeredgecolor = 'none')
plt.setp(line6, color='k', linewidth=2)
blue = mlines.Line2D([], [], color='blue',
                           label='NCAR Ens Control', linewidth = 2,marker = "o", markeredgecolor = 'none')
green = mlines.Line2D([], [], color='green',
                           label='NAM-4km', linewidth = 2,marker = "o", markeredgecolor = 'none')
red = mlines.Line2D([], [], color='red',
                           label='HRRRv1', linewidth = 2,marker = "o", markeredgecolor = 'none')
cyan = mlines.Line2D([], [], color='c',
                           label='NAM-12km', linewidth = 2,marker = "o", markeredgecolor = 'none')
darkred = mlines.Line2D([], [], color='darkred',
                           label='HRRRv2', linewidth = 2,marker = "o", markeredgecolor = 'none')
#plt.legend(handles=[blue, green, red, cyan, darkred],bbox_to_anchor=(0.13, .1), fontsize = 14)
plt.title('Event Size Frequency Bias', fontsize = 22)
plt.xlabel('24-hour Precipitation (mm)', fontsize = 17, labelpad = 10)
plt.ylabel('Bias Ratio', fontsize = 17, labelpad = 10)

plt.savefig("../plots/dailyprecip_bias_binned_interp.pdf")
plt.show()














